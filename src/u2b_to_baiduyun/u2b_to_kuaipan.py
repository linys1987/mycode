# encoding: utf-8
# created on 2014年7月21日
# filename: u2b_to_kuaipan.py
# version: 1.0
# author: linyi1987@gmail.com

import u2b
import Kuaipan
from kuaipan_lin import *

file = Kuaipan.KuaipanFile(consumer_key, consumer_secret, oauth_token, oauth_token_secret)
file.upload_file(r'C:\Users\Lin\Downloads\yturl-master.zip', 'yturl-master.zip', True)
