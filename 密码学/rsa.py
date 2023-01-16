import random
import binascii

def gcd(m, n):
    if (n == 0) :
        return m
    else:
        return gcd(n , m%n)

def ex_gcd(m , b ):
    if m < b:
        t = m
        m = b
        b = t
    x1, x2, x3 = 1, 0, m
    y1, y2, y3 = 0, 1, b
    while True:
        if y3 == 0:
            return 'None'
            break
        elif y3 == 1:
            return y2 % m
            break
        else:
            q = x3 // y3
            t1, t2, t3 = x1 - q * y1, x2 - q * y2, x3 - q * y3
            x1, x2, x3 = y1, y2, y3
            y1, y2, y3 = t1, t2, t3

'''def is_prime(m)
    for i in range(2,m):
        if m % i ==0:
            return False
            break
    return True'''

#素性测试

def miller_rabin(num):
    s = num - 1
    t = 0
    while s % 2 == 0:
        s = s // 2
        t += 1

    for number in range(20):
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                else:
                    i = i + 1
                    v = (v ** 2) % num
    return True

#新版
def is_prime(m):
    if m < 2:
        return m

    prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
                101, 103, 107,109, 113, 127, 131, 137, 139, 149, 151,157, 163, 167, 173, 179, 181, 191, 193,197,
                199, 211, 223, 227, 229, 233, 239,241, 251, 257, 263, 269, 271, 277, 281,283, 293, 307, 311, 313,
                317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
                443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571,
                577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
                701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829,
                839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977,
                983, 991, 997]

    if m in prime_list:
        return True

    for i in prime_list:
        if m % i == 0:
            return False
            break

    return miller_rabin(m)
#平方求幂模
def repeatmodn(a, b, n):
    result = 1
    while b != 0:
        if (b & 1) == 1:
            result = (result * a) % n
        a = (a * a) % n
        b >>= 1
    return result

def create():
    while True:
        n = random.randrange(2**49, 2**50)
        if is_prime(n):
            return n

#rsa加解密
def rsa(a , b ,n) :
   return repeatmodn(a, b, n)
#计算长度
def length(a):
    i = 0
    while a>0 :
        i +=1
        a = a//10
    return i

def main():
    #加密所需
    p = create()
    q = create()
    while q == p:
        q = create()
    n = p * q
    e = 65537
    oula = (p - 1) * (q - 1)
    d = ex_gcd(e, oula)


    #明文转换与分组
    plaintext = 'Lakers never die!'
    print('plaintext =', plaintext)
    plaintext = plaintext.encode('utf-8')
    plaintext = int(binascii.hexlify(plaintext),16)
    len = length(plaintext)#获取十进制位数，以10位为一组
    len1 = len % 10
    len2 = len // 10
    len3 = len2+1
    plainlist = [0] * (len3)
    cipherlist1 = [0] * (len3)
    cipherlist2 = [0] * (len3)
    decryptlist1 = [0] * (len3)
    decryptlist2 = [0] * (len3)
    plainlist[len2] = plaintext % pow(10 , len1)
    plaintext = plaintext // 10
    len2 -= 1

    while plaintext != 0:
        plainlist[len2] = plaintext % pow(10,10)
        plaintext = plaintext // pow(10,10)
        len2 -= 1

    for i in range(len3):
        cipherlist1[i] = rsa(plainlist[i],e,n)
        cipherlist2[i] = rsa(plainlist[i],d,n)
    print("加密结果为", cipherlist1)
    print("签名结果为",cipherlist2)
    for j in range(len3):
        decryptlist1[j] = rsa(cipherlist1[j],d,n)
        decryptlist2[j] = rsa(cipherlist2[j],e,n)
    print("解密结果为", decryptlist1)
    print("验证签名结果为", decryptlist2)

    decryptxt1 = 0
    decryptxt2 = 0
    len3-=1
    for k in range(len3):
        decryptxt1 = decryptxt1*pow(10,10) + decryptlist1[k]
        decryptxt2 = decryptxt2 * pow(10, 10) + decryptlist2[k]
    decryptxt1 = decryptxt1 *pow(10,len1) + decryptlist1[len3]
    decryptxt2 = decryptxt2 * pow(10, len1) + decryptlist2[len3]


    text1 = binascii.unhexlify(hex(decryptxt1)[2:])
    text2 = binascii.unhexlify(hex(decryptxt2)[2:])
    print('解密文本为',text1)
    print('验证签名文本为',text2)
if __name__ == "__main__":
    main()
