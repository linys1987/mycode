# encoding: utf-8
# create 2014年7月17日
# filename: stockmon.py
# version: 1.0
# author: linys1987@gmail.com

'''从http://hq.sinajs.cn/list=CODE接口获取股票交易信息,
CODE样式:
sz300245 sz代表深交所股票, sh代表上交所股票
返回样式:
var hq_str_sz300245="天玑科技,24.370,24.410,25.090,25.850,24.000,25.090,25.100,
7949694,200025645.950,42785,25.090,26000,25.080,1800,25.070,3200,25.060,37481,
25.050,12600,25.100,2200,25.130,10900,25.150,12000,25.160,1600,25.180,2014-07-11,15:05:50,00";
0:股票名字
1:今日开盘价
2:昨日收盘价
3:当前价格
4:今日最高价
5:今日最低价
6:竞买价即'买一'报价
7:竞卖价即'卖一'报价
8:成交的股票数,由于股票交易以一百股为基本单位,所以在使用时,通常把该值除以一百
9:成交金额,单位为'元',为了一目了然,通常以'万元'为成交金额的单位,所以通常把该值除以一万
10:'买一'股数
11:'买一'报价
12:'买二'股数
13:'买二'报价
14:'买三'股数
15:'买三'报价
16:'买四'股数
17:'买四'报价
18:'买五'股数
19:'买五'报价
20:'卖一'股数
21:'卖一'报价
22:'卖二'股数
23:'卖二'报价
24:'卖三'股数
25:'卖三'报价
26:'卖四'股数
27:'卖四'报价
28:'卖五'股数
29:'卖五'报价
30:日期
31:时间
'''
import sys
import time
import os
import urllib2
import re
import ctypes
import requests


# 定义刷新频率
REFESH = 3

# 获取股票URL
def get_url():
    code = sys.argv[1]
    url = r'http://hq.sinajs.cn/list=' + code
    return url

def match_result(url):
    try:
        f = urllib2.urlopen(url, timeout=REFESH)
    except:
        print 'Get Stock Info Error, try again in %d seconds.' % (REFESH)
        return False
    re_str = r'var hq_str_\w\w(\d+)="(.*)";\n'
    text = f.read()
    match_result = re.search(re_str, text)
    data = match_result.group(2).split(',')
    data.append(match_result.group(1))
    return data

def format_output(data):
    '''
    格式化输出
    '''
    stock_code = data[-1]
    stock_name = data[0]
    # price_open = data[1]
    price_yestday = float(data[2])
    price_now = float(data[3])
    # price_high = data[4]
    # price_low = data[5]
    # stocks_traded = data[8]
    # stocks_traded_value = data[9]
    # buy_1_num = data[10]
    # buy_1_value = data[11]
    # buy_2_num = data[12]
    # buy_2_value = data[13]
    # buy_3_num = data[14]
    # buy_3_value = data[15]
    # buy_4_num = data[16]
    # buy_4_value = data[17]
    # buy_5_num = data[18]
    # buy_5_value = data[19]
    # sell_1_num = data[20]
    # sell_1_value = data[21]
    # sell_2_num = data[22]
    # sell_2_value = data[23]
    # sell_3_num = data[24]
    # sell_3_value = data[25]
    # sell_4_num = data[26]
    # sell_4_value = data[27]
    # sell_5_num = data[28]
    # sell_5_value = data[29]
    date_now = data[30]
    time_now = data[31]
    change_pencent = round(abs(price_now-price_yestday)/price_yestday, 4)*100
    return change_pencent, price_now, stock_name, stock_code, price_yestday, date_now, time_now

def color_text(color):
    '''
    定义输出的颜色
    for more information see http://msdn.microsoft.com/en-us/library/windows/desktop/ms686047(v=vs.85).aspx
    '''
    if color == 'red':
        return ctypes.windll.Kernel32.SetConsoleTextAttribute(7, 4)
    if color == 'green':
        return ctypes.windll.Kernel32.SetConsoleTextAttribute(7, 2)
    if color == 'reset':
        return ctypes.windll.Kernel32.SetConsoleTextAttribute(7, 8)

def carriage_return():
    sys.stdout.write('\r')
    sys.stdout.flush()

# 飞信短信接口
def send_msg(msg):
    '''使用飞信短信接口发送股票信息'''
    url_space_login = 'http://f.10086.cn/huc/user/space/login.do?m=submit&fr=space'
    url_login = 'http://f.10086.cn/im/login/cklogin.action'
    url_sendmsg = 'http://f.10086.cn/im/user/sendMsgToMyselfs.action'
    parameter= { 'mobilenum':'PHONENUMBER', 'password':'PASSWORD'}
 
    session = requests.Session()
    session.post(url_space_login, data = parameter)
    session.get(url_login)
    session.post(url_sendmsg, data = {'msg':msg})

# 判断是否交易时间
def is_trade():
    def is_weekday():
        weekday = time.strftime('%w')
        if weekday in ['1', '2', '3', '4', '5']:
            return True
        return False
    def is_trade_time():
        now = time.strftime('%H%M')
        if 930 < int(now) < 1130 or 1300 < int(now) < 1500:
            return True
        else:
            return False
    if is_weekday():
        if is_trade_time():
            return True
    return False

def main():
    # 初始化窗口大小
    os.system('mode con: cols=45 lines=5')

    # 短信发送标记
    msgsent = False
    change_pencent_previous = 0

    if len(sys.argv) < 2:
        print 'Add stock code like "python stock.py sz300245"'
        return False
    else:
        url = get_url()

    # 获取股票信息并输出及产生短信提示.
    while True:
        data = match_result(url)

        if data:
            change_pencent, price_now, stock_name, stock_code, price_yestday, date_now, time_now = format_output(data)
            ctypes.windll.kernel32.SetConsoleTitleA(stock_name+' '+str(price_now))  # @UndefinedVariable

            # 格式化输出,待优化
            print '='*44
            color = ''
            if price_now < price_yestday:
                color = 'green'
            elif price_now > price_yestday:
                color = 'red'
            else:
                color = 'reset'
            color_text('reset')
            print 'Stock Name: ' + stock_name + '\t' + 'Stock Code: ' + stock_code
            print 'Price  Now: ',
            color_text(color)
            print str(price_now) + '\t',
            color_text('reset')
            print 'Change Per: ',
            color_text(color)
            print str(change_pencent) + '%'
            color_text('reset')
            print '='*44
            for i in range(REFESH, 0, -1):
                print 'Wait %d seconds to refesh.' % (i),
                carriage_return()
                time.sleep(1)
            os.system('cls' if sys.platform == 'nt' else 'clear')

            # 当涨跌幅度变化大于value时, 发送短信息
            if abs(change_pencent_previous - change_pencent) > 0.5:
                msgsent = False

            # 发送短信息内容
            if is_trade():
                if change_pencent > 1 and not msgsent:
                    if color == 'red':
                        msg = 'The price of {} rise to {}%, the price now is {} {} {}.'.format(stock_code, change_pencent, price_now, date_now, time_now)
                    if color == 'green':
                        msg = 'The price of {} fall to {}%, the price now is {} {} {}.'.format(stock_code, change_pencent, price_now, date_now, time_now)
                    try:
                        send_msg(msg)
                        change_pencent_previous = change_pencent
                        msgsent = True
                    except:
                        pass

if __name__ == '__main__':
    main()
