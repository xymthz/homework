#Project1: SM3 birthday attack

import re
import random
import string
import time
from collections import Counter

def cut_text(text,lenth):  #数据按间距分组划分iv向量
    textArr = re.findall('.{'+str(lenth)+'}', text)
    textArr.append(text[(len(textArr)*lenth):])
    return textArr
def zy(n,k):        #循环左移k位,共32比特
    k=k%32
    b=str(bin(n))
    b=b.split('0b')[1]
    b=(32-len(b))*'0'+b
    return int(b[k:]+b[:k],2)

def s2m2b(s):#字符串s 转化为二进制字符串m & 数据m填充,分组b[i]
    r = ""
    x = ""
    for i in s:
        l = 8 - len((x + bin(ord(i))).split('0b')[1]) % 8
        r = r + l * '0' + (x + bin(ord(i))).split('0b')[1]
    k=512-(64+(len(r)+1))%512
    out=r+'1'+k*'0'
    length=bin(len(r)).split('0b')[1]
    t=64-len(length)
    out=out+t*'0'+length
    out=cut_text(out,512)
    return out
def T(j):
    if j<16:
        T =int('0x79cc4519',16)
    else:
        T =int('0x7a879d8a',16)
    return T
def FF(x,y,z,j):  #布尔函数1
    if j<=15:
        return x^y^z
    else:
        return (x&y)|(y&z)|(x&z)
def GG(x,y,z,j):    #布尔函数2
    if j<=15:
        return x^y^z
    else:
        return (x&y)|(~x&z)

def p0(x):  #置换函数1，式中X为字
    return x^(zy(x,9))^(zy(x,17))
def p1(x):  #置换函数2，式中X为字
    return x^(zy(x,15))^(zy(x,23))

def cf(v,b):
    w = cut_text(b, 32)
    w2 = []
    for j in range(16):
        w[j]=int(w[j],2)
    del w[16]
    for j in range(16, 68):
        x = p1(w[j - 16] ^ w[j - 9] ^ zy(w[j - 3] ,15)) ^ zy(w[j - 13] ,7) ^ w[j - 6]
        w.append(x)
    for j in range(64):
        x = w[j] ^ w[j + 4]
        w2.append(x)
        
    A=cut_text(v,8)
   
    for i in range(8):
        A[i]=int(A[i],16)
    for j in range(64):
        ss1=zy((zy(A[0],12)+A[4]+zy(T(j),j))%(2**32),7)%(2**32)
        ss2=(ss1^zy(A[0],12))%(2**32)
        tt1=(FF(A[0],A[1],A[2],j)+A[3]+ss2+w2[j])%(2**32)
        tt2=(GG(A[4],A[5],A[6],j)+A[7]+ss1+w[j])%(2**32)
        A[3]=A[2]
        A[2]=zy(A[1],9)
        A[1]=A[0]
        A[0]=tt1
        A[7]=A[6]
        A[6]=zy(A[5],19)
        A[5]=A[4]
        A[4]=p0(tt2)
        
    a=''
    for i in range(8):
        A[i]=str(hex(A[i])).split('0x')[1]
        k=8-len(A[i])
        a=a+k*'0'+A[i]
    v1=int(a,16)^int(v,16)
    v1=hex(v1).split('0x')[1]
    if len(v1)<64:
        v1="0"*(64-len(v1))+str(v1)
    # print(v1,"v1")
    return v1

def SM3(m):
    iv='7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
    plain = m
    B=s2m2b(plain)
    for b in B:
        if b!='':
            iv=cf(iv,b)
    return(iv)


#随机生成消息m，寻找一对碰撞。使用简化的SM3，只考虑输出的前32bits,则以0.5的概率得到一对碰撞，至少需要的输入个数为2^16
def birthday_attack():
    n=2**17 #所需输入个数不少于2^16
    list1=[] #消息
    list2=[] #简化的SM3输出（前32bits）
    x1=0
    x2=0
    c=0
    
    t1=time.time()
    
    for i in range(n):
        m=''.join(random.sample(string.ascii_letters + string.digits, 15))#消息长可设置
        list1.append(m)
        list2.append(SM3(m)[0:8])
    count=Counter(list2)
    for k,v in count.items():
        if v>1:
            print("找到了一对碰撞：")
            c=k
            break
    if c==0:
        print("本次运气不好，没找到碰撞")
    else:
        t2=time.time()
        
        x1=list2.index(c)
        list2[x1]=0
        x2=list2.index(c)
        print(list1[x1],'与',list1[x2],'的SM3输出的前32bits相同')
        print("它们经SM3输出的hash值分别为：")
        print(SM3(list1[x1]))
        print(SM3(list1[x2]))
        
        print("time:",t2-t1)
            

birthday_attack()

































