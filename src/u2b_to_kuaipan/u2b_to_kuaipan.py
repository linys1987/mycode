# encoding: utf-8
# created on 2014年7月21日
# filename: u2b_to_kuaipan.py
# version: 1.0
# author: linyi1987@gmail.com

import sys
import urlparse
import time
import os
import re
import oauth2 as oauth
import json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
from urllib2 import HTTPError
import requests
import smtplib
from email.mime.text import MIMEText

TIME_ZONE = 'Asia/Shanghai'
RETRY_COUNT = 10

# 配置字符编码为utf-8
reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

# 读取配置文件
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open(r'config.ini'))
consumer_key = config.get('consumer', 'consumer_key')
consumer_secret = config.get('consumer', 'consumer_secret')
oauth_token = config.get('token', 'oauth_token')
oauth_token_secret = config.get('token', 'oauth_token_secret')

from_mail_address = config.get('mail', 'from_mail_address')
to_mail_address = config.get('mail', 'to_mail_address')
mail_password = config.get('mail', 'mail_password')
phone_number = config.get('phone', 'phone_number')
phone_password = config.get('phone', 'phone_password')

default_url = r'http://youtube.com/get_video_info?video_id='
quality_map = {5 : '.FLV', # 240P 
               17 : '.3GP', # 1440P
               18 : '.MP4', #  360P
               22 : '.MP4', # 720P
               36 : '.3GP', # 240P
               43 : '.WebM', # 360P
               82 : '.MP4', # 360P
               83 : '.MP4', # 240P
               84 : '.MP4', # 720P
               85 : '.MP4', # 1080P
               100 : '.WebM' # 360P
               }

