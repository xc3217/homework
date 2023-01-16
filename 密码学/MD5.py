S = [7,  12,  17,  22,  7,  12,  17,  22,  7,  12,  17,  22,  7,  12,  17,  22,
        5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
t = [0xD76AA478, 0xE8C7B756, 0x242070DB, 0xC1BDCEEE, 0xF57C0FAF, 0x4787C62A, 0xA8304613, 0xFD469501,
    0x698098D8, 0x8B44F7AF, 0xFFFF5BB1, 0x895CD7BE, 0x6B901122, 0xFD987193, 0xA679438E, 0x49B40821,
    0xF61E2562, 0xC040B340, 0x265E5A51, 0xE9B6C7AA, 0xD62F105D, 0x02441453, 0xD8A1E681, 0xE7D3FBC8,
    0x21E1CDE6, 0xC33707D6, 0xF4D50D87, 0x455A14ED, 0xA9E3E905, 0xFCEFA3F8, 0x676F02D9, 0x8D2A4C8A,
    0xFFFA3942, 0x8771F681, 0x6D9D6122, 0xFDE5380C, 0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70,
    0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05, 0xD9D4D039, 0xE6DB99E5, 0x1FA27CF8, 0xC4AC5665,
    0xF4292244, 0x432AFF97, 0xAB9423A7, 0xFC93A039, 0x655B59C3, 0x8F0CCC92, 0xFFEFF47D, 0x85845DD1,
    0x6FA87E4F, 0xFE2CE6E0, 0xA3014314, 0x4E0811A1, 0xF7537E82, 0xBD3AF235, 0x2AD7D2BB, 0xEB86D391]

m = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12,
    5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2,
    0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]

def int2bin(n,  count=24):
    return "".join([str((n >> y) & 1) for y in range(count-1,  -1,  -1)])
def F(x,  y,  z):
    return (x & y) | ((~x) & z)
def G(x,  y,  z):
    return (x & z) | (y & (~z))
def H(x,  y,  z):
    return x ^ y ^ z
def I(x,  y,  z):
    return y ^ (x | (~z))
def rol(x,  t):
    x &= 0xFFFFFFFF
    x = ((x << t) | (x >> (32 - t))) & 0xFFFFFFFF
    return x
def FF(a,  b,  c,  d,  x,  s,  t):
    temp = a + F(b,  c,  d) + x + t
    temp = rol(temp,  s)
    result = (temp + b) & 0xFFFFFFFF
    return result
def GG(a,  b,  c,  d,  x,  s,  t):
    temp = a + G(b,  c,  d) + x + t
    temp = rol(temp,  s)
    result = (temp + b) & 0xFFFFFFFF
    return result
def HH(a,  b,  c,  d,  x,  s,  t):
    temp = a + H(b,  c,  d) + x + t
    temp = rol(temp,  s)
    result = (temp + b)& 0xFFFFFFFF
    return result
def II(a,  b,  c,  d,  x,  s,  t):
    temp = a + I(b,  c,  d) + x + t
    temp = rol(temp,  s)
    result = (temp + b) & 0xFFFFFFFF
    return result
def fill(x):
    text = ""
    for i in range(len(x)):
        c = int2bin(ord(x[i]),  8)
        text += c

    if (len(text) % 512 != 448):
        if ((len(text) + 1) % 512 != 448):
            text += '1'
        while (len(text) % 512 != 448):
            text += '0'

    length = len(x) * 8
    if (length <= 255):
        length = int2bin(length,  8)
    else:
        length = int2bin(length,  16)
        temp = length[8:12] + length[12:16] + length[0:4] + length[4:8]
        length = temp

    text += length
    while (len(text) % 512 != 0):
        text += '0'
    return text
def main():
    # 构造常数表
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476

    # 初始输入的ABCD
    init_A = A
    init_B = B
    init_C = C
    init_D = D
    plaintext = "Lakers never die!!!"
    filled_plaintext = fill(plaintext)
    print(filled_plaintext)

    M = []
    for i in range(0,  len(filled_plaintext),  32):
        num = ""
        for j in range(0,  len(filled_plaintext[i:i + 32]),  4):
            temp = filled_plaintext[i:i + 32][j:j + 4]
            temp = hex(int(temp,  2))
            num += temp[2]

        num_tmp = ""
        for j in range(8,  0,  -2):
            temp = num[j - 2:j]
            num_tmp += temp

        num = ""
        for i in range(len(num_tmp)):
            num += int2bin(int(num_tmp[i],  16),  4)
        temp = int(num, 2)
        M.append(temp)
    print(M)

    for k in range(0,len(filled_plaintext)//512):
        for j in range(0, 16):
            if (j % 4 == 0):
                A = FF(A,  B,  C,  D,  M[m[j]],  S[j],  t[j])
            if (j % 4 == 1):
                D = FF(D,  A,  B,  C,  M[m[j]],  S[j],  t[j])
            if (j % 4 == 2):
                C = FF(C,  D,  A,  B,  M[m[j]],  S[j],  t[j])
            if (j % 4 == 3):
                B = FF(B,  C,  D,  A,  M[m[j]],  S[j],  t[j])

        for j in range(0, 16):
            if(j % 4 == 0):
                A = GG(A,  B,  C,  D,  M[m[j+16]],  S[j+16],  t[j+16])
            if(j % 4 == 1):
                D = GG(D,  A,  B,  C,  M[m[j+16]],  S[j+16],  t[j+16])
            if (j % 4 == 2):
                C = GG(C,  D,  A,  B,  M[m[j+16]],  S[j+16],  t[j+16])
            if (j % 4 == 3):
                B = GG(B,  C,  D,  A,  M[m[j+16]],  S[j+16],  t[j+16])

        for j in range(0, 16):
            if (j % 4 == 0):
                A = HH(A,  B,  C,  D,  M[m[j+32]],  S[j+32],  t[j+32])
            if (j % 4 == 1):
                D = HH(D,  A,  B,  C,  M[m[j+32]],  S[j+32],  t[j+32])
            if (j % 4 == 2):
                C = HH(C,  D,  A,  B,  M[m[j+32]],  S[j+32],  t[j+32])
            if (j % 4 == 3):
                B = HH(B,  C,  D,  A,  M[m[j+32]],  S[j+32],  t[j+32])

        for j in range(0, 16):
            if (j % 4 == 0):
                A = II(A,  B,  C,  D,  M[m[j+48]],  S[j+48],  t[j+48])
            if (j % 4 == 1):
                D = II(D,  A,  B,  C,  M[m[j+48]],  S[j+48],  t[j+48])
            if (j % 4 == 2):
                C = II(C,  D,  A,  B,  M[m[j+48]],  S[j+48],  t[j+48])
            if (j % 4 == 3):
                B = II(B,  C,  D,  A,  M[m[j+48]],  S[j+48],  t[j+48])

    A = (A + init_A) & 0xFFFFFFFF
    B = (B + init_B) & 0xFFFFFFFF
    C = (C + init_C) & 0xFFFFFFFF
    D = (D + init_D) & 0xFFFFFFFF

    answer = ""
    print("循环结束后的ABCD",hex(A),hex(B),hex(C),hex(D))
    for register in [A,  B,  C,  D]:
        register = hex(register)[2:]
        for i in range(8,  0,  -2):
            answer += str(register[i - 2:i])
    print(len(answer))
    print("32位加密结果位",answer)
if __name__ =='__main__' :
    main()
