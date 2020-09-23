# int CRC = ox0000ffff;
# int POLYNOMIAL = 0x00o0a0o1;
# int i，j;
# for (i = 0; i < bytes.length; i++){
# CRC^= (int) bytes[i];
# for (j= 0; j<8; j++){
# if ((CRC & oxoooo00o1)== 1){
# CRC>>= 1;
# CRC^= POLYNOMIAL;
# }else {
# CRC >>= 1;
#
# CRC = 0x0000ffff
# POLYNOMIAL = 0x0000a0001
# bytes = 0x7E00160100000000044C0000300000000B010000023000B7987D
# for i in range(len(bytes)):
#     CRC ^= int(bytes[i])
#     for j in range(8):
#         if CRC & 0x00000001 == 1:
#             CRC >>= 1
#             CRC ^= POLYNOMIAL
#         else:
#             CRC >>= 1
#
# print(CRC)


def crc16(x):
    CRC = 0
    POLYNOMIAL = 0x1005
    while x:
        wchar=x[:2]
        x=x[2:]
    # for byte in x:
        wchar = ord(wchar)
        CRC ^= (wchar << 8)
        print(hex(wchar), hex(CRC))
        for i in range(8):
            if CRC & 0x8000:
                CRC <<= 1
                CRC ^= POLYNOMIAL
            else:
                CRC <<= 1
        print('end\t\t', hex(CRC))
    s = hex(CRC).upper()
    print(s)
    # return s[4:6] + s[2:4] if invert == True else s[2:4] + s[4:6]


def calc_crc(string):
    data = bytearray.fromhex(string)
    crc = 0xFFFF
    for pos in data:
        print(pos)
        crc ^= pos
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return hex(((crc & 0xff) << 8) + (crc >> 8))


crc = calc_crc('0102030405060708')
print(crc)


if __name__ == '__main__':
    # 7E00140100000000044C0000300000000B02000002 12717D
    print(crc16("16014C"))
