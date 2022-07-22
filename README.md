# 创新创业实践课程作业
## Project1: SM3 birthday attack

SM3密码Hash算法输出Hash值的长度为256比特。  
（1）如果只考虑SM3输出的前n bits，利用生日攻击，要使至少找到一对碰撞的概率大于0. 5，则选取的随机输入数量至少为![1](http://latex.codecogs.com/svg.latex?2^{n/2})。考虑的n越大，需要的输入越多。   
比如，考虑SM3输出的前32bits，则至少需要216个输入能以0.5的概率找到一对碰撞：
