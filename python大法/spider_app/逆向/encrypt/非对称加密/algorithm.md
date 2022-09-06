### 非对称加密

```
公钥和私钥不同，公钥加密的数据，私钥才能解密；私钥加密的数据，公钥才能解密；
私钥包含公钥，公钥无法推导出私钥
```

### RSA

```
私钥的格式：
pkcs1： private rsa private key
pkcs8： private private key
```

### RSA模式与填充细节

```
None 模式与ECB模式是一直的；
NOPadding：
明文最多字节树为密钥字节数
密文与密钥等长
填充字节0，加密后的密文不变

PKCS1Padding：
明文最大字节数为密钥字节数-11
密文与密钥等长
每一次的填充不一样，使得加密后的密文会变
```

# 非对称加密和对称加密组合使用

```
随机生成AES密钥,
使用AES对明文加密,得到数据密文cipherText;
使用RSA公钥对AES密钥加密,得到密钥密文cipherKey
提交密钥密文cipherKey和cipherText到服务器;
服务器使用RSA私钥解析获得AES的密文;
使用AES密钥对密文解密
```