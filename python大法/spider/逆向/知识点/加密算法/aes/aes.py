# @Time : 2022/5/23 23:27
# @Author :bo~
# @FileName: aes.py
# @Description: AES
import base64
from Crypto.Cipher import AES

"""
填充：
pkcs7：缺多少补多少，补的是缺的数字。如127bit，不到128bit，后面补1
x923填充字节0
模式：
每个块128bit，可以指定每个块的加密方式
ECB： 每个分块分别进行AES加密
CBC： 每个密文块都依赖于前面的所有明文块，IV先与第一个明文块进行异或。
"""


# AES
# 需要补位，str不是16的倍数那就补足为16的倍数
def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes


# 加密方法
def encrypt(key, text):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)  # 初始化加密器
    # aes = AES.new(add_to_16(key), AES.MODE_CBC)  # 初始化加密器 CBC模式
    encrypt_aes = aes.encrypt(add_to_16(text))  # 先进行aes加密,分段加密，每次128bit
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
    return encrypted_text


# 解密方法
def decrypt(key, text):
    aes = AES.new(add_to_16(key), AES.MODE_ECB)  # 初始化加密器
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')  # 执行解密密并转码返回str
    return decrypted_text
