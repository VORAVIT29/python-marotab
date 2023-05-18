# import pytesseract
from function.dataStatic import *
from io import BytesIO
from PIL import Image
import easyocr
import base64
# import cv2
import os


# pytesseract.pytesseract.tesseract_cmd = f"{os.getcwd()}/function/Tesseract-OCR/tesseract.exe"


# def img_to_text(img):
#     text = pytesseract.image_to_string(img, config="--psm 6")
#     text = pytesseract.image_to_string(img)
#     return text


# def noise_img(img):
#     return cv2.medianBlur(img, 7)


# def resize(img):
#     return cv2.resize(img, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)


# def get_gayScale(img):
#     return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
#     return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


# def thresholding(img):
#     return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
#     return cv2.threshold(img, 90, 255, cv2.THRESH_BINARY)[1]


# def adaptive(img):
#     return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 41, 5)
#     return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 1)


# img = cv2.imread('mitor2.jpg', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('mitor.jpg')

# img1 = get_gayScale(img)
# img1 = adaptive(img1)
# img1 = resize(img1)
# img1 = thresholding(img1)
# img1 = noise_img(img1)


# result_text = img_to_text(img1)
# print(result_text)

# cv2.imshow('mitor', img1)
# cv2.imshow('original', img)
# cv2.waitKey(0)

class tesseract:
    result = {'status': '', 'result': None}
    img64 = None

    def __init__(self, img_patch):
        self.img64 = img_patch

    def set_data(self):
        img_split = str(self.img64).split(',')[1]
        img_bytes = base64.b64decode(img_split)
        img = Image.open(BytesIO(img_bytes))

        # Save img byte to img png
        img.save('image_process.png', 'PNG')

        reander = easyocr.Reader(['en'])
        result = reander.readtext('image_process.png')
        # font = cv2.FONT_HERSHEY_SIMPLEX

        # spacer = 100
        text_list = []
        confidence_percentage_list = 0
        for detection in result:
            text = detection[1]
            text_list.append(text)
            score = detection[2]
            confidence_percentage_list = round(score * 100, 1)

        # remove image
        os.remove("image_process.png")

        return set_result(STATUS_SUCCESS, {'texts': ''.join(text_list), 'confidences': confidence_percentage_list})
