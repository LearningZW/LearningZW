
#==============================
#author : VinChang
# FileName:getGraph.py
#date : 2021/6/15 21:24
#==============================
#_*_ coding:utf-8 _*_

import numpy as np
import networkx as nx
from getMatrix import getMatrix


#将矩阵转化成graph
def getGraph (matrix):
    graph = {}
    for i in range (1,matrix.shape [0]):  # 遍历矩阵行向量
        value = []

        for j in range (1,matrix.shape [1]):  # 遍历矩阵列向量
            if matrix [i] [j] != 0:
                value.append (j)
                graph [i] = value

    return graph

print(getGraph(getMatrix()))
