# encoding: utf-8
"""
Created on 2014年7月3日

@author: Linys

All coordinates assume a screen resolution of 1280x1024, and Chrome 
maximized with the Bookmarks Toolbar enabled.
Down key has been hit 4 times to center play area in browser.
x_pad = 37
y_pad = 463
Play area =  x_pad, x_pad, x_pad+641, y_pad+481
"""

from PIL import ImageGrab, ImageOps
import os
import time
import win32api, win32con
from numpy import *


x_pad = 37
y_pad = 463

# 初始食材数量
foodOnHand = {'shrimp':5,
              'rice':10,
              'nori':10,
              'roe':10,
              'salmon':5,
              'unagi':5}

def screenGrab():
    box = (x_pad, y_pad, x_pad+641, y_pad+481)
    im = ImageGrab.grab(box)
    # im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im
    
def grab():
    box = (x_pad, y_pad, x_pad+641, y_pad+481)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    print a
    return a

# 鼠标左键
def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    # print 'Left Click'

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    # print 'Left Down'
    
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    # print 'Left Release'
    
def mousePos(cord):
    win32api.SetCursorPos((x_pad+cord[0], y_pad+cord[1]))

def getCords():
    x, y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    return x, y

# 开始游戏，跳过游戏前菜单
def startGame():
    # press Start button
    mousePos(Cord.s_start)
    leftClick()
    time.sleep(0.1)
    
    # press Continue button
    mousePos(Cord.s_continue)
    leftClick()
    time.sleep(0.1)
    
    # press Skip button
    mousePos(Cord.s_skip)
    leftClick()
    time.sleep(0.1)
    
    # press Continue button again
    mousePos(Cord.s_continue)
    leftClick()
    time.sleep(0.1)
    
# 游戏物品坐标
class Cord:
    # cords for startmenu
    s_continue = (308, 398)
    s_skip = (581, 460)
    s_start = (306, 207)
    
    # cords for food
    f_nori = (37, 398)
    f_rice = (90, 346)
    f_roe = (93, 401)
    f_salmon = (36, 453)
    f_shrimp = (32, 344)
    f_unagi = (90, 451)
    
    # cords for plants
    p_five = (481, 203)
    p_four = (383, 205)
    p_one = (78, 214)
    p_six = (585, 213)
    p_three = (280, 210)
    p_two = (180, 210)
    
    # cord for board
    b_board = (194, 407)
    
    # cord for buy
    b_diliver = (493, 305)
    b_exit = (591, 352)
    b_fishegg = (573, 287)
    b_nori = (495, 285)
    b_phone = (588, 391)
    m_rice = (539, 294)
    b_rice = (546, 283)
    b_sake = (536, 321)
    b_salmon = (488, 341)
    b_shrimp = (488, 232)
    b_topping = (526, 279)
    b_unagi = (574, 233)

# 收盘子
def clearTable():
    mousePos(Cord.p_one)
    leftClick()
    
    mousePos(Cord.p_two)
    leftClick()
    
    mousePos(Cord.p_three)
    leftClick()
    
    mousePos(Cord.p_four)
    leftClick()
    
    mousePos(Cord.p_five)
    leftClick()
    
    mousePos(Cord.p_six)
    leftClick()
    
    time.sleep(1)
    
# 烹饪寿司
def completeSushi():
    mousePos(Cord.b_board)
    leftClick()
    time.sleep(1)
    
def makeOnigiri():
    mousePos(Cord.f_rice)
    leftClick()
    time.sleep(0.1)
    leftClick()
    mousePos(Cord.f_nori)
    leftClick()
    time.sleep(0.1)
    completeSushi()
    
def makeCalRoll():
    mousePos(Cord.f_rice)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_roe)
    leftClick()
    mousePos(Cord.f_nori)
    leftClick()
    time.sleep(0.1)
    completeSushi()
    
def makeGunMaki():
    mousePos(Cord.f_rice)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_roe)
    leftClick()
    time.sleep(0.1)
    leftClick()
    mousePos(Cord.f_nori)
    leftClick()
    time.sleep(0.1)
    completeSushi()
    
def makeSalmonRoll():
    mousePos(Cord.f_rice)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_nori)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_salmon)
    leftClick()
    time.sleep(0.1)
    leftClick()
    completeSushi()
    
def makeShrimp():
    mousePos(Cord.f_rice)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_nori)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_shrimp)
    leftClick()
    time.sleep(0.1)
    leftClick()
    completeSushi()
    
def makeUnagi():
    mousePos(Cord.f_rice)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_nori)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_unagi)
    leftClick()
    time.sleep(0.1)
    leftClick()
    completeSushi()

