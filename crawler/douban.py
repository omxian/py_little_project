import requests
import crawler.douban_export_excel
from lxml import html
import re

datas = []
item_id = 1


# TODO 添加一些GUI的展示
def crawl(origin_url):
    resp = requests.get(origin_url)
    page = resp.content
    root = html.fromstring(page)
    contents = root.xpath('//*[@id="content"]/div/div[1]/div[2]/div/table/tbody/tr/td/a')
    for content in contents:
        # TODO 这里可以做一波优化，启动多线程爬
        handle_item_list(content.text)

    crawler.douban_export_excel.export_excel(datas)


def handle_item_list(small_type):
    # TODO 此处只拉取了类目的前20条，可以修改分页代码拉取更多信息
    item_list_url = 'https://book.douban.com/tag/' + small_type + '?start=0&type=T'
    resp = requests.get(item_list_url)
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
        datas.append(data)


if __name__ == '__main__':
    url = 'https://book.douban.com/tag/?view=type'  # 豆瓣图书标签
    crawl(url)
