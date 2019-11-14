class node:
    def add_edge(self, node_2, value):
        self.connects.append((node_2, value))

    def __init__(self, order):
        self.state = False
        self.order = order
        self.connects = []
