from typing import List, Tuple
from getMatrix import *
import time


class Tarjan:
    # 求无向连通图的桥
    def getCuttingPointAndCuttingEdge(edges: List[Tuple]):
        link, dfn, low = {}, {}, {}# link为字典邻接表
        global_time = [0]
        for a, b in edges:
            if a not in link:
                link[a] = []
            if b not in link:
                link[b] = []
            link[a].append(b)#无向图
            link[b].append(a)#无向图
            dfn[a], dfn[b] = 0, 0
            low[a], low[b] = 0, 0

        cutting_points, cutting_edges = [], []
 
        def dfs(cur, prev, root):
            global_time[0] += 1
            dfn[cur], low[cur] = global_time[0], global_time[0]
 
            children_cnt = 0
            flag = False
            for next in link[cur]:
                if next != prev:
                    if dfn[next] == 0:
                        children_cnt += 1
                        dfs(next, cur, root)
 
                        if cur != root and low[next] >= dfn[cur]:
                            flag = True
                        low[cur] = min(low[cur], low[next])
 
                        if low[next] > dfn[cur]:
                            cutting_edges.append([cur, next] if cur < next else [next, cur])
                    else:
                        low[cur] = min(low[cur], dfn[next])
 
            if flag or (cur == root and children_cnt >= 2):
                cutting_points.append(cur)
 
        dfs(edges[0][0], None, edges[0][0])
        return cutting_points, cutting_edges

    def getConnections(self):
        connections=[]
        for i in range(getMatrix().shape[0]):
           for j in range(getMatrix().shape[1]):
               if getMatrix()[i][j]==1:
                   connections.append([i,j])
        return connections
 
class Solution:
    def criticalConnections(self, connections: List[List[int]]) -> str:
        edges = [(a, b) for a, b in connections]
        cutting_dots, cutting_edges = Tarjan.getCuttingPointAndCuttingEdge(edges)
        return "割边数为：{1}\n割边集为：\n{0},\n" \
                "{4}\n"\
               "割点数为：{3}\n割点集为：\n{2}),"\
                .format([[a, b] for a, b in cutting_edges],len([[a, b] for a, b in cutting_edges]),
                        cutting_dots,len(cutting_dots),
                        "==================================================================")


if __name__=='__main__':

    # connections = [[0,1],[1,2],[2,0],[1,3]]
    # n = 4
    # s = Solution()
    # result = s.criticalConnections(n,connections)
    # print(result)

    s_time=time.process_time()
    s = Solution()
    n=32
    T=Tarjan
    z=T.getConnections(self=getMatrix())
    result = s.criticalConnections(z)
    e_time=time.process_time()
    c_time=e_time-s_time
    print(result)
    print("花费时间：%ds"%c_time)

