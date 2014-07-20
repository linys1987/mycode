# encoding: utf-8
import urlparse
import urllib2
# import time

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

QUALITY_MAP ={5 : 'FLV 240P', 
              17 : '3GP 1440',
              18 : 'MP4 360P',
              22 : 'MP4 720P',
              36 : '3GP 240P',
              43 : 'WebM 360P',
              82 : 'MP4 360P',
              83 : 'MP4 240P',
              84 : 'MP4 720P',
              85 : 'MP4 1080P',
              100 : 'WebM 360P'}

def get_video_info(vid):
    '''通过get_video_info加视频ID的方式获取视频信息'''
    DEFAULT_URL = r'http://youtube.com/get_video_info?video_id='
    url = DEFAULT_URL + vid
    
    #开启http的代理模式以供调试使用
    proxy_handler = urllib2.ProxyHandler({"http" : '127.0.0.1:8087'})
    opener = urllib2.build_opener(proxy_handler)
    urllib2.install_opener(opener)

    try:
        data = urllib2.urlopen(url, timeout=5).read()
        return data
    except Exception as e:
        return e

def get_download_url(data):
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

def download_video(url, title):
    file_name = title.replace('|', '').replace(';', ' ') + '.mp4'
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    
    file_size_dl = 0
    block_sz = 1024*8*8
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

a = get_download_url(get_video_info('LGtwHqXbR_k'))
download_video(a['22'], a['title'])

# b=open('get_video_info', 'r')
# b = b.read()
# a = urlparse.parse_qs(b)

# c = urlparse.parse_qs(str(a['url_encoded_fmt_stream_map']))


# for item in c:
#     print item, c[item]