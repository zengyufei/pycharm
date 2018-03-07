# -*- coding: UTF-8 -*_
import PIL.ImageOps
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'd:/soft/Tesseract-OCR/tesseract'

def initTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

'''
①不要盲目的去直接用代码识别，识别不出来就怀疑代码有问题或者 pytesseract 不好用：
    先将验证码用图片处理工具处理，一步步得到理想图片，记住处理过程，将处理后的图片直接用 pytesseract 识别，代码如下：
'''

im = Image.open('D:/dowork/pyCharm/网上随手抓代码/别人的验证码识别/aaa.png')
# 图片的处理过程
im = im.convert('L')
binaryImage = im.point(initTable(), '1')
im1 = binaryImage.convert('L')
im2 = PIL.ImageOps.invert(im1)
im3 = im2.convert('1')
im4 = im3.convert('L')
#将图片中字符裁剪保留
box = (30,10,90,28)
region = im4.crop(box)

# 测试两种结果
# 将图片字符放大 一点
out1 = region.resize((120, 38))
# 将图片字符放大 再放大一点
out2 = region.resize((240, 76))

outImg1 = pytesseract.image_to_string(out1)
print(outImg1)
out1.show()

outImg2 = pytesseract.image_to_string(out2)
print(outImg2)
out2.show()
