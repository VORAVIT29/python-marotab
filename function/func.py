import cv2
from PIL import Image
from pytesseract import pytesseract


class ruk:
    path_img = None
    patch_crop = None

    def __init__(self, patch):
        self.path_img = patch
        self.patch_crop = 'croptest.png'

    # ---- function open Camera ----
    def openCaramra(self):
        print("Please waiting Open Camera....")
        camera = cv2.VideoCapture(0)

        while True:
            _, image = camera.read()
            cv2.imshow('Text detection', image)
            # กด s เพื่อ save รูป
            if cv2.waitKey(1) & 0xFF == ord('s'):
                cv2.imwrite('croptest.png', image)
                break

        camera.release()
        cv2.destroyAllWindows()

    # ---- function img to string ----
    def show_img_to_str(self):
        img_row = cv2.imread(self.patch_crop)
        img_row = cv2.cvtColor(img_row, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('Result', img_row)
        img_to_str = pytesseract.image_to_string(img_row)
        print(f'Text => {img_to_str}')
        return img_to_str
        # cv2.waitKey(0)

    # ---- function select crop img ----
    def select_crop_img(self):
        img_row = cv2.imread(self.patch_crop)
        img_pos = cv2.selectROI(img_row)
        print('image pos : ', img_pos)

        pos_crop = img_row[
            int(img_pos[1]): int(img_pos[1] + img_pos[3]),
            int(img_pos[0]): int(img_pos[0] + img_pos[2])
        ]
        # save crop img
        cv2.imwrite('croptest.png', pos_crop)
        cv2.destroyAllWindows()