class U2b(object):
    '''
    youtube视频是itag对应表
    参考来源: http://en.wikipedia.org/wiki/YouTube#Quality_and_codecs
    本程序主要下载22 MP4 720P格式的视频
    5    FLV    240p    Sorenson H.263    N/A    0.25    MP3    64
    17    3GP    144p    MPEG-4 Visual    Simple    0.05    AAC    24
    18    MP4    360p    H.264    Baseline    0.5    AAC    96
    22    MP4    720p    H.264    High    2-3    AAC    192
    36    3GP    240p    MPEG-4 Visual    Simple    0.175    AAC    36
    43    WebM    360p    VP8    N/A    0.5    Vorbis    128
    82    MP4    360p    H.264    3D    0.5    AAC    96
    83    MP4    240p    H.264    3D    0.5    AAC    96
    84    MP4    720p    H.264    3D    2-3    AAC    192
    85    MP4    1080p    H.264    3D    3-4    AAC    192
    100    WebM    360p    VP8    3D    N/A    Vorbis    128
    '''
    def __init__(self):
        self.quality_map = quality_map
        self.default_url = default_url
         
    def get_video_id(self, url):
        '''获取youtube视频id'''
        url_match = r'https?://www\.youtube\.com/watch\?v=(.*)'
        vid = re.search(url_match, url)
        if vid:
            vid = vid.group(1)
            print 'Get video id: ' + vid
            return vid
        else:
            print 'Bad url, check again.'
            return False

    def get_video_info(self, vid):
        '''通过get_video_info加视频ID的方式获取视频信息'''
        url = self.default_url + vid

        try:
            data = urllib2.urlopen(url, timeout=5).read()
            return data
        except Exception as e:
            return e
        
    def set_up_proxy(self, enable=False):
        #开启http的代理模式以供调试使用
        if enable:
            proxy_handler = urllib2.ProxyHandler({"http" : '127.0.0.1:8087'})
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
        else:
            proxy_handler = urllib2.ProxyHandler({})
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
                
    def format_title(self, title):
        '''格式化视频标题, 暂时没有更好的办法处理unicode字符'''
        title = re.sub('[^a-zA-Z0-9]', '', title)
        len_title = len(title)
        if title == '' or len_title < 10:
            title = 'Rename-' + time.strftime('%Y%m%d%H%M')
        return title
    
    def get_url_title(self, data):
        if isinstance(data, str):
            content = urlparse.parse_qs(data)
            
            # 判断是否正确获取video_info
            if 'status' in content and content['status'] == ['fail']:
                print 'Reason:', content['reason'][0]
                return -1
            
            # 格式化url_encoded_fmt_stream_map获取各版本视频下载链接
            # 返回质量最高的视频下载url
            url_encoded_fmt_stream_map = str(content['url_encoded_fmt_stream_map'])
            url_map = urlparse.parse_qs(url_encoded_fmt_stream_map)
            try:
                if 'url' in url_map and 'itag' in url_map:
                    url = url_map['url']
                    itag = url_map['itag']
                    url_itag = dict(zip(itag, url))
                    title = content['title'][0]
                    best_video_itag = url_map['itag'][0]
                    video_type = self.quality_map[int(best_video_itag)].lower()
                    best_url = url_itag[best_video_itag]
                    return best_url, title, video_type
                else:
                    print 'Bad data, try again.'
                    return -2
            except:
                return -2
    
    def download_video(self, url, title, videotype, max_file_size=300, write_file_size=200):
        '''下载视频并显示进度
        url: 视频下载链接
        title: 视频标题
        '''
        write_file_size = write_file_size*1024*1024
        file_name = self.format_title(title)
        # 伪装为浏览器访问, 未能解决403问题, 待查
        headers = {'Accept-Encoding':'gzip,deflate,sdch',
                   'Accept-Language':'zh-CN,zh;q=0.8',
                   'Connection':'keep-alive',
                   'User-Agent':'Chrome/36.0.1985.125'
                   #'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
                   }
        try:
            req = urllib2.Request(url, headers=headers)  
            u = urllib2.urlopen(req)
        except HTTPError as e:
            print e

        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        file_size_mb = round(file_size/1024.0/1024.0, 1)
        file_size_left = file_size
        print "Downloading: %s %sMB" % (file_name, file_size_mb)
        
        file_name_list = []
        file_size_dl = 0
        block_sz = 1024 * 512
        
        # 如果文件大小大于max_file_size限制, 文件将被分割为多个write_file_size大小的文件, 后缀为Part0, Part1, Part2等
        if file_size_mb >= max_file_size:
            print ('File size is %3.1fMB larger than %dMB, will be divided into %d pieces, %dMB per piece.' % 
                   (file_size_mb, max_file_size, int(file_size/write_file_size)+1, write_file_size/1024/1024))
            for i in range(int(file_size/write_file_size)+1):
                f = open(file_name+'-Part%d' % i+videotype, 'wb')
                file_name_list.append(file_name+'-Part%d' % i+videotype)
                while True:
                    buffer_block = u.read(block_sz)
                    if not buffer_block:
                        break
                    file_size_dl += len(buffer_block)
                    f.write(buffer_block)
                    status = r"%10d" % file_size_dl
                    if file_size_left <= write_file_size:
                        write_file_size = file_size_left
                    complete_percent = int(file_size_dl*50.0/(write_file_size))
                    status = (str(round(int(status)/1024.0/1024.0, 1)) + 'MB\t' + '[' + '>'*complete_percent 
                              + ' '*(50-complete_percent) + ']' + '  %3.2f%%' % (file_size_dl*100.0/(write_file_size)))
                    sys.stdout.write('\r'+status)
                    sys.stdout.flush()
                    if file_size_dl >= write_file_size:
                        file_size_dl = 0
                        file_size_left -= write_file_size
                        f.close()
                        break
                sys.stdout.write('\n')
                f.close()
        
        # 文件大小小于max_file_size, 下载为一个文件.
        else:
            f = open(file_name+videotype, 'wb')
            while True:
                buffer_block = u.read(block_sz)
                if not buffer_block:
                    break
             
                file_size_dl += len(buffer_block)
                f.write(buffer_block)
                status = r'%10d' % file_size_dl
                complete_percent = int(file_size_dl*50.0/file_size)
                status = (str(round(int(status)/1024.0/1024.0, 1)) + 'MB\t' + '[' + '>'*complete_percent 
                          + ' '*(50-complete_percent) + ']' + '  %3.2f%%' % (file_size_dl*100.0/file_size))
                sys.stdout.write('\r'+status)
                sys.stdout.flush()
            sys.stdout.write('\n')
            file_name_list.append(file_name+videotype)
            f.close()
        return file_name_list
        
class KuaiPanAuth(object):
    '''获取快盘token, 参考文档:
    https://developer.linkedin.com/documents/getting-oauth-token-python
    '''
    def __init__(self):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
    
    @staticmethod
    def str_to_dict(string):
        '''将字符串转换为字典'''
        string = string.replace('\'', '"')
        string = json.loads(string)
        return string
    
    def get_oauth_token(self):
        '''获取快盘token'''
        consumer = oauth.Consumer(consumer_key, consumer_secret)
        client = oauth.Client(consumer)
        request_token_url = r'https://openapi.kuaipan.cn/open/requestToken'
        resp, content = client.request(request_token_url, "POST")
        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])
        
        request_token = self.str_to_dict(content)
        authorize_rul = r'https://www.kuaipan.cn/api.php?ac=open&op=authorise&oauth_token=' + request_token['oauth_token']
        
        # 登录快盘并授权
        try:
            print'Opening:', authorize_rul
            import webbrowser
            webbrowser.open(authorize_rul,new=2)
        except:
            print 'Auto open url fail, copy the url below and paste in the browser:'
            print authorize_rul
        
        # 获取返回的pin码,存储到oauth_verifier
        accepted = 'n'
        while accepted.lower() == 'n':
            accepted = raw_input('Is authorized? (y/n) ')
        oauth_verifier = raw_input('What is the PIN? ')
        
        # 获取access_token
        try:
            access_token_url = r'https://openapi.kuaipan.cn/open/accessToken'
            token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
            token.set_verifier(oauth_verifier)
            client = oauth.Client(consumer, token)
            resp, content = client.request(access_token_url, "POST")
            access_token = self.str_to_dict(content)
            for key in access_token:
                print key + ': ' + str(access_token[key])
            return access_token
        except Exception as e:
            print 'Get access_token fail:'
            print e
            
