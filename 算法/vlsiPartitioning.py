import sys
import numpy as np
import networkx as nx
from collections import namedtuple,deque

sys.path.append (r'D:/python_pycharm/pycharm_films')

"""
所涉及的参数预览：
1，matrix--描述邻接矩阵
2，graph--描述单个顶点与其余顶点之间的联系

"""


# 输入VLSI矩阵
def getMatrix ():
    f = open ('D:/研究生/课题文件/门级电路划分算法研究/输入输出文件/gv_matrix.txt')  # 打开数据文件文件
    row0 = f.readline ().split ('\t')  # 导入第一行列表
    row0.pop ()  # 删除列表后多出的''
    row = len (row0)
    f.seek (0,0)  # 用于重置指针到f文件开头
    lines = f.readlines ()  # 把全部数据文件读到一个列表lines中
    matrix = np.zeros ((len (lines)+1,row),dtype=int)  # 先创建一个 与txt文本同型的全零方阵matrix，并且数据的类型设置为int
    matrix_row = 0  # 表示矩阵的行，从0行开始
    for line in lines:  # 把lines中的数据逐行读取出来
        list_matrix = line.split ('\t')  # 处理逐行数据：strip表示把头尾的'\n'去掉，split表示以空格来分割行数据，然后把处理后的行数据返回到list列表中
        list_matrix.pop ()  # 删除最后一个’‘
        matrix [matrix_row:] = list_matrix [0:row]  # 把处理后的数据放到方阵A中。list[0:row]表示列表的0,1,2,...row列数据放到矩阵matrix中的matrix_row行
        matrix_row += 1
    for i in range (matrix.shape [0]-1):  #矩阵行
            matrix [i] [i] = 0
    return matrix



# 将matrix转换成graph形式
'''
graph={'A':['B','C'],
	   'B':['A','C','D'],
	   'C':['A','B','D','E'],
	   'D':['B','C','E','F'],
	   'E':['C','D'],
	   'F':['D']
}
'''



def bfs (start_node,end_node,graph):  # 开始节点  目标节点 图字典
    node = namedtuple ('node','name, from_node')  # 使用namedtuple定义节点，用于存储前置节点
    search_queue = deque ()  # 使用双端队列，这里当作队列使用，根据先进先出获取下一个遍历的节点
    name_search = deque ()  # 存储队列中已有的节点名称
    visited = {}  # 存储已经访问过的节点

    search_queue.append (node (start_node,None))  # 填入初始节点，从队列后面加入
    name_search.append (start_node)  # 填入初始节点名称
    path = []  # 用户回溯路径
    queue_bsf=[]
    print ('开始搜索...')
    while search_queue:  # 只要搜索队列中有数据就一直遍历下去
        print ('待遍历节点: ',name_search)
        current_node = search_queue.popleft ()  # 从队列前边获取节点，即先进先出，这是BFS的核心
        name_search.popleft ()  # 将名称也相应弹出
        if current_node.name not in visited:  # 当前节点是否被访问过
            print ('当前节点: ',current_node.name,end=' | ')
            queue_bsf.append(current_node.name)
            if current_node.name == end_node:  # 退出条件，找到了目标节点，接下来执行路径回溯和长度计算
                pre_node = current_node  # 路径回溯的关键在于每个节点中存储的前置节点
                while True:  # 开启循环直到找到开始节点
                    if pre_node.name == start_node:  # 退出条件：前置节点为开始节点
                        path.append (start_node)  # 退出前将开始节点也加入路径，保证路径的完整性
                        break
                    else:
                        path.append (pre_node.name)  # 不断将前置节点名称加入路径
                        pre_node = visited [pre_node.from_node]  # 取出前置节点的前置节点，依次类推
                break
            else:
                visited [current_node.name] = current_node  # 如果没有找到目标节点，将节点设为已访问，并将相邻节点加入搜索队列，继续找下去
                for node_name in graph [current_node.name]:  # 遍历相邻节点，判断相邻节点是否已经在搜索队列
                    if node_name not in name_search:  # 如果相邻节点不在搜索队列则进行添加
                        search_queue.append (node (node_name,current_node.name))
                        name_search.append (node_name)

    print ('搜索完毕:',queue_bsf)  # 打印搜索结果


# if __name__ == '__main__':
#     print(getMatrix(),"\n",getMatrix().shape)
#     print (bfs(1,30,getGraph(getMatrix())))

