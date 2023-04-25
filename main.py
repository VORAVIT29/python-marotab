import json

from pytesseract import pytesseract
import pyodbc as odcbcon
import random
from function import func, connectSQL

# main
# pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# SQL Local
# sql = connectSQL.SQL('DESKTOP-R4AEEG6\SQLEXPRESS', 'testDatabase')
# SQL Server
sql = connectSQL.SQL('35.240.177.233', 'marotabBeta')
num = '2'
tempTarget = '{"username":"user' + num + '","password":"pass' + num + '","admin_password":"adminPass' + num + '","name_host":"name' + num + '","last_name":"last' + num + '","email":"email' + num + '@email.com","phone_number":"09123456789"}'
print(tempTarget)
json_temp = json.loads(tempTarget)
for field in json_temp:
    print(json_temp[field])
# while True:
#     tar = func.ruk()
#     tar.openCaramra()
#     tar.select_crop_img()
#     # img to text
#     text_mitor = tar.show_img_to_str()

#     # test insert data
#     if len(text_mitor) > 0:
#         # connect sql
#         sql = connectSQL.SQL('DESKTOP-R4AEEG6\SQLEXPRESS', 'testDatabase')
#         # query table
#         sql.select_query('info_mitor')
#         # insert data
#         random_age = random.randint(0, 100)
#         list_values = (text_mitor.replace('\n', ''), random_age)
#         sql.insert_data('info_mitor', list_values)
#         break

#     else:
#         print('รูปไม่ชัดการุณากลับไปถ่ายรูปใหม่.....')
