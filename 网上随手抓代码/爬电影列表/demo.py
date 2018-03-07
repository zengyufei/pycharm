# import CustomMysql

# mysql = CustomMysql.Mysql("127.0.0.1", 3306, "root", "root", "dy", "utf8")
# record = mysql.get("select * from bean where title like '%模仿游戏%'")
# print(record)


import base64
from io import BytesIO

import requests
from PIL import Image


def imgToBase64(imgSrc):
    response = requests.get(imgSrc)  # 将这个图片保存在内存
    # 将这个图片从内存中打开，然后就可以用Image的方法进行操作了
    image = Image.open(BytesIO(response.content))
    # 得到这个图片的base64编码
    ls_f = base64.b64encode(BytesIO(response.content).read())
    # 打印出这个base64编码
    print(ls_f)

imgToBase64("https://img.aolusb.com/im/201803/20183292822761.jpg")