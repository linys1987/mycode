# encoding: utf-8
# version: 1.0
# author: linys1987@gmail.com

import os
import time
from PIL import ImageGrab
import win32api, win32con

# 定义浮标的getpixel数值
PIXELNUM = (230, 59, 56)
# 定义矩形截图大小
BOXSIZE = 50

def screenGrab():
    '''全屏截图'''
    im = ImageGrab.grab()
    # im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    print time.ctime() + ': '+ '截图完成'
    return im

def getCoords(img):
    '''获取浮标坐标'''
    w, h = img.size
    for i in range(w):
        for j in range(h):
            if img.getpixel((i, j)) == PIXELNUM:
                print time.ctime() + ': '+ '获取到浮标坐标为', i, j
                return (i, j)
    print '无法获取浮标坐标.'
    return False

def boxGrab(cord):
    '''获取浮标坐标周围500像素矩形截图'''
    x, y = cord
    box = (x-BOXSIZE, y-BOXSIZE, x+BOXSIZE, y+BOXSIZE)
    im = ImageGrab.grab(box)
    # im.save(os.getcwd() + '\\box_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im

def isBait(img):
    '''判断鱼是否上钩'''
    w, h = img.size
    for i in range(w):
        for j in range(h):
            if img.getpixel((i, j)) == PIXELNUM:
                if abs(j-50) > 10:
                    print time.ctime() + ': '+ '监测到浮标位置移动, 右键收杆.'
                    return True
    print time.ctime() + ': '+ '浮标未动, 没有鱼上钩.'
    return False

def rightClick():
    '''鼠标右键点击'''
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
    
def mousePos(cord):
    '''鼠标指针位置'''
    win32api.SetCursorPos(cord)
    
def startFish():
    win32api.keybd_event(70, 0, 0, 0)
    time.sleep(0.02)
    win32api.keybd_event(70, 0, win32con.KEYEVENTF_KEYUP, 0)

def main():
    while True:
        # 下钩钓鱼
        # startFish()
        time.sleep(2)
        # 获取屏幕截图
        full_img = screenGrab()
        # 获取浮标位置
        buoy_pos = getCoords(full_img)
        # 判断是否上钩
        starttime = time.time()
        if buoy_pos:
            while True:
                box_img = boxGrab(buoy_pos)
                if isBait(box_img):
                    mousePos(buoy_pos)
                    rightClick()
                    break
                # 超过钓鱼时间, 重新下杆.
                if (time.time() - starttime) > 20:
                    print time.ctime() + ': '+ '超过钓鱼时间, 重新下杆.'
                    break
                # time.sleep(0.5)
        else:
            print time.ctime() + ': '+ '无法获取浮标位置, 重新下杆.'
            
if __name__ == '__main__':
    main()