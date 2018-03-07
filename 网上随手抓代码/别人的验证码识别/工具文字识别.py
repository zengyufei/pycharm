# -*- coding: UTF-8 -*-、
import sys

import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'd:/soft/Tesseract-OCR/tesseract'

im = Image.open('D:/dowork/pyCharm/网上随手抓代码/别人的验证码识别/0249.jpg')
aa = pytesseract.image_to_string(im)
print(aa)

im = Image.open('D:/dowork/pyCharm/网上随手抓代码/别人的验证码识别/3061.jpg')
aa = pytesseract.image_to_string(im)
print(aa)
