# encoding: utf-8
'''
Created on 2014年7月3日

@author: Linys
'''

from PIL import ImageGrab
import os
import time

x_pad = 37
y_pad = 463

def screenGrab():
    box = (x_pad, y_pad, x_pad+641, y_pad+481)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    
def main():
    screenGrab()
    
if __name__ == '__main__':
    main()
