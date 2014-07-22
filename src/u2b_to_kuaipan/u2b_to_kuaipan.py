# encoding: utf-8
# created on 2014年7月21日
# filename: u2b_to_kuaipan.py
# version: 1.0
# author: linyi1987@gmail.com

import urlparse
import oauth2 as oauth
import json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import requests

consumer_key = r'xcurFwFZzzEFFQ9H'
consumer_secret = r'CN4kIlggsjKZaevY'

oauth_token = r'04493d217ca5799c627c73df'
oauth_token_secret = r'84ce4479edf74487b2eb3207e137bdc0'

from_mail_address = ''
to_mail_address = ''
mail_password = ''
phone_number = ''
phone_password = ''

default_url = r'http://youtube.com/get_video_info?video_id='
quality_map = {5 : 'FLV 240P', 
               17 : '3GP 1440',
               18 : 'MP4 360P',
               22 : 'MP4 720P',
               36 : '3GP 240P',
               43 : 'WebM 360P',
               82 : 'MP4 360P',
               83 : 'MP4 240P',
               84 : 'MP4 720P',
               85 : 'MP4 1080P',
               100 : 'WebM 360P'
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
        import re
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
        
    def set_up_proxy(self, enable=True):
        #开启http的代理模式以供调试使用
        if enable:
            proxy_handler = urllib2.ProxyHandler({"http" : '127.0.0.1:8087'})
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
        else:
            proxy_handler = urllib2.ProxyHandler({})
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
    
    def get_download_url(self, data):
        '''获取视频下载url'''
        if isinstance(data, str):
            content = urlparse.parse_qs(data)
            
            # 判断是否正确获取video_info
            if 'status' in content and content['status'] == ['fail']:
                print 'Reason:', content['reason'][0]
                return -1
            
            # 格式化url_encoded_fmt_stream_map获取各版本视频下载链接
            url_encoded_fmt_stream_map = str(content['url_encoded_fmt_stream_map'])
            url_map = urlparse.parse_qs(url_encoded_fmt_stream_map)
            if 'url' in url_map and 'itag' in url_map:
                url = url_map['url']
                itag = url_map['itag']
                url_itag = dict(zip(itag, url))
                url_itag['title'] = content['title'][0]
                for key in url_itag:
                    print key, url_itag[key]
                #print url_itag
                return url_itag
            else:
                print 'Bad data, try again.'
    
    def download_video(self, url, title):
        '''下载视频并显示进度
        url: 视频下载链接
        title: 视频标题
        '''
        file_name = title.replace('|', '').replace(';', ' ') + '.mp4'
        u = urllib2.urlopen(url)
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        
        file_size_dl = 0
        block_sz = 1024 * 8 * 8
        while True:
            buffer_block = u.read(block_sz)
            if not buffer_block:
                break
        
            file_size_dl += len(buffer_block)
            f.write(buffer_block)
            status = r"%10d" % file_size_dl
            status = str(round(int(status)/1024.0/1024.0, 1)) + 'MB  ' + '>'*int(file_size_dl*100.0/file_size)+' %3.2f%%' % (file_size_dl * 100. / file_size)
            print status
        f.close()
        
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
        default_url = r'http://api-content.dfs.kuaipan.cn/1/fileops/upload_locate'
        content = urllib2.urlopen(default_url)
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
                      'root': 'app_folder',
                      'overwrite' : forceoverwrite
                      }
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
            
class Notification(object):
    
    def __init__(self):
        self.from_mail_address = from_mail_address
        self.to_mail_address = to_mail_address
        self.phone_number = phone_number
        self.phone_password = phone_password
        self.mail_password = mail_password
        
    def send_msg(self, msg):
        '''使用飞信短信接口发送信息提醒'''
        url_space_login = 'http://f.10086.cn/huc/user/space/login.do?m=submit&fr=space'
        url_login = 'http://f.10086.cn/im/login/cklogin.action'
        url_sendmsg = 'http://f.10086.cn/im/user/sendMsgToMyselfs.action'
        parameter= { 'mobilenum':self.phone_number, 'password':self.phone_password}
        
        session = requests.Session()
        session.post(url_space_login, data = parameter)
        session.get(url_login)
        session.post(url_sendmsg, data = {'msg':msg})
        
    def send_mail(self, subject, msg):
        '''使用网易邮箱发送邮件提醒'''
        import smtplib
        from email.mime.text import MIMEText
        msg = MIMEText(msg, _charset='UTF-8')
        msg['Subject'] = subject
        msg['From'] = self.from_mail_address
        msg['To'] = self.to_mail_address
        
        smail = smtplib.SMTP('smtp.163.com')
        smail.login(self.from_mail_address, self.mail_password)
        smail.sendmail(self.from_mail_address, [self.to_mail_address], msg.as_string())
        smail.quit()