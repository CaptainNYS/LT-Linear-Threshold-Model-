# -*- coding: utf-8 -*-
# Captain_N
import csv
import random
import numpy as np
import matplotlib .pyplot as plt

N = 769
start = [1,3,5,7,9,
         761,763,765,767,768
         ]#初始激活节点集
M=10#每一循环的遍历次数
#读取数据
print("读取数据")
with open('links.csv', encoding='utf-8') as f:
    data = csv.reader(f)
    network =np.zeros((33312,2),dtype=np.int64)#int64是numpy中引入的一个类，即 numpy.int64
    fluence = np.zeros((N, N), dtype=float)#初始化影响力矩阵（边的权重，节点之间有出边和入边）
    print(fluence.shape)
    for i, line in enumerate(data):#enumerate 将对象转为索引序列，可以同时获得索引和值。
        #print(line[0])  #matlab中节点标号1~769，python中节点标号0~768.
        network[i][0]=int(line[0])-1
        network[i][1]=int(line[1])-1
        #print(isinstance(network[i][0],int)) #检查变量类型
        fluence[int(network[i][0])][int(network[i][1])]=line[2]
    print(fluence[3][0])
#存储为邻接矩阵
# new_network =np.zeros((N,N),dtype=np.int64)
# for i in range(7624):
#     a= network[i][0]
#     b= network[i][1]
#     new_network[a][b]=1
#定义初始状态
print("定义初始状态")
state = np.zeros((N),dtype=np.int64)#初始化节点，1代表激活，0代表未激活
threshold=np.zeros((N))
print(threshold.shape)#(769,)
for n in range(N):
    threshold[n]=random.random()#定义社交网络中节点对某一新闻的阈值，随机独立
for i in range(len(start)):
    if i>=1:
        state[start[i]]=1 #初始化状态state
#起点备份，保证每次起点相同
old_state = state.copy()
#初始化传播M步遍历N节点的张量
c=np.zeros((M,N))
print(c.shape)
#开始循环

c[0]=old_state.copy()
#print(old_state)
new_state= old_state.copy()
activated=start
activated_num=len(start)
print(len(start))
print(len(activated))
print("开始循环")
#开始传播
for j in range(M-1):#29步后到达第30个状态
    print("开始第"+str(j)+"次传播")
    #顺次遍历节点
    for m in range(N):
        # 判断是否已经激活，如果激活则跳过
        if (new_state[m] == 0):
            sum_fluence=0
            #累加邻接激活节点对此节点的影响
            for n in range(N):
                if(new_state[n]==1):
                    sum_fluence+=fluence[m][n]
                #print(sum_fluence)
            if ((0.0511*sum_fluence)>=threshold[m]):
                new_state[m]=1
                activated.append(m)
                activated_num+=1
                print(activated)
            else:
                continue
        else:
            continue

    c[j + 1] = new_state.copy()
    print("第"+str(j)+"步传播激活节点一共为："+str(activated_num)+"个")
print(len(activated))
#统计每次循环每步激活节点占比，准备画图
s=np.zeros((M))
#mean_s=np.zeros((K))
for m in range(M):
    state =c[m]
    num =0
    for n in range(N):
        if (state[n]==1):
            num =num+1

    pdf = num/N
    s[m] = pdf
#出图
x_zhou=np.array(range (M))

plt.figure()

plt.plot(x_zhou,s)
plt.ylim((0,1))
plt.xlim((0,10))
plt.xticks(np.linspace(0, 10, 11))#构建等差数列
plt.yticks(np.linspace(0, 1, 11))
plt.legend(labels = ['activated1'], loc = 'best')
plt.xlabel('Time/step')
plt.ylabel('Node density')



plt .show()


