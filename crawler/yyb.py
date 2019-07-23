import requests
import json
import xlwt
import xlrd
from datetime import datetime
import crawler.excel_helper
from xlutils.copy import copy
from crawler.progress_tool import print_progress_bar
import time

# 分类ID
categorys = {
    '总榜': 0,
    '腾讯软件': -10,
    '购物': 122,
    '阅读': 102,
    '新闻': 110,
    '视频': 103,
    '旅游': 108,
    '工具': 115,
    '社交': 106,
    '音乐': 101,
    '美化': 119,
    '摄影': 104,
    '理财': 114,
    '系统': 117,
    '生活': 107,
    '出行': 112,
    '安全': 118,
    '教育': 111,
    '健康': 109,
    '娱乐': 105,
    '儿童': 100,
    '办公': 113,
    '通讯': 116,
}


def crawl():
    from_index = 0
    count = 30
    category_key = list(categorys.keys())
    print_progress_bar(0, len(category_key), prefix='Progress:', suffix='Complete', length=len(category_key))
    progress = 1
    url = "https://sj.qq.com/myapp/cate/appList.htm?orgame=1&categoryId=%d&pageSize=%d&pageContext=%d"
    for name, category_id in categorys.items():
        category_index = category_key.index(name)
        real_url = url % (category_id, count, from_index)
        resp = requests.get(real_url)
        page = resp.content
        datas = json.loads(page)
        export_excel(datas['obj'], category_index)
        time.sleep(0.1)
        print_progress_bar(progress, len(category_key), prefix='Progress:', suffix='Complete', length=len(category_key))
        progress += 1


def export_excel(datas, category_index):
    start_row_index = 1
    for data in datas:
        item = [data['appName'],
                data['authorName'],
                data['apkUrl'],
                datetime.utcfromtimestamp(data['apkPublishTime']).strftime('%Y-%m-%d'),
                data['newFeature'],
                "%.2f" % data['averageRating'],  # 四舍五入保留两位小数
                data['appRatingInfo']['ratingCount'],
                data['appDownCount'],
                ]

        rb = xlrd.open_workbook('yyb.xls', formatting_info=True)
        # 复制新打开的
        wb = copy(rb)
        sheet = wb.get_sheet(category_index)
        crawler.excel_helper.write_column(sheet, item, start_row_index)
        wb.save('yyb.xls')
        start_row_index += 1


def init_wb():
    # TODO try catch
    # TODO 设置表格宽度
    wb_title = ['应用名', '公司名称', '下载链接', '应用发布时间', '新功能说明', '平均分数', '评分人数', '下载量']
    wb = xlwt.Workbook()
    char_length = 367  # 367大约是一个字符的宽度
    for category in categorys:
        ws = wb.add_sheet(category)
        ws.col(3).width = char_length * 11
        ws.col(7).width = char_length * 10
        crawler.excel_helper.write_column(ws, wb_title, 0, 0)

    try:
        wb.save('yyb.xls')
    except PermissionError as e:
        print(str(e) + " excel 打开中，请关闭后再试")


if __name__ == '__main__':
    init_wb()
    crawl()
