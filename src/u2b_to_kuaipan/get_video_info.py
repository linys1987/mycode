# encoding: utf-8

import urlparse

f = open('get_video_info', 'rb')
text = f.read()
f.close()

data = urlparse.parse_qs(text)
# for key in data:
#     print key
# print data['url_encoded_fmt_stream_map']

url_map = urlparse.parse_qs(str(data['url_encoded_fmt_stream_map']))
title = data['title'][0]
best_url = url_map['url']
video_type = url_map['itag'][0]

print type(video_type)

# print data['title']
# for key in url_itag:
#     print key
# print url_itag['itag']
# # print data



#['22', '43', '18', '5', '36', '17']
# 5    FLV    240p    Sorenson H.263    N/A    0.25    MP3    64
# 17    3GP    144p    MPEG-4 Visual    Simple    0.05    AAC    24
# 18    MP4    360p    H.264    Baseline    0.5    AAC    96
# 22    MP4    720p    H.264    High    2-3    AAC    192
# 36    3GP    240p    MPEG-4 Visual    Simple    0.175    AAC    36
# 43    WebM    360p    VP8    N/A    0.5    Vorbis    128
# 82    MP4    360p    H.264    3D    0.5    AAC    96
# 83    MP4    240p    H.264    3D    0.5    AAC    96
# 84    MP4    720p    H.264    3D    2-3    AAC    192
# 85    MP4    1080p    H.264    3D    3-4    AAC    192
# 100    WebM    360p    VP8    3D    N/A    Vorbis    128