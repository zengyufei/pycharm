import win32api
import win32gui
import win32process

import win32con

# 根据类名及标题名查询句柄，
hwnd = win32gui.FindWindow("WeChatMainWndForPC", "微信")
hreadID, processID = win32process.GetWindowThreadProcessId(hwnd)

print(hwnd)
print(hreadID)
print(processID)

# 没有直接修改窗口大小的方式，但可以曲线救国，几个参数分别表示句柄,起始点坐标,宽高度,是否重绘界面 ，如果想改变窗口大小，就必须指定起始点的坐标，没果对起始点坐标没有要求，随便写就可以；如果还想要放在原先的位置，就需要先获取之前的边框位置，再调用该方法即可
# win32gui.MoveWindow(hwnd, 150, 150, 768, 768, True)

# 指定句柄设置为前台，也就是激活
win32gui.SetForegroundWindow(hwnd)
# 设置为后台
win32gui.SetBkMode(hwnd, win32con.TRANSPARENT)

