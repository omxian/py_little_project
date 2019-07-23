

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
