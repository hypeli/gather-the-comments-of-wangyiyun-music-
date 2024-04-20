# This Python file uses the following encoding: utf-8
"""抓取网易云音乐热评
post
1.找到未加密参数
2.把参数进行加密，并且加密过程要与网易云的一致， params->encText, encSecKey->encSecKey
3.请求网易拿评论
"""
import requests
from Crypto.Cipher import AES
from base64 import b64encode
import json

import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='

# 真实参数
data1 = {
    'csrf_token': "",
    'cursor': "-1",
    'offset': "0",
    'orderType': "1",
    'pageNo': "1",
    'pageSize': "20",
    'rid': "R_SO_4_1382576173",
    'threadId': "R_SO_4_1382576173",
}

# 服务于d
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'
e = '010001'
i = 'Y8s72hDJ7t1IKRI2'  # 手动固定
def get_encSeckey():    # i固定，它也固定
    return 'd2945ca2eeeb45e32e784e50a81431dda8c871ac7b8182f6e5bff55f1c333c96cf39516e0639ff833a6282b2023d993596f9e3d659f55059b754ec4f07ae18b6d2201eebbf9dfca703f2f9dc739e961f8ba5bf43015f34d338726f4215baad9996eae4bca4ae153fc04a1a758c891520615d8afab1c2a46777ad3987dfaac1b3'

# 转换为十六的倍数，为下方加密算法服务
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data

def get_params(data):   # 默认接收到的是字符串，因为字典无法加密
    first = enc_params(data, g)
    second = enc_params(first, i)
    return second

def enc_params(data, key):  # 加密过程
    data = to_16(data)
    aes = AES.new(key=key.encode('utf-8'), iv='0102030405060708'.encode('utf-8'), mode=AES.MODE_CBC)    # 创建加密器
    bs = aes.encrypt(data.encode('utf-8'))   # 加密完结果无法被utf-8识别。加密的内容长度必须是十六的倍数
    return str(b64encode(bs), 'utf-8')  # 转换成字符串



# 处理加密过程
'''
function a(a) {# 返回随机的十六位字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)  # 循环十六次
            e = Math.random() * b.length,   # 随机数
            e = Math.floor(e),  # 取整
            c += b.charAt(e);   # 取字符串中的某某位置
        return c
    }
    function b(a, b) {# 数据，'0CoJUm6Qyw8W8jud'
        var c = CryptoJS.enc.Utf8.parse(b)  # b是密钥
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          # AES加密
          , f = CryptoJS.AES.encrypt(e, c, {    # 加密的密钥
            iv: d,  # 偏移量
            mode: CryptoJS.mode.CBC # 模式
        });
        return f.toString()
    }
    function c(a, b, c) {
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    入口
    f:'00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    function d(d, e, f, g) {    d:数据 e:'010001' f: g: '0CoJUm6Qyw8W8jud'
        var h = {}  # 空对象
          , i = a(16);  # 十六位随机值,把i设置成定值，为了让c返回的数是固定的
        return h.encText = b(d, g),
        h.encText = b(h.encText, i),    # params
        h.encSecKey = c(i, e, f),    # en

    }
'''
data2 = {
    'params': get_params(json.dumps(data1)),
    'encSecKey': get_encSeckey()
    }
res = requests.post(url=url, data=data2)
res.encoding = res.apparent_encoding
res = res.json()
# res.encoding = res.apparent_encoding
# print(res.text)
comment_list = res['data']['comments']
for comment in comment_list:
    print(comment['content'])
