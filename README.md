# 创新创业实践课程作业
(1)小组成员(未组队，仅一人)：李宣仪 github账户名为xymthz  
(2)所做项目：  
   Project1: SM3 birthday attack  (全部完成)  
   Project2: SM3 长度扩展攻击      (全部完成)   
注：两个项目的SM3算法代码部分实现参考博客：https://blog.csdn.net/weixin_44932880/article/details/118385226

## Project1: SM3 birthday attack
对应代码：Project1.py  
运行环境建议IDLE(python 3.8 64-bit版本)，其他也行，一些网页版python在线运行也可以

SM3密码Hash算法输出Hash值的长度为256比特。如果只考虑SM3输出的前n bits，利用生日攻击，要使至少找到一对碰撞的概率大于0. 5，则选取的随机输入数量至少为![1](http://latex.codecogs.com/svg.latex?2^{n/2})。考虑的n越大，需要的输入越多。  
比如，考虑SM3输出的前32bits，则至少需要![2](http://latex.codecogs.com/svg.latex?2^{16})个输入能以0.5的概率找到一对碰撞：
![image](https://github.com/xymthz/homework/blob/main/images/Project1_%E5%9B%BE%E7%89%871.png)
![image](https://github.com/xymthz/homework/blob/main/images/Project1_%E5%9B%BE%E7%89%872.png)
这里time 计算运行所需时间的单位为秒。
本次运行中，使用了![3](http://latex.codecogs.com/svg.latex?2^{17})个输入，以提高找到碰撞的概率。不过，如果要找到特定消息m1（输出为SM3(m1)）的碰撞，并使其找到的概率不小于0. 5，则至少需要选取的随机输入数量为![2](http://latex.codecogs.com/svg.latex?2^{n-1})。随机找到一对碰撞的难度，比较找到一个固定结果H(x)的碰撞的难度要小很多。


## Project2: SM3 长度扩展攻击
对应代码：Project2.py  
运行环境建议IDLE(python 3.8 64-bit版本)，其他也行，一些网页版python在线运行也可以

对随机选取的字符串m进行长度扩展攻击，m1是长度扩展的字符。  
首先，攻击时，m是未知的，SM3(m)的值和m的长度是已知的。先根据原消息的长度和m1构造消息，由于不知道m的值，只知道m的长度，所以m部分可以用等长的任意字符串m*代替(如用’a')。随后进行padding，再将附加信息放在后面，消息就构造完成了。由SM3(m)值作为初始向量iv来加密m*||padding后面新附加的部分,得到新的hash值。  
![image](https://github.com/xymthz/homework/blob/main/images/Project2_%E5%9B%BE%E7%89%871.png)
![image](https://github.com/xymthz/homework/blob/main/images/Project2_%E5%9B%BE%E7%89%872.png)
验证我们得到的hash值是否正确：在已知原消息m的情况下按正常流程求SM3(m||padding||m1)，与之前通过SM3(m)和m1求得的hash值对比，如果相同，则长度扩展攻击成功。  
注：python代码中，s2m2b函数是SM3正常进行数据填充的函数，s2m2b_1函数则实现了正常对m进行数据填充后再拼接m1再数据填充。SM3函数是正常的SM3加密，只有一个参数m；SM3_1函数是求SM3(m||padding||m1)；有两个参数m和m1。