class KuaiPan(object):
    '''快盘Api'''
    def __init__(self):
        self.oauth_token_secret = oauth_token_secret
        self.oauth_token = oauth_token
        self.token = oauth.Token(oauth_token, oauth_token_secret)
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        self.signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
    
    def get_oauth_url(self, url, method='GET', parameters=None):
        '''获取upload地址'''
        oauth_request = oauth.Request.from_consumer_and_token(self.consumer,
                                                              token=self.token,
                                                              http_method=method,
                                                              http_url=url,
                                                              parameters=parameters,
                                                              is_form_encoded=True)
        oauth_request.sign_request(self.signature_method_hmac_sha1, self.consumer, self.token)
        # print oauth_request.to_url()
        return oauth_request.to_url()
    
    def get_upload_locate(self):
        '''获取上传url'''
        default_get_url = r'http://api-content.dfs.kuaipan.cn/1/fileops/upload_locate'
        content = urllib2.urlopen(default_get_url)
        resp, text = content.code, content.read()
        if resp == 200:
            result = KuaiPanAuth.str_to_dict(text)
            return result
        else:
            print 'Get upload locate fail:'
            print content.read()
            
    def upload_file(self, filelocate, forceoverwrite=True):
        '''上传文件'''
        register_openers()
        url = self.get_upload_locate()['url'] + r'1/fileops/upload_file'
        parameters = {'path': filelocate,
                      'root': 'root',
                      'overwrite' : forceoverwrite
                      }
        print 'Uploading %s' % filelocate
        upload_url = self.get_oauth_url(url, method='POST', parameters=parameters)
        datagen, headers = multipart_encode({filelocate: open(filelocate, 'rb')})
        try:
            request = urllib2.Request(upload_url, datagen, headers)
            content = urllib2.urlopen(request)
            if content.code == 200:
                print 'Upload %s successed.' % filelocate
                return content.code
            else:
                print 'Upload failed.'
                return content.code
        except Exception as e:
            print 'Upload failed.'
            print e
            
def set_timezone(timezone):
    os.environ['TZ'] = timezone
    time.tzset()  # @UndefinedVariable

def send_msg(msg):
    '''使用飞信短信接口发送信息提醒'''
    url_space_login = 'http://f.10086.cn/huc/user/space/login.do?m=submit&fr=space'
    url_login = 'http://f.10086.cn/im/login/cklogin.action'
    url_sendmsg = 'http://f.10086.cn/im/user/sendMsgToMyselfs.action'
    parameter= { 'mobilenum':phone_number, 'password':phone_password}
        
    session = requests.Session()
    session.post(url_space_login, data = parameter)
    session.get(url_login)
    session.post(url_sendmsg, data = {'msg':msg})
        
def send_mail(subject, msg):
    '''使用网易邮箱发送邮件提醒'''
    msg = MIMEText(msg, _charset='UTF-8')
    msg['Subject'] = subject
    msg['From'] = from_mail_address
    msg['To'] = to_mail_address
        
    smail = smtplib.SMTP('smtp.163.com')
    smail.login(from_mail_address, mail_password)
    smail.sendmail(from_mail_address, [to_mail_address], msg.as_string())
    smail.quit()
    
def main():
    '''主程序'''
    set_timezone(TIME_ZONE)
    start = time.time()
    # 重试次数
    count = 0
    url = sys.argv[1]
    if url == '--upload':
        kuaipan = KuaiPan()
        file_name = sys.argv[2]
        kuaipan.upload_file(file_name, True)
    else:
        u2b = U2b()
        vid = u2b.get_video_id(url)
        data = u2b.get_video_info(vid)
        down_url, title, video_type = '', '', ''
        if u2b.get_url_title(data) == -1:
            return False
        while u2b.get_url_title(data) == -2:
            data = u2b.get_video_info(vid)
            if u2b.get_url_title(data) != -2:
                down_url, title, video_type = u2b.get_url_title(data)
            count += 1
            if count >= RETRY_COUNT:
                print 'Retry %d times, exit.' % count
                return False
        down_url, title, video_type = u2b.get_url_title(data)            
        file_name_list = u2b.download_video(down_url, title, video_type, 300, 200)
        kuaipan = KuaiPan()
        for file_name in file_name_list:
            kuaipan.upload_file(file_name, True)
            # 删除完成上传的文件
            os.remove(file_name)
    stop = time.time()
    print 'Cost', round(stop - start, 2),'seconds.'

if __name__ == '__main__':
    main()
