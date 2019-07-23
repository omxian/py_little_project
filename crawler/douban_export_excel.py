import xlwt
import crawler.excel_helper


def export_excel(datas):
    # 目前先简单将数据导表
    # TODO 根据定义顺序生成
    # TODO 根据small_type生成新标签页
    titles = ["id", "name", "author", "item_url", "small_type", "rank", "rank_num"]
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')
    crawler.excel_helper.write_column(ws, titles)

    start_row_index = 1
    for item_data in datas:
        crawler.excel_helper.write_column(ws, item_data.values(), start_row_index)
        start_row_index += 1
    try:
        wb.save('test.xls')
    except PermissionError as e:
        print(str(e) + " excel 打开中，请关闭后再试")
