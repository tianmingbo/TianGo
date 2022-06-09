# @Time : 2022/5/23 23:17
# @Author :bo~
# @FileName: base64.py
# @Description:
import base64


def base64_encode(text):
    encode_data = base64.b64encode(text.encode())
    return encode_data


def base64_decode(encode_data):
    decode_data = base64.b64decode(encode_data)
    return decode_data


if __name__ == '__main__':
    text = 'I love Python!'
    encode_data = base64_encode(text)
    decode_data = base64_decode(encode_data)
    print('Base64 编码：', encode_data)
    print('Base64 解码：', decode_data)

# Base64 编码：b'SSBsb3ZlIFB5dGhvbiE='
# Base64 解码：b'I love Python!'
