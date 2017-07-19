import xlrd
from Pedestrian import Pedestrian


def open_file(file_path):
    pedestrians = []
    book = xlrd.open_workbook(file_path)
    sheet = book.sheet_by_index(0)
    col_num = sheet.ncols
    row_num = sheet.nrows
    for col in range(1, col_num):
        a = Pedestrian()
        for row in range(1, row_num):
            a.add_info((round(sheet.cell(row, 0).value, 2), sheet.cell(row, col).value))
        pedestrians.append(a)
    return pedestrians

# file_path = "F:\data set\数据\跟随.xlsx"
# leader_status = {}
# follower_status = {}
# open_file(file_path, leader_status, follower_status)
