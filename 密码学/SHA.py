K = [
    0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f, 0xe9b5dba58189dbbc,
    0x3956c25bf348b538, 0x59f111f1b605d019, 0x923f82a4af194f9b, 0xab1c5ed5da6d8118,
    0xd807aa98a3030242, 0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
    0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235, 0xc19bf174cf692694,
    0xe49b69c19ef14ad2, 0xefbe4786384f25e3, 0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65,
    0x2de92c6f592b0275, 0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
    0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f, 0xbf597fc7beef0ee4,
    0xc6e00bf33da88fc2, 0xd5a79147930aa725, 0x06ca6351e003826f, 0x142929670a0e6e70,
    0x27b70a8546d22ffc, 0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
    0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6, 0x92722c851482353b,
    0xa2bfe8a14cf10364, 0xa81a664bbc423001, 0xc24b8b70d0f89791, 0xc76c51a30654be30,
    0xd192e819d6ef5218, 0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
    0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99, 0x34b0bcb5e19b48a8,
    0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb, 0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3,
    0x748f82ee5defb2fc, 0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
    0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915, 0xc67178f2e372532b,
    0xca273eceea26619c, 0xd186b8c721c0c207, 0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178,
    0x06f067aa72176fba, 0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
    0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c,
    0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817]

def int2bin(n,  count=24):
    return "".join([str((n >> y) & 1) for y in range(count-1,  -1,  -1)])

def ch(x, y, z):
    return ((x & y) ^ ( (~x) & z)) & 0xFFFFFFFFFFFFFFFF

def maj(x, y, z):
    return ((x & y) ^ (x & z) ^ (y & z)) & 0xFFFFFFFFFFFFFFFF

def rol(s, t):
    s = (s >> t) | (s << (64-t)) & 0xFFFFFFFFFFFFFFFF
    return s

def shr(s, t):
    s = (s << t) & 0xFFFFFFFFFFFFFFFF
    return s

def kesi1(x):
    result = rol(x, 1) ^ rol(x, 8) ^ shr(x, 7)
    result = result & 0xFFFFFFFFFFFFFFFF
    return result

def kesi0(x):
    result = rol(x, 19) ^ rol(x, 61) ^ shr(x, 6)
    result = result & 0xFFFFFFFFFFFFFFFFF
    return result

def expand_w(a, b, c, d):
    result = kesi1(a) + b + kesi0(c) + d
    result = result & 0xFFFFFFFFFFFFFFFF
    return result

def sigma0(a):
    result = rol(a, 28) ^ rol(a, 34) ^ rol(a, 39)
    result = result & 0xFFFFFFFFFFFFFFFF
    return result

def sigma1(a):
    result = rol(a, 14) ^ rol(a, 18) ^ rol(a, 41)
    result = result & 0xFFFFFFFFFFFFFFFF
    return result

def roundfun(a, b, c, d, e, f, g, h, wt, kt):
    temp1 = (h + ch(e, f, g) + sigma1(e) + wt + kt) & 0xFFFFFFFFFFFFFFFF
    temp2 = (sigma0(a) + maj(a, b, c)) & 0xFFFFFFFFFFFFFFFF
    h = g
    g = f
    f = e
    e = (d + temp1) & 0xFFFFFFFFFFFFFFFF
    d = c
    c = b
    b = a
    a = (temp1 + temp2) & 0xFFFFFFFFFFFFFFFF
    return a, b, c, d, e, f, g, h

def fill(x):
    text = ""
    for i in range(len(x)):
        c = int2bin(ord(x[i]),  8)
        text += c

    if (len(text) % 1024 != 896):
        if ((len(text) + 1) % 1024 != 896):
            text += '1'
        while (len(text) % 1024 != 896):
            text += '0'

    length = len(x) * 8
    if (length < 512):
        length = int2bin(length,  8)
    else:
        length = int2bin(length,  16)
        temp = length[8:12] + length[12:16] + length[0:4] + length[4:8]
        length = temp

    text += length
    while (len(text) % 1024 != 0):
        text += '0'
    return text

def main():

    #初始向量
    h0 = 0x6A09E667F3BCC908
    h1 = 0xBB67AE8584CAA73B
    h2 = 0x3C6FE373FE94F82B
    h3 = 0xA54FF53A5F1D36F1
    h4 = 0x510E527FADE682D1
    h5 = 0x9B05688C2B3E6C1F
    h6 = 0x1F83D9ABFB41BD6B
    h7 = 0x5BE0CD19137E2179

    #初始赋值
    a = h0
    b = h1
    c = h2
    d = h3
    e = h4
    f = h5
    g = h6
    h = h7
    print(K)
    messsage = "Lakers never die!!!!!"
    filled_txt = fill(messsage)
    print(filled_txt)
    length = len(filled_txt)
    M = []
    W = [0] * (length//64)
    expanded_W = [0]*80
    #分割为64bit
    for i in range(0, length, 64):
        num = ""
        for j in range(0, len(filled_txt[i:i + 64]), 4):
            temp = filled_txt[i:i + 64][j:j + 8]
            temp = hex(int(temp, 2))
            num += temp[2]
        num_tmp = ""
        for j in range(16, 0, -2):
            temp = num[j - 2:j]
            num_tmp += temp

        num = ""
        for j in range(len(num_tmp)):
            num += int2bin(int(num_tmp[j], 16), 4)
        temp = int(num, 2)
        M.append(temp)
    print(M)
    for k in range(0, length//1024):
        for j in range(0, 16):
            W[16*k+j] = M[16*k + j]
        for j in range(0, 80):
            if j < 16 :
                expanded_W[j] = W[16*k+j]
            else:
                expanded_W[j] = expand_w(expanded_W[j-2], expanded_W[j-7], expanded_W[j-15], expanded_W[j-16])
        for j in range(0, 80):
            a, b, c, d, e, f, g, h = roundfun(a, b, c, d, e, f, g, h, expanded_W[j], K[j])

    h0 = (h0 + a) & 0xFFFFFFFFFFFFFFFF
    h1 = (h1 + b) & 0xFFFFFFFFFFFFFFFF
    h2 = (h2 + c) & 0xFFFFFFFFFFFFFFFF
    h3 = (h3 + d) & 0xFFFFFFFFFFFFFFFF
    h4 = (h4 + e) & 0xFFFFFFFFFFFFFFFF
    h5 = (h5 + f) & 0xFFFFFFFFFFFFFFFF
    h6 = (h6 + g) & 0xFFFFFFFFFFFFFFFF
    h7 = (h7 + h) & 0xFFFFFFFFFFFFFFFF

    answer = ""
    for register in [h0,  h1,  h2,  h3, h4, h5, h6, h7]:
        register = hex(register)[2:]
        for i in range(16,  0,  -2):
            answer += str(register[i - 2:i])
    #938e8b51a10753b739a2d1fb4a229bfb1f594342c2c1fc5c68db1392c22586c05ec69f99734c63064239f32ff9008e841ba6caaa8fccb4f59720c01a7e5b5acd
    print(len(answer))
    print("128位加密结果位",answer)

if __name__ == '__main__':
    main()
