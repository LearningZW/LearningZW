import networkx as nx
import matplotlib.pyplot as plt
from getMatrix import *

G = nx.Graph()

type(G)
plt.figure(figsize=(10, 20))


def getConnections(self):
    connections=[]
    for i in range(getMatrix().shape[0]):
       for j in range(getMatrix().shape[1]):
           if getMatrix()[i][j]==1:
               connections.append([i,j])
    return connections

G=getConnections(getMatrix())

nx.draw(G,with_labels=True)


if __name__=='__main__':
    plt.show()
