# 创新创业实践课程作业
## Project1: SM3 birthday attack

SM3密码Hash算法输出Hash值的长度为256比特。如果只考虑SM3输出的前n bits，利用生日攻击，要使至少找到一对碰撞的概率大于0. 5，则选取的随机输入数量至少为![1](http://latex.codecogs.com/svg.latex?2^{n/2})。考虑的n越大，需要的输入越多。  
比如，考虑SM3输出的前32bits，则至少需要![2](http://latex.codecogs.com/svg.latex?2^{16})个输入能以0.5的概率找到一对碰撞：
![image](https://github.com/xymthz/homework/blob/main/images/Project1_%E5%9B%BE%E7%89%871.png)
![image](https://github.com/xymthz/homework/blob/main/images/Project1_%E5%9B%BE%E7%89%872.png)
这里time 计算运行所需时间的单位为秒。
本次运行中，使用了![3](http://latex.codecogs.com/svg.latex?2^{17})个输入，以提高找到碰撞的概率。不过，如果要找到特定消息m1（输出为SM3(m1)）的碰撞，并使其找到的概率不小于0. 5，则至少需要选取的随机输入数量为![2](http://latex.codecogs.com/svg.latex?2^{n-1})。随机找到一对碰撞的难度，比较找到一个固定结果H(x)的碰撞的难度要小很多。


## Project2: SM3 长度扩展攻击
