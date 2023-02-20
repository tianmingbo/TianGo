import time
import base64
from urllib import parse
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5

password = "12345678"
timestamp = str(int(time.time() * 1000))
encrypted_object = timestamp + "|" + password
public_key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDq04c6My441Gj0UFKgrqUhAUg+kQZeUeWSPlAU9fr4HBPDldAeqzx1UR92KJHuQh/zs1HOamE2dgX9z/2oXcJaqoRIA/FXysx+z2YlJkSk8XQLcQ8EBOkp//MZrixam7lCYpNOjadQBb2Ot0U/Ky+jF2p+Ie8gSZ7/u+Wnr5grywIDAQAB"
rsa_key = RSA.import_key(base64.b64decode(public_key))  # 导入读取到的公钥
cipher = PKCS1_v1_5.new(rsa_key)  # 生成对象
encrypted_password = base64.b64encode(cipher.encrypt(encrypted_object.encode(encoding="utf-8")))
encrypted_password = parse.quote(encrypted_password)
print(encrypted_password)
