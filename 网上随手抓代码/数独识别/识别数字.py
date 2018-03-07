# -*- coding: UTF-8 -*-
# @url https://mp.weixin.qq.com/s?__biz=MzU2MDAyNzk5MA==&mid=2247483695&idx=1&sn=e6068895b92749da4cf43c0ef7e87ed8&chksm=fc0f0116cb78880042081292735c468d1bbae57afb3e998468667d39a15a3bee7b1ebe7d9aa7#rd
import cv2

img = cv2.imread('shudu.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
## 阈值分割
ret, thresh = cv2.threshold(gray, 200, 255, 1)
## 对二值图像执行膨胀操作
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5, 5))
dilated = cv2.dilate(thresh, kernel)

## 轮廓提取，cv2.RETR_TREE表示建立层级结构
image, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
#cv2.drawContours(img,contours,5,(0,255,0),3)
print (type(contours))
print (type(contours[0]))
print (len(contours))

print (type(hierarchy))
print (type(hierarchy[0]))
print (len(hierarchy))

## 提取小方格，其父轮廓都为0号轮廓
boxes = []
for i in range(len(hierarchy[0])):
    if hierarchy[0][i][3] == 0:
        boxes.append(hierarchy[0][i])

print(boxes)
print(boxes[0])
print(contours[boxes[1][2]])
x, y, w, h = cv2.boundingRect(contours[boxes[1][2]])
img = cv2.rectangle(img, (x - 1, y - 1), (x + w + 1, y + h + 1), (0, 0, 255), 2)
## 提取数字，其父轮廓都存在子轮廓
number_boxes = []
for j in range(len(boxes)):
    if boxes[j][2] != -1:
        # number_boxes.append(boxes[j])
        x, y, w, h = cv2.boundingRect(contours[boxes[j][2]])
        number_boxes.append([x, y, w, h])
        #cv2.drawContours(img, contours[boxes[j][2]], -1, (0, 0, 255), 3)
        #img = cv2.rectangle(img, (x - 1, y - 1), (x + w + 1, y + h + 1), (0, 0, 255), 2)

cv2.namedWindow("img", cv2.WINDOW_NORMAL);
cv2.imshow("img", img)
cv2.waitKey(0)


