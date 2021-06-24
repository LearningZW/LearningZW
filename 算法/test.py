import random

def DFS(graph,s):#图  s指的是开始结点
    #需要一个队列
    cluster=[]
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
            else:
               cluster.append([].append(w))




graph={
    'A':['B','C'],
    'B':['A','C','D'],
    'C':['A','B','D','E'],
    'D':['B','C','E','F'],
    'E':['C','D'],
    'F':['D']
}
print(DFS(graph,"A"))