def makeDragon():
    mousePos(Cord.f_rice)
    leftClick()
    time.sleep(0.1)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_nori)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_unagi)
    leftClick()
    time.sleep(0.1)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_roe)
    leftClick()
    time.sleep(0.1)
    completeSushi()

def makeCombo():
    mousePos(Cord.f_rice)
    leftClick()
    time.sleep(0.1)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_nori)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_unagi)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_roe)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_salmon)
    leftClick()
    time.sleep(0.1)
    mousePos(Cord.f_shrimp)
    leftClick()
    time.sleep(0.1)
    completeSushi()
    
# 食材补充    
def buyFood(food):
    '''
    (127, 127, 127) rice unavailable
    (109, 123, 127) shrimp unavailable
    (60, 29, 2) unagi unavailable
    (33, 30, 11) b_nori unavailable
    (127, 61, 0) fishegg unavailable
    (127, 71, 47) salmon unavailable
            根据该点的rgb值判断是否有钱进行购买
    '''
    if food == 'rice':
        mousePos(Cord.b_phone)
        time.sleep(0.1)
        leftClick()
        mousePos(Cord.m_rice)
        time.sleep(0.1)
        leftClick()
        time.sleep(0.1)
        s = screenGrab()
        time.sleep(0.1)
        if s.getpixel(Cord.b_rice) != (127, 127, 127):
            print str(time.ctime()) + ': ' + 'Rice is aviailable.'
            mousePos(Cord.b_rice)
            time.sleep(0.1)
            leftClick()
            mousePos(Cord.b_diliver)
            foodOnHand['rice'] += 10
            time.sleep(0.1)
            leftClick()
            time.sleep(3)
        else:
            print str(time.ctime()) + ': ' + 'Rice is NOT available.'
            mousePos(Cord.b_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)
    
    if food == 'nori':
        mousePos(Cord.b_phone)
        time.sleep(0.1)
        leftClick()
        mousePos(Cord.b_topping)
        time.sleep(0.1)
        leftClick()
        time.sleep(0.1)
        s = screenGrab()
        time.sleep(0.1)
        if s.getpixel(Cord.b_nori) != (33, 30, 11):
            print str(time.ctime()) + ': ' + 'Nori is aviailable.'
            mousePos(Cord.b_nori)
            time.sleep(0.1)
            leftClick()
            mousePos(Cord.b_diliver)
            foodOnHand['nori'] += 10
            time.sleep(0.1)
            leftClick()
            time.sleep(3)
        else:
            print str(time.ctime()) + ': ' + 'Nori is NOT available.'
            mousePos(Cord.b_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)
            
    if food == 'roe':
        mousePos(Cord.b_phone)
        time.sleep(0.1)
        leftClick()
        mousePos(Cord.b_topping)
        time.sleep(0.1)
        leftClick()
        time.sleep(0.1)
        s = screenGrab()
        time.sleep(0.1)
        if s.getpixel(Cord.b_fishegg) != (127, 61, 0):
            print str(time.ctime()) + ': ' + 'Fishegg is aviailable.'
            mousePos(Cord.b_fishegg)
            time.sleep(0.1)
            leftClick()
            mousePos(Cord.b_diliver)
            foodOnHand['roe'] += 10
            time.sleep(0.1)
            leftClick()
            time.sleep(3)
        else:
            print str(time.ctime()) + ': ' + 'Fishegg is NOT available.'
            mousePos(Cord.b_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)
            
    if food == 'salmon':
        mousePos(Cord.b_phone)
        time.sleep(0.1)
        leftClick()
        mousePos(Cord.b_topping)
        time.sleep(0.1)
        leftClick()
        time.sleep(0.1)
        s = screenGrab()
        time.sleep(0.1)
        if s.getpixel(Cord.b_salmon) != (127, 71, 47):
            print str(time.ctime()) + ': ' + 'Salmon is aviailable.'
            mousePos(Cord.b_salmon)
            time.sleep(0.1)
            leftClick()
            mousePos(Cord.b_diliver)
            foodOnHand['salmon'] += 5
            time.sleep(0.1)
            leftClick()
            time.sleep(3)
        else:
            print str(time.ctime()) + ': ' + 'Salmon is NOT available.'
            mousePos(Cord.b_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)
            
    if food == 'shrimp':
        mousePos(Cord.b_phone)
        time.sleep(0.1)
        leftClick()
        mousePos(Cord.b_topping)
        time.sleep(0.1)
        leftClick()
        time.sleep(0.1)
        s = screenGrab()
        time.sleep(0.1)
        if s.getpixel(Cord.b_shrimp) != (109, 123, 127):
            print str(time.ctime()) + ': ' + 'Shrimp is aviailable.'
            mousePos(Cord.b_shrimp)
            time.sleep(0.1)
            leftClick()
            mousePos(Cord.b_diliver)
            foodOnHand['shrimp'] += 5
            time.sleep(0.1)
            leftClick()
            time.sleep(3)
        else:
            print str(time.ctime()) + ': ' + 'Shrimp is NOT available.'
            mousePos(Cord.b_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)
            
    if food == 'unagi':
        mousePos(Cord.b_phone)
        time.sleep(0.1)
        leftClick()
        mousePos(Cord.b_topping)
        time.sleep(0.1)
        leftClick()
        time.sleep(0.1)
        s = screenGrab()
        time.sleep(0.1)
        if s.getpixel(Cord.b_unagi) != (60, 29, 2):
            print str(time.ctime()) + ': ' + 'Unagi is aviailable.'
            mousePos(Cord.b_unagi)
            time.sleep(0.1)
            leftClick()
            mousePos(Cord.b_diliver)
            foodOnHand['unagi'] += 5
            time.sleep(0.1)
            leftClick()
            time.sleep(3)
        else:
            print str(time.ctime()) + ': ' + 'Unagi is NOT available.'
            mousePos(Cord.b_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)

