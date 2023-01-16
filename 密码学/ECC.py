import math
def get_inv(a,b):
    for i in range (1 , b):
         if (i * a) % b == 1:
             return i
    return -1
#获得逆元
def gcd(a,b):
    if b:
        return gcd(b,a%b)
    else:
        return a
def getpandq(x1, y1, x2, y2, a, p):
    flag = 1

    if x1 == x2 and y1 == y2:
        fenzi = 3 * (x1 ** 2) + a
        fenmu = 2 * y1
    else:
        fenzi = y2 - y1
        fenmu = x2 - x1
        if fenzi * fenmu < 0:
            flag = 0
            fenzi = abs(fenzi)
            fenmu = abs(fenmu)


    temp = gcd(fenzi, fenmu)
    fenzi = fenzi / temp
    fenmu = fenmu / temp

    k = fenzi * get_inv(fenmu, p)%p

    if flag == 0:
        k = -k
    k = k % p

    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return x3,y3
def rank(x0,y0,a,p):
    x1 = x0
    y1 = (-1*y0) % p
    x2 = x0
    y2 = y0
    countnum = 1
    while True :
        countnum += 1
        x3,y3 = getpandq(x2,y2,x0,y0,a,p)
        if x3 == x1 and y3 == y1 :
            return countnum + 1
        x2 = x3
        y2 = y3
#获取椭圆曲线的阶
def getset(a, b, p):
    print('输出所有生成元和阶')
    for i in range (1, p):
        sum = (i ** 3 + a * i + b) % p
        for j in range (0 , p):
            temp = (j ** 2) % p
            if temp == sum :
                print('x=','y=',i,j)
                print('rank=', rank(i, j, a, p))
def getKey(Gx , Gy ,key,a,p):
    x1 = Gx
    y1 = Gy
    while key != 1:
        x1, y1 = getpandq(x1, y1, Gx, Gy, a, p)
        key -= 1
    return x1, y1
def is_sqr(x):
    r = int(math.sqrt(x))
    if( r * r == x):
        return True
    else:
        return False
def transpoint(P , a , b, r,p):
    x = P * r
    temp = x**3 + a*x + b
    while(is_sqr(temp%p)==False):
        x+=1
        temp = x ** 3 + a * x + b
    return x , int(math.sqrt(temp%p))
def intlen(x):
    countnum = 0
    while x != 0 :
        countnum+=1
        x = x//10
    return countnum
def main():
    #测试用例
    a=1
    b=7
    p=163
    print((4*(a**3)+27*(b**2))%p)
    #输出所有生成元和阶
    getset(a,b,p)

    Gx = int(input('请选择一个点作为G的横坐标：'))
    Gy = int(input('请选择一个点作为G的纵坐标：'))
    G_rank = rank(Gx,Gy,a,p)
    print('G的阶为：',G_rank)
    #用户A生成私钥

    d = int(input('输入一个小于阶的数作为私钥d：（推荐选取30到50之间的数）'))

    #生成公钥Q
    P_x,P_y = getKey(Gx, Gy, d, a, p)
    # 加密选取的随机数
    r = int(input('输入一个随机数'))
    #获取明文
    plaintext = int(input('请输入你要加密的明文数字'))
    plainlength = intlen(plaintext)
    length = plainlength
    #对加密数字进行分组
    P = [0]*length
    while plaintext != 0 :
        temp1 = plaintext % 10
        P[length-1] = temp1
        length -= 1
        plaintext = plaintext // 10
    #转换成点
    print(P)
    P_point = []
    for j in range(0,plainlength):
        t17,t32 = transpoint(P[j],a,b,r,p)
        P_point.append([t17,t32])
    print(P_point)
    # 加密过程
    c=[]
    for k in range(plainlength):
        c1x, c1y = getKey(Gx, Gy, r, a, p)
        tempx, tempy = getKey(P_x, P_y, r, a, p)
        temp1x, temp1y = P_point[k]
        c2x, c2y = getpandq(temp1x, temp1y, tempx, tempy, a, p)
        c.append([c1x, c1y, c2x, c2y])
    print("密文为", c)

    #解密
    detxt = []
    for l in range(plainlength):
        d1x, d1y, d2x, d2y = c[l]
        temp1x,temp1y = getKey(d1x, d1y, d, a, p)
        temp1y = (-1*temp1y) % p
        d2x, d2y = getpandq(d2x,d2y,temp1x,temp1y, a, p)
        detxt.append([d2x,d2y])
    print("解密结果为",detxt)
if __name__ =='__main__' :
    main()

