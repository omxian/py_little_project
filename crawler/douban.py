import requests
import crawler.douban_export_excel
from lxml import html
import re
import threading
import time
import sys
lock = threading.Lock()
datas = []
item_id = 1
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,ima'
              'ge/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                  '537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Connection': 'keep-alive',
    'Host': 'https://book.douban.com',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referrer': 'https://book.douban.com',
}


def crawl(origin_url):
    resp = requests.get(origin_url, headers)
    page = resp.content
    root = html.fromstring(page)
    contents = root.xpath('//*[@id="content"]/div/div[1]/div[2]/div/table/tbody/tr/td/a')
    thread = []
    progress = 0
    print("Total data length %d" % len(contents))
    for content in contents:
        t = threading.Thread(target=handle_item_list, args=(content.text,))
        t.start()
        thread.append(t)

        progress += 1
        sys.stdout.write("\r" + str(progress) + "/" + str(len(contents)))
        sys.stdout.flush()

    print("\nHandling Data...")
    for t in thread:
        t.join()

    print("Generating Excel, data length %d..." % len(datas))
    crawler.douban_export_excel.export_excel(datas)


def handle_item_list(small_type):
    # TODO 此处只拉取了类目的前20条，可以修改分页代码拉取更多信息
    item_list_url = 'https://book.douban.com/tag/' + small_type + '?start=0&type=T'
    headers["Referer"] = "https://book.douban.com/tag/?view=type"
    resp = requests.get(item_list_url, headers)
    page = resp.content
    root = html.fromstring(page)
    items = root.xpath('//*[@id="subject_list"]/ul/li/div[2]')

    for item in items:
        global item_id
        # TODO 拉取了部分信息，可以拉取热门评价、详细介绍等
        data = {
            'id': item_id,
            'name': item.xpath('h2/a/@title')[0],
            'author': item.xpath('div[@class="pub"]')[0].text.split('/')[0].strip(),
            'item_url': item.xpath('h2/a/@href')[0],
            'small_type': small_type,
        }
        rank_html_obj = item.xpath('div[2]/span[2]')
        if len(rank_html_obj):
            data['rank'] = rank_html_obj[0].text
        else:
            data['rank'] = -1

        regex = re.search(r'\d+', item.xpath('div[2]/span[@class="pl"]')[0].text)
        if regex:
            data['rank_num'] = regex.group()
        else:
            data['rank_num'] = 0
        item_id += 1
        lock.acquire()
        datas.append(data)
        lock.release()


if __name__ == '__main__':
    start_time = time.time()
    url = 'https://book.douban.com/tag/?view=type'  # 豆瓣图书标签
    crawl(url)
    print("--- %.2f seconds ---" % (time.time() - start_time))
