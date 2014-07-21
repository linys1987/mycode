# encoding: utf-8
# created on 2014年7月21日
# filename: kuaipan.py
# version: 1.0
# author: linys1987@gmail.com

'''使用金山快盘的接口将文件上传到网盘
参考文档: http://www.kuaipan.cn/developers/document.htm
'''

consumer_key = r'xcurFwFZzzEFFQ9H'
consumer_secret = r'CN4kIlggsjKZaevY'
oauth_token_secret = r'84ce4479edf74487b2eb3207e137bdc0'
oauth_token = r'04493d217ca5799c627c73df'

def str_to_dict(string):
    import json
    string = string.replace('\'', '"')
    string = json.loads(string)
    return string

def get_oauth_token():
    '''获取快盘token, 参考文档:
    https://developer.linkedin.com/documents/getting-oauth-token-python
    '''
    import oauth2 as oauth
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)
    request_token_url = r'https://openapi.kuaipan.cn/open/requestToken'
    resp, content = client.request(request_token_url, "POST")
    if resp['status'] != '200':
        raise Exception("Invalid response %s." % resp['status'])
    
    request_token = str_to_dict(content)
    authorize_rul = r'https://www.kuaipan.cn/api.php?ac=open&op=authorise&oauth_token=' + request_token['oauth_token']
    
    # 登录快盘并授权
    try:
        print'尝试自动打开链接:', authorize_rul
        import webbrowser
        webbrowser.open(authorize_rul,new=2)
    except:
        print '自动打开链接失败,使用浏览器打开下面链接:'
        print authorize_rul
    
    # 获取返回的pin码,存储到oauth_verifier
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('是否授权? (y/n) ')
    oauth_verifier = raw_input('输入返回PIN码?')
    
    # 获取access_token
    try:
        access_token_url = r'https://openapi.kuaipan.cn/open/accessToken'
        token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        client = oauth.Client(consumer, token)
        resp, content = client.request(access_token_url, "POST")
        access_token = str_to_dict(content)
        for key in access_token:
            print key.upper() + ': ' + str(access_token[key])
        return access_token
    except Exception as e:
        print '获取access_token失败,返回消息内容:'
        print e
if __name__ == '__main__':   
    get_oauth_token()