# 制作食物
def makeFood(food):
    if food == 'onigiri':
        makeOnigiri()
        foodOnHand['rice'] -= 2
        foodOnHand['nori'] -= 1
    if food == 'caliroll':
        makeCalRoll()
        foodOnHand['rice'] -= 1
        foodOnHand['nori'] -= 1
        foodOnHand['roe'] -= 1
    if food == 'gunmaki':
        makeGunMaki()
        foodOnHand['rice'] -= 1
        foodOnHand['nori'] -= 1
        foodOnHand['roe'] -= 2
    if food == 'salmonroll':
        makeSalmonRoll()
        foodOnHand['rice'] -= 1
        foodOnHand['nori'] -= 1
        foodOnHand['salmon'] -= 2
    if food == 'shrimp':
        makeShrimp()
        foodOnHand['rice'] -= 1
        foodOnHand['nori'] -= 1
        foodOnHand['shrimp'] -= 2
    if food == 'unagi':
        makeUnagi()
        foodOnHand['rice'] -= 1
        foodOnHand['nori'] -= 1
        foodOnHand['unagi'] -= 2
    if food == 'dragon':
        makeDragon()
        foodOnHand['rice'] -= 2
        foodOnHand['nori'] -= 1
        foodOnHand['roe'] -= 1
        foodOnHand['unagi'] -= 2
    if food == 'combo':
        makeCombo()
        foodOnHand['rice'] -= 2
        foodOnHand['nori'] -= 1
        foodOnHand['roe'] -= 1
        foodOnHand['unagi'] -= 1
        foodOnHand['shrimp'] -= 1
        foodOnHand['salmon'] -= 1
        
# 判断食材剩余数量，进行补充        
def checkFood():
    for i, j in foodOnHand.items():
        if i == 'nori' or i == 'rice' or i == 'roe':
            # print i,foodOnHand[i]
            if j <= 3:
                print str(time.ctime()) + ': ' + '{} count is {} need to be restored.'.format(i.title(), foodOnHand[i])
                buyFood(i)
        if i == 'salmon' or i == 'shrimp' or i == 'unagi':
            if j <= 2:
                print str(time.ctime()) + ': ' + '{} count is {} need to be restored.'.format(i.title(), foodOnHand[i])
                buyFood(i)
            
    
def get_seat_one():
    x, y = 27+x_pad, 62+y_pad
    box = (x, y, x+63, y+16)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

def get_seat_two():
    x, y = 128+x_pad, 62+y_pad
    box = (x, y, x+63, y+16)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

def get_seat_three():
    x, y = 229+x_pad, 62+y_pad
    box = (x, y, x+63, y+16)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

def get_seat_four():
    x, y = 330+x_pad, 62+y_pad
    box = (x, y, x+63, y+16)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

def get_seat_five():
    x, y = 431+x_pad, 62+y_pad
    box = (x, y, x+63, y+16)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

def get_seat_six():
    x, y = 532+x_pad, 62+y_pad
    box = (x, y, x+63, y+16)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

def get_result():
    box = (205+x_pad, 116+y_pad, 447+x_pad, 153+y_pad)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

def get_day_final():
    box = (180+x_pad, 361+y_pad, 465+x_pad, 395+y_pad)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a
    

