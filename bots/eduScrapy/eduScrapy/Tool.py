
import base64
import json
from aip import AipOcr
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA

# publickey算法
def crack_pwd(key, pwd):
    key = "-----BEGIN PUBLIC KEY-----\n" + key + "\n-----END PUBLIC KEY-----"
    rsakey = RSA.importKey(key)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
    cipher_text = base64.b64encode(cipher.encrypt(pwd.encode(encoding="utf-8")))  # 对传递进来的用户名或密码字符串加密
    value = cipher_text.decode('utf8')  # 将加密获取到的bytes类型密文解码成str类型
    return value

def yzm(image):

    # 调用百度云SDK，正式上线请使用你自己的APP_ID,API_KEY,SECRET_KEY
    APP_ID = '19620339'
    API_KEY = 'Q41VnfAoDna1SaRqtbSuoGI9'
    SECRET_KEY = 'NqOunCOzclO2mTAOGAxqxmxRbrOkA1dq'

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    message = client.basicGeneral(image)
    return message