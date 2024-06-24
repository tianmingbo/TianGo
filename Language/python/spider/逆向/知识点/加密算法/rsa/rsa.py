from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, PKCS1_OAEP
import base64


def generate_key():
    key = RSA.generate(2048)  # 模2048bit
    print('正在生成公钥！')
    with open('public.pem', 'wb') as f:
        f.write(key.public_key().export_key())
    print('正在生成私钥！')
    with open('private.pem', 'wb') as f:
        f.write(key.export_key())


def encrypt(data):
    with open('public.pem', 'rb') as f:
        content = f.read()
    rsakey = RSA.import_key(content)
    rsakey = PKCS1_v1_5.new(rsakey)
    res = base64.b64encode(rsakey.encrypt(data))
    print("加密信息：", res.decode('utf8'))
    return res


def decrypt(data):
    with open('private.pem', 'rb') as f:
        content = f.read()
    rsakey = RSA.import_key(content)
    rsakey = PKCS1_v1_5.new(rsakey)
    res = rsakey.decrypt(base64.b64decode(data), "ERROR")
    print("解密信息：", res.decode('utf8'))
    return res


if __name__ == '__main__':
    generate_key()
    data = "dali".encode('utf8')
    encodeData = encrypt(data)
    decodeData = decrypt(encodeData)
