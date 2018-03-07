# -*- coding: UTF-8 -*-

# 找茬
import cv2
from PIL import ImageChops
from PIL import ImageGrab
from PIL import Image
import numpy as np

tu1 = cv2.imread("test1.jpg")
tu2 = cv2.imread("test2.jpg")
img1 = cv2.imread("out.jpg")

img1 = cv2.medianBlur(img1, 3)

hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

##lower=np.array([25,25,25], dtype=np.uint8)
##upper=np.array([255,255,255], dtype=np.uint8)
##mask=cv2.inRange(img1,lower,upper)
lower_blue = np.array([0, 0, 0], dtype=np.uint8)
upper_blue = np.array([255, 255, 30], dtype=np.uint8)
mask = cv2.inRange(hsv, lower_blue, upper_blue)
# 根据阈值构建掩模
kernel = np.ones((1, 1), np.uint8)
mask_img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
list_cnt = []
for cnt in contours:
    area = cv2.contourArea(cnt)
    list_cnt.append({"area": area, "cnt": cnt})
list_cnt.sort(key=lambda obj: obj.get('area'), reverse=True)
index = 0
for i in range(len(list_cnt)):
    x, y, w, h = cv2.boundingRect(list_cnt[i]['cnt'])
    if i < 5:
        dst = cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 0, 0), 2)
    else:
        dst = cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 255, 0), 2)



cv2.imshow('img1', tu1)
cv2.imshow('img', tu2)
cv2.imshow('dst', img1)
cv2.waitKey(0)



