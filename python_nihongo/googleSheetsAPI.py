# run the program via this module!
# what this program will do:
# go into the words i havent learned subsheet
# sift through and add the words from selenium into the bottom

from seleniumFun import *
import gspread
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials

def insert_to_spreadsheet(my_data):
    line_number = len(data) + 2

    for vocab in my_data:
        kanji = vocab.get_kanji()
        hiragana = vocab.get_hiragana()
        meaning = vocab.get_meaning()
        # print(f"appending data {kanji}, {hiragana} to sheet")
        sheet.insert_row([kanji, hiragana, meaning], line_number)
        line_number += 1

# global variables***
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("./creds.json", scope)
client = gspread.authorize(creds)
# for troubleshooting, use the tutorial sheet
sheet = client.open("tutorial").get_worksheet(1)
# sheet = client.open("Japanese_Study").get_worksheet(1)
data = sheet.get_all_records()

insert_to_spreadsheet(words_for_excel)
print("all done!")