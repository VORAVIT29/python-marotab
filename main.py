from pytesseract import pytesseract
import pyodbc as odcbcon
import random
from function import func, connectSQL

# main
pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# connect sql
sql = connectSQL.SQL('DESKTOP-R4AEEG6\SQLEXPRESS', 'testDatabase')

while True:
    tar = func.ruk()
    tar.openCaramra()
    tar.select_crop_img()
    # img to text
    text_mitor = tar.show_img_to_str()

    # test insert data
    if len(text_mitor) > 0:
        # query table
        sql.select_query('info_mitor')
        # insert data
        random_age = random.randint(0, 100)
        list_values = (text_mitor.replace('\n', ''), random_age)
        sql.insert_data('info_mitor', list_values)

        break
    else:
        print('รูปไม่ชัดการุณากลับไปถ่ายรูปใหม่.....')
