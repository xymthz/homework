#Project2： SM3 长度扩展攻击

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

def s2m2b_1(s,s1):#字符串s 转化为二进制字符串m & 数据m填充,分组b[i]
    s=s2m2b(s)
    r = ""
    x = ""
    for i in s1:
        l = 8 - len((x + bin(ord(i))).split('0b')[1]) % 8
        r = r + l * '0' + (x + bin(ord(i))).split('0b')[1]
    t=""
    for i in s:
        t=t+i
    r=t+r
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

def SM3_1(m,m1):
    iv='7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
    B=s2m2b_1(m,m1)
    for b in B:
        if b!='':
            iv=cf(iv,b)
    return(iv)




#m,m1可修改为其他值,进行测试

##m="222"
##m1="333"
m="d2XBYjIQqbsZOeNabdffffegdddyiiongjgjhgjdhjh111233487896hhhhhhhhhhhhh77777777777777777"
m1="1234"
m_len=len(m)

print("对m进行长度扩展攻击，m为",m,"，将在填充后的m后面添加m1,m1为",m1,"\n")
iv=SM3(m)
print("首先,攻击时，m是未知的，SM3(m)的值是已知的,\nSM3(m)=",iv)
#构造消息
m2='a'*m_len
A=s2m2b(m2)
m_len1=len(A)-1
B=s2m2b_1(m2,m1)
B=B[m_len1:]
for b in B:
    if b!='':
        iv=cf(iv,b)
print("先根据原消息的长度(用任意字符串填充，填充内容为m*)和m1构造消息，由SM3(m)作为初始向量iv来加密m*||padding后面新附加的部分,得到新的hash值为：\n",iv)


print("\n验证我们得到的hash值是否正确:\n在已知原消息m的情况下按正常流程求SM3(m||padding||m1),结果为：")
print(SM3_1(m,m1))
print("与之前通过SM3(m)和m1求得的hash值相同,因此长度扩展攻击成功")



