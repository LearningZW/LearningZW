# -*- coding: utf-8 -*-
import numpy as np
from FMalgorithm.mainP.Util import Cell, Net, Block
import sys
import logging


class FiducciaMattheyses:
    INITIAL_BLOCK = "A"  # 所有单元格最初所属的块
    r = 0.5  # 比率，用于捕获算法产生的最终分区的平衡准则

    def __init__(self):
        self.cell_array = {}
        self.net_array = {}
        self.pmax = 0  # 这将在input_routine中进行计算

        self.blockA = None  # 当调用输入例程时，它会被初始化(我们需要知道pmax)
        """:type blockA Block"""
        self.blockB = None  # 当调用输入例程时，它会被初始化(我们需要知道pmax)
        """:type blockB Block"""
        self.cutset = 0  # 被切割的集合数
        self.snapshot = None  # 这将保持FiducciaMattheyses在快照拍摄时的状态
        self.logger = logging.getLogger("FiducciaMattheyses")

    def take_snapshot(self):
        """
        对FiducciaMattheyses的当前状态进行快照
        """
        self.snapshot = self.cutset
        self.blockA.take_snapshot()
        self.blockB.take_snapshot()
        for cell in self.cell_array.values():
            cell.take_snapshot()
        for net in self.net_array.values():
            net.take_snapshot()

    def load_snapshot(self):
        """
        加载保存的FiducciaMattheyses快照，当前的FiducciaMattheyses状态将丢失
        """
        assert self.snapshot is not None
        self.cutset = self.snapshot
        self.blockA.load_snapshot()
        self.blockB.load_snapshot()
        for cell in self.cell_array.values():
            cell.load_snapshot()
        for net in self.net_array.values():
            net.load_snapshot()

    def input_routine(self, edge_matrix: np.ndarray, selection=None):
        """
        从表单的输入矩阵构造cell_array和net_array
        [[1, 1, 1, 0, 1],
         [1, 1, 1, 1, 0],
         [1, 1, 1, 0, 1],
         [0, 1, 0, 1, 1],
         [1, 0, 1, 1, 1]]
        其中1表示两个节点之间的一条边。
        在上面的示例中，节点0连接到1、2和4(通过查看表的第一行)
        如果选择不是None，则只考虑列表中指定的单元格。所有其他的
        edge_matrix中的单元格将被忽略
        :param 选择:不应被忽略的单元格列表
        :type selection: list
        :param edge_matrix: 如前所述，包含单元格边缘信息
        :type edge_matrix: np.ndarray
        """
        assert isinstance(edge_matrix, np.ndarray)
        if selection is None:
            Q = [i for i in range(edge_matrix.shape[0])]
        else:
            Q = selection
        net = 0
        for i in range(len(Q)):
            for j in range(i + 1, len(Q)):
                if edge_matrix[Q[i]][Q[j]] == 1:
                    self.__add_pair(Q[i], Q[j], net)
                    net += 1

        for cell in self.cell_array.values():
            if cell.pins > self.pmax:
                self.pmax = cell.pins

        self.blockA = Block("A", self.pmax, self)
        self.blockB = Block("B", self.pmax, self)

        for cell in self.cell_array.values():
            cell.block = self.blockA
            self.blockA.add_cell(cell)
        for net in self.net_array.values():
            net.blockA_ref = self.blockA
            net.blockB_ref = self.blockB
        self.compute_initial_gains()
        self.blockA.initialize()

    def __add_pair(self, i: int, j: int, net_n: int):
        """
        添加连接的节点对。将不存在的cell_i, cell_j, net添加到cell_array和
        净相应的数组。还添加了单元和网络之间的依赖关系
        """
        cell_i = self.__add_cell(i)
        cell_j = self.__add_cell(j)
        net = self.__add_net(net_n)

        cell_i.add_net(net)
        cell_j.add_net(net)
        net.add_cell(cell_i)
        net.add_cell(cell_j)

    def __add_cell(self, cell: int) -> Cell:
        """
        添加一个单元格到cell_array，如果它不存在，返回新创建的或现有的单元格
        """
        if cell not in self.cell_array:
            cell_obj = Cell(cell, FiducciaMattheyses.INITIAL_BLOCK)
            self.cell_array[cell] = cell_obj
        else:
            cell_obj = self.cell_array[cell]
        return cell_obj

    def __add_net(self, net: int) -> Net:
        """
        在net_array中添加一个net，如果它不存在，返回新创建的net或现有的net
        """
        if net not in self.net_array:
            net_obj = Net(net)
            self.net_array[net] = net_obj
        else:
            net_obj = self.net_array[net]
        return net_obj

    def get_base_cell(self) -> Cell:
        """
        找到基本单元。这是一个具有最大增益的单元格，如果移动到它，它也能提供最好的平衡
        如果不存在互补块，则为空
        """
        a = self.get_candidate_base_cell_from_block(self.blockA)
        b = self.get_candidate_base_cell_from_block(self.blockB)

        if a is None and b is None:
            return None
        elif a is None and b is not None:
            return b[0]
        elif a is not None and b is None:
            return a[0]
        else:  # both not None
            bfactor_a = a[1]
            bfactor_b = b[1]
            if bfactor_a < bfactor_b:
                return a[0]
            else:
                return b[0]

    def get_candidate_base_cell_from_block(self, block: Block):  # -> Tuple[Cell, float]
        """
        从满足基本单元格要求的指定块获取单元格，如果存在则为None
        在给定的块中没有这样的单元格吗
        """
        assert isinstance(block, Block)
        candidate_cell = block.get_candidate_base_cell()
        if candidate_cell is None:
            return None
        bfactor = self.get_balance_factor(candidate_cell)
        if bfactor is None:
            return None
        else:
            return candidate_cell, bfactor

    def get_balance_factor(self, cell: Cell):
        """
        首先使用平衡准则检查该单元格移动到互补块是否会导致a
        如果是这样，则返回abs(|A| - rW)，否则为None。这个值越接近零
        分区越接近预期(基于比率r)
        """
        if cell.block.name == "A":
            A = self.blockA.size - 1
            B = self.blockB.size + 1
        else:
            assert cell.block.name == "B"
            A = self.blockA.size + 1
            B = self.blockB.size - 1
        W = A + B
        smax = self.pmax
        r = FiducciaMattheyses.r
        if r * W - smax <= A <= r * W + smax:
            return abs(A - r * W)
        else:
            return None

    def is_partition_balanced(self) -> bool:
        """
        检查均衡条件，如果当前分区均衡，返回true
        """
        W = self.blockA.size + self.blockB.size
        smax = 1  # self.pmax
        r = FiducciaMattheyses.r
        A = self.blockA.size
        return r * W - smax <= A <= r * W + smax

    def compute_initial_gains(self):
        """
        计算所有单元的初始增益
        """
        for cell in self.cell_array.values():
            cell.gain = 0
            for net in cell.nets:
                if cell.block.name == "A":
                    if net.blockA == 1:
                        cell.gain += 1
                    if net.blockB == 0:
                        cell.gain -= 1
                else:
                    assert cell.block.name == "B"
                    if net.blockB == 1:
                        cell.gain += 1
                    if net.blockA == 0:
                        cell.gain -= 1
                if cell.bucket_num is not None:  # if None then this cell is in the free cell list
                    cell.yank()

    def initial_pass(self):
        """
        建立平衡分区的初始过程中，应该首先调用input_routine
        """
        assert self.blockA is not None
        assert self.blockB is not None

        assert self.blockA.size >= self.blockB.size
        while not self.is_partition_balanced():
            bcell = self.blockA.get_candidate_base_cell()
            assert bcell.block.name == "A"  # all cells initially belong to block A
            self.blockA.move_cell(bcell)

    def perform_pass(self):
        """
        执行一次完整的传递，直到没有更多的单元格能够移动，或者平衡条件不允许任何更多的移动。
        必须先调用input_routine()和initial_pass()函数
        """
        best_cutset = sys.maxsize

        self.compute_initial_gains()
        self.blockA.initialize()
        self.blockB.initialize()
        bcell = self.get_base_cell()
        while bcell is not None:
            if bcell.block.name == "A":
                self.blockA.move_cell(bcell)
            else:
                assert bcell.block.name == "B"
                self.blockB.move_cell(bcell)
            if self.cutset < best_cutset:
                best_cutset = self.cutset
                self.take_snapshot()

            bcell = self.get_base_cell()
        if self.snapshot is not None:
            self.load_snapshot()

    def find_mincut(self):
        """
        执行多次传球，直到没有更多的改进，保持最好的传球。
        必须先调用Input_routine()。
        返回分区的形式为:([1,3,5]，[2,4,6,7])
        """
        self.initial_pass()
        prev_cutset = sys.maxsize
        self.perform_pass()
        self.logger.debug("当前迭代过程: %d 割集: %d" % (1, self.cutset))
        iterations = 1
        while self.cutset != prev_cutset:
            prev_cutset = self.cutset
            self.perform_pass()
            self.logger.debug("当前迭代过程: %d 割集: %d" % (iterations + 1, self.cutset))
            iterations += 1

        self.logger.info("在%d次迭代中发现mincut: %d" % (iterations, self.cutset))

        return [c.n for c in self.blockA.cells], [c.n for c in self.blockB.cells]

c=FiducciaMattheyses()
z=c.find_mincut()
print(z)