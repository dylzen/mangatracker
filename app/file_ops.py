from json.tool import main
import os
from openpyxl import load_workbook

def load_book():
    path_test = os.path.join(os.path.expanduser('~'), 'coding', 'files', 'Manga Collection 2021.xlsx')
    workBook = load_workbook(path_test, read_only=False)
    return path_test, workBook

def get_titles(user_input):
    if user_input == 'a':
        col = 26
        print("You chose AC")
    else:
        col = 25  
        print("You chose MAL")
    path_test, book = load_book()
    sheet = book['auto']
    mangalist = []
    for row in sheet.iter_rows(min_row=2, min_col=col): ## colonna 25=Y, MAL link
        mangalist.append(row[0].value)
    return mangalist

# def get_titles_ac():
#     path_test, book = load_book()
#     sheet = book['auto']
#     mangalist = []
#     for row in sheet.iter_rows(min_row=2, min_col=26): ## colonna 26=Z, AC link
#         mangalist.append(row[0].value)
#     return mangalist