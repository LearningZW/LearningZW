#==============================
#author : VinChang
# FileName:getMatrix.py
#date : 2021/6/9 8:07
#==============================
#_*_ coding:utf-8 _*_
import numpy as np

# data = np.loadtxt('D:/研究生/课题文件/门级电路划分算法研究/输入输出文件/gv_matrix.txt')

# z=pd.read_table('D:/研究生/课题文件/门级电路划分算法研究/输入输出文件/gv_matrix.txt', sep='\s+')

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

if __name__=='__main__':
    z=getMatrix()
    print(z.shape[1])
