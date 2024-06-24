from Crypto.Cipher import DES
import base64
import binascii
import execjs


def encrypt(key, text):
    cryptor = DES.new(key.encode(), DES.MODE_ECB)
    # 这里密钥key 长度必须为16（AES-128）,
    # 24（AES-192）,或者32 （AES-256）Bytes 长度
    # 目前AES-128 足够目前使用
    length = 8
    count = len(text)
    # 0 填充
    if count < length:
        add = (length - count)
        # \0 backspace
        text = text + ('\0' * add)
    elif count > length:
        add = (length - (count % length))
        text = text + ('\0' * add)
    ciphertext = cryptor.encrypt(text.encode())
    # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    # 所以这里统一把加密后的字符串转化为16进制字符串
    return base64.b64encode(ciphertext)

def decrypt(key,decryptText):
    cipherX = DES.new(key.encode(), DES.MODE_ECB)
    y = cipherX.decrypt(decryptText)
    return y.decode()

if __name__ == '__main__':
    # text = '{"d":0.19,"m":[[0,1,0],[31,-2,102],[55,-3,201],[57,-3,302]],"c":314,"cs":1,"wd":0}'
    # key = "0a711d8b"
    text = base64.b64decode("tPmzA8fX1WY=")
    key = "sshummei"
    new_key = decrypt(key,text)
    print(new_key)
    import random
    print(random.randint(5, 20))

    print(list(map(list,zip([1,2,3],[1,2,3],[1,2,3]))))


