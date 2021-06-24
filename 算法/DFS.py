import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
'''
tarjan 能直接求出强连通分量,但必须是有向图
https://www.cnpython.com/pypi/tarjan
eg:
z={1:[2],2:[1,5],3:[4],4:[3,5],5:[6],6:[7],7:[8],8:[6,9],9:[]}
>>>tarjan(z)
>>>[[9], [8, 7, 6], [5], [2, 1], [4, 3]]
'''
from tarjan import * #import tarjan 会报错：TypeError: 'module' object is not callable

def getMatrix():
    f = open ('D:/研究生/课题文件/门级电路划分算法研究/输入输出文件/gv_matrix.txt')  # 打开数据文件文件
    row0 = f.readline().split ('\t')  # 导入第一行列表
    row0.pop()  # 删除列表后多出的''
    len_row = len(row0)
    f.seek (0,0)  # 用于重置指针到f文件开头
    lines = f.readlines ()  # 把全部数据文件读到一个列表lines中
    # 先创建一个 与txt文本同型的全零方阵matrix，并且数据的类型设置为int
    matrix = np.zeros ((len (lines)+1,len_row),dtype=int)
    matrix_row = 0  # 表示矩阵的行，从0行开始
    for line in lines:  # 把lines中的数据逐行读取出来
        # 处理逐行数据：strip表示把头尾的'\n'去掉，split表示以空格来分割行数据，然后把处理后的行数据返回到list列表中
        list_matrix = line.split ('\t')
        list_matrix.pop ()  # 删除最后一个’‘
        # 把处理后的数据放到方阵A中。list[0:row]表示列表的0,1,2,...row列数据放到矩阵matrix中的matrix_row行
        matrix[matrix_row:] = list_matrix [0:len_row]

        matrix_row += 1
    for i in range (matrix.shape [0]-1):  #矩阵行
            matrix [i][i] = 0
    return matrix


def getGraph (matrix):
    graph = {}
    for i in range (1,matrix.shape [0]):  # 遍历矩阵行向量
        value = []

        for j in range (1,matrix.shape [1]):  # 遍历矩阵列向量
            if matrix [i] [j] != 0:
                value.append (j)
                graph [i] = value

    return graph


# graph={
#     'A':['B','C'],
#     'B':['A','C','D'],
#     'C':['A','B','D','E'],
#     'D':['B','C','E','F'],
#     'E':['C','D'],
#     'F':['D']
# }

# print(getGraph(getMatrix()))
# print('------------------------------------')
# print(list(getGraph(getMatrix()).keys()))


def DFS(graph,s):#图  s指的是开始结点
    #需要一个队列
    stack=[]
    stack.append(s)
    seen=set()#看是否访问过
    seen.add(s)
    while len(stack)>0:
        #拿出邻接点
        vertex=stack.pop()#这里pop参数没有0了，最后一个元素
        nodes=graph[vertex]
        for w in nodes:
            if w not in seen:#如何判断是否访问过，使用一个数组
                stack.append(w)
                seen.add(w)
        print(vertex)


if __name__=="__main__":
    print(getMatrix())
    # print(getGraph(getMatrix()))