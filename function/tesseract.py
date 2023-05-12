import cv2
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = f"{os.getcwd()}/function/Tesseract-OCR/tesseract.exe"


def img_to_text(img):
    text = pytesseract.image_to_string(img)
    return text


def noise_img(img):
    return cv2.medianBlur(img, 5)


def get_gayScale(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)


def thresholding(img):
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


img = cv2.imread('croptest.png', cv2.IMREAD_GRAYSCALE)
img = get_gayScale(img)
# img = thresholding(img)
img = noise_img(img)
cv2.imshow('test', img)
cv2.waitKey(0)
img = img_to_text(img)
print(img)
