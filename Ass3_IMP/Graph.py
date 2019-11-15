from Ass3_IMP.node import *


class Graph:
    node_number = 0
    edge_number = 0

    def __init__(self, node_number, edge_number):
        self.node_number = node_number
        self.edge_number = edge_number
        self.nodes = [None] * (self.node_number+1)
