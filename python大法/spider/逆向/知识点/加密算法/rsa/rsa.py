# @Time : 2022/5/23 23:28
# @Author :bo~
# @FileName: rsa.py
# @Description:
import rsa


def rsa_encrypt(pu_key, t):
    # 公钥加密
    rsa = rsa.encrypt(t.encode("utf-8"), pu_key)
    return rsa


def rsa_decrypt(pr_key, t):
    # 私钥解密
    rsa = rsa.decrypt(t, pr_key).decode("utf-8")
    return rsa


if __name__ == "__main__":
    public_key, private_key = rsa.newkeys(512)   # 生成公钥、私钥
    print('公钥：', public_key)
    print('私钥：', private_key)
    text = 'I love Python!'  # 加密对象
    encrypted_str = rsa_encrypt(public_key, text)
    print('加密字符串：', encrypted_str)
    decrypted_str = rsa_decrypt(private_key, encrypted_str)
    print('解密字符串：', decrypted_str)

'''
公钥：PublicKey(7636479066127060956100056267701318377455704072072698049978592945665550579944731953431504993757594103617537700972424661030900303472123028864161050235168613, 65537)
私钥：PrivateKey(7636479066127060956100056267701318377455704072072698049978592945665550579944731953431504993757594103617537700972424661030900303472123028864161050235168613, 65537, 3850457767980968449796700480128630632818465005441846698224554128042451115530564586537997896922067523638756079019054611200173122138274839877369624069360253, 4713180694194659323798858305046043997526301456820208338158979730140812744181638767, 1620238976946735819854194349514460863335347861649166352709029254680140139)
加密字符串：b"\x1aaeps\xa0c}\xb6\xcf\xa3\xb0\xbb\xedA\x7f}\x03\xdc\xd5\x1c\x9b\xdb\xda\xf9q\x80[=\xf5\x91\r\xd0'f\xce\x1f\x01\xef\xa5\xdb3\x96\t0qIxF\xbd\x11\xd6\xb25\xc5\xe1pM\xb4M\xc2\xd4\x03\xa6"
解密字符串：I love Python!
'''