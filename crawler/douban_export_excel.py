import xlwt


def export_excel(datas):
    # 目前先简单将数据导表
    # TODO 根据定义顺序生成
    # TODO 根据small_type生成新标签页
    titles = ["id", "name", "author", "item_url", "small_type", "rank", "rank_num"]
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')
    write_column(ws, titles)

    start_row_index = 1
    for item_data in datas:
        write_column(ws, item_data.values(), start_row_index)
        start_row_index += 1
    try:
        wb.save('test.xls')
    except PermissionError as e:
        print(e + " excel 打开中，请关闭后再试")


# ws 一张工作表
# list 数据列表
# from_index 从列的哪一个index开始
def write_column(work_sheet, column_datas, row_index=0, from_index=0):
    column_indx = from_index
    for item in column_datas:
        work_sheet.write(row_index, column_indx, item)
        column_indx += 1


# ws 一张工作表
# list 数据列表
# from_index 从行的哪一个index开始
def write_row(work_sheet, row_datas, column_index=0, from_index=0):
    row_index = from_index
    for item in row_datas:
        work_sheet.write(row_index, column_index, item)
        row_index += 1