def get_all_seats():
    get_seat_one()
    get_seat_two()
    get_seat_three()
    get_seat_four()
    get_seat_five()
    get_seat_six()
    
# 一天营业后重置食材数量
def resetFoodOnHand():
    global foodOnHand
    print str(time.ctime()) + ': ' + 'ResetFoodOnHand'
    foodOnHand = {'shrimp':5,
              'rice':10,
              'nori':10,
              'roe':10,
              'salmon':5,
              'unagi':5}
    
    
# 判断是否为空位
class Sushi:
    seat_1 = 8119
    seat_2 = 5986
    seat_3 = 11598
    seat_4 = 10532
    seat_5 = 6782
    seat_6 = 9041
    result = 9406
    day_final = 10860

# 个寿司的类型对应字典    
sushiTypes = {2670:'onigiri', 
              3143:'caliroll',
              2677:'gunmaki',
              2474:'salmonroll',
              2921:'shrimp',
              2893:'unagi',
              3307:'dragon',
              4159:'combo'
              }
# 主循环体    
def check_bubs():
    
    clearTable()
    checkFood()
    
    s1 = get_seat_one()
    if s1 != Sushi.seat_1:
        if sushiTypes.has_key(s1):
            print str(time.ctime()) + ': ' + 'Table 1 needs {}.'.format(sushiTypes[s1].title())
            makeFood(sushiTypes[s1])
        else:
            print str(time.ctime()) + ': ' + 'Sushi not found.'
    else:
        print str(time.ctime()) + ': ' + 'Table 1 is empty.'
        
    checkFood()
    
    s2 = get_seat_two()
    if s2 != Sushi.seat_2:
        if sushiTypes.has_key(s2):
            print str(time.ctime()) + ': ' + 'Table 2 needs {}.'.format(sushiTypes[s2].title())
            makeFood(sushiTypes[s2])
        else:
            print str(time.ctime()) + ': ' + 'Sushi not found.'
    else:
        print str(time.ctime()) + ': ' + 'Table 2 is empty.'
        
    clearTable()
    checkFood()
     
    s3 = get_seat_three()
    if s3 != Sushi.seat_3:
        if sushiTypes.has_key(s3):
            print str(time.ctime()) + ': ' + 'Table 3 needs {}.'.format(sushiTypes[s3].title())
            makeFood(sushiTypes[s3])
        else:
            print str(time.ctime()) + ': ' + 'Sushi not found.'
    else:
        print str(time.ctime()) + ': ' + 'Table 3 is empty.'
        
    checkFood()
    
    s4 = get_seat_four()
    if s4 != Sushi.seat_4:
        if sushiTypes.has_key(s4):
            print str(time.ctime()) + ': ' + 'Table 4 needs {}.'.format(sushiTypes[s4].title())
            makeFood(sushiTypes[s4])
        else:
            print str(time.ctime()) + ': ' + 'Sushi not found.'
    else:
        print str(time.ctime()) + ': ' + 'Table 4 is empty.'

    clearTable()
    checkFood()
     
    s5 = get_seat_five()
    if s5 != Sushi.seat_5:
        if sushiTypes.has_key(s5):
            print str(time.ctime()) + ': ' + 'Table 5 needs {}.'.format(sushiTypes[s5].title())
            makeFood(sushiTypes[s5])
        else:
            print str(time.ctime()) + ': ' + 'Sushi not found.'
    else:
        print str(time.ctime()) + ': ' + 'Table 5 is empty.'
        
    checkFood()
     
    s6 = get_seat_six()
    if s6 != Sushi.seat_6:
        if sushiTypes.has_key(s6):
            print str(time.ctime()) + ': ' + 'Table 6 needs {}.'.format(sushiTypes[s6].title())
            makeFood(sushiTypes[s6])
        else:
            print str(time.ctime()) + ': ' + 'Sushi not found.'
    else:
        print str(time.ctime()) + ': ' + 'Table 6 is empty.'
        
    final = get_day_final()
    if final == Sushi.day_final:
        print str(time.ctime()) + ': ' + 'Day end. Get result.'
        result = get_result()
        if result == Sushi.result:
            print str(time.ctime()) + ': ' + 'You win, continue.'
            mousePos(Cord.s_continue)
            leftClick()
            time.sleep(0.1)
            leftClick()
            resetFoodOnHand()
        else:
            print str(time.ctime()) + ': ' + 'You fail.'
            return False
    else:
        print str(time.ctime()) + ': ' + 'Not end, continue server.'
    
    print '='*70
    
            
        
    
def main():
    startGame()
    while 1:
        check_bubs()
    
if __name__ == '__main__':
    main()