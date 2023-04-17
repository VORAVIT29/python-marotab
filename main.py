from pytesseract import pytesseract
import pyodbc as odcbcon
from function import func, connectSQL

# main
pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
patch_img = "image\mitor2.jpg"
tar = func.ruk(patch_img)
# tar.openCaramra()
# tar.select_crop_img()

# img to text
text_mitor = tar.show_img_to_str()

# save data in SQL Server
# connect sql
sql = connectSQL.SQL('DESKTOP-R4AEEG6\SQLEXPRESS', 'testDatabase')

# query table
sql.select_query('info_mitor')

# test insert data 
# list_values = (text_mitor, 10)
# sql.insert_data('info_mitor', list_values)
