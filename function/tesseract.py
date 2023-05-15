# import pytesseract
# import cv2
# import os

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


# # result_text = img_to_text(img1)
# # print(result_text)

# cv2.imshow('mitor', img1)
# cv2.imshow('original', img)
# cv2.waitKey(0)

import easyocr
import cv2


# from matplotlib import pyplot as plt


class tesseract:
    img = None

    def __init__(self, img_patch):
        img = img_patch

    def set_data(self):
        reander = easyocr.Reader(['en'])
        result = reander.readtext("miter.jpg")
        font = cv2.FONT_HERSHEY_SIMPLEX

        spacer = 100
        text_list = []
        for detection in result:
            top_left = tuple(detection[0][0])
            bottom_right = tuple(detection[0][2])
            text = detection[1]
            text_list.append(text)
            img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 3)
            img = cv2.putText(img, text, (20, spacer), font,
                              0.5, (255, 45, 0), 2, cv2.LINE_AA)
            spacer += 15

            # plt.imshow(img)
            # plt.show()

            # plt.imshow(imgOrg)
            # plt.show()

            # text_list
