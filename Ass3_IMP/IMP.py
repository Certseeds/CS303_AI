from Ass3_IMP.Graph import *
from Ass3_IMP.node import *
from Ass3_IMP.ISE import *
from queue import PriorityQueue as PQ
import argparse
import random
import numpy as np
import multiprocessing as mp
import sys
import time

file_pair_1 = ("network.txt", "seeds5.txt")
file_pair_2 = ("NetHEPT.txt", "seeds50.txt")
result_pair_1 = (30.47, 37.02)
result_pair_2 = (1127.44, 1456.98)
worker_num = 8
work_times = 1024
sys.setrecursionlimit(1000000)


def file_to_graph(file_name):
    readed_file = open(file_name, mode='r', encoding='UTF-8')
    node_number, edge_number = readed_file.readline().split(" ")
    node_number, edge_number = int(node_number), int(edge_number)
    graph = Graph(node_number, edge_number)
    for i in range(1, node_number + 1, 1):
        graph.nodes[i] = node(i)
    for i in range(0, edge_number, 1):
        begin, end, value = readed_file.readline().split(" ")
        graph.nodes[int(begin)].add_edge(graph.nodes[int(end)], float(value))
    return graph


class Worker(mp.Process):
    def __init__(self, inQ, outQ, random_seed, length):
        super(Worker, self).__init__(target=self.start)
        self.inQ = inQ
        self.outQ = outQ
        self.set_up_time = time.time()
        self.length = length
        np.random.seed(random_seed)  # 如果子进程的任务是有随机性的，一定要给每个子进程不同的随机数种子，否则就在重复相同的结果了

    def run(self):
        while True:
            task = self.inQ.get()  # 取出任务， 如果队列为空， 这一步会阻塞直到队列有元素
            graph, seed, func = task  # 解析任务
            result = func(graph, seed)  # 执行任务
            self.outQ.put(result)  # 返回结果


def create_worker(num, length):
    '''
    创建子进程备用
    :param num: 多线程数量
    '''
    for i in range(num):
        worker.append(Worker(mp.Queue(), mp.Queue(), np.random.randint(0, 10 ** 9), length))
        worker[i].start()


def finish_worker():
    '''
    关闭所有子线程
    '''
    for w in worker:
        w.terminate()


if __name__ == '__main__':
    times = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--file_name', type=str, default=file_pair_1[0])
    parser.add_argument('-k', '--seed_size', type=int, default=5)
    parser.add_argument('-m', '--model', type=str, default='IC')
    parser.add_argument('-t', '--time_limit', type=int, default=60)
    args = parser.parse_args()
    file_name = args.file_name
    seed_size = args.seed_size
    model = args.model
    time_limit = args.time_limit
    # print(np.random.randint(0, 10, 2) for i in range(16))
    # begin to write my code
    graph_1 = file_to_graph(file_name)
    np.random.seed(np.random.randint(0, 1145141919))
    worker = []
    seedset = set()
    list = PQ()
    before_seeds_count = 0
    for i in graph_1.nodes:
        if i is None:
            continue
        seedset.add(i.order)
        after_seeds_count = ISE_function(graph_1, seedset, model)
        seedset.remove(i.order)
        diff = after_seeds_count - before_seeds_count
        list.put((-1 * diff, i.order))
    print(sorted(list.queue))
    seedset.add(list.get()[1])
    #print(seedset)
    for i in range(1, seed_size, 1):
        new_list = PQ()
        count = len(seedset)
        before_seeds_count = ISE_function(graph_1, seedset, model)
        for j in range(0, list.qsize() - 1, 1):
            node1 = list.get()
            node2 = list.get()
            if node1[1] in seedset:
                continue
            seedset.add(node1[1])
            after_seeds_count = ISE_function(graph_1, seedset, model)
            seedset.remove(node1[1])
            diff = after_seeds_count - before_seeds_count
            if diff >= -1 * node2[0]:
                seedset.add(node1[1])
                list.put(node2)
                #print("before")
                new_list.put((-1 * diff, node1[1]))
                # print("after")
                break
            new_list.put((-1 * diff, node1[1]))
            list.put(node2)
        if len(seedset) == count:
            seedset.add(new_list.get()[1])
        while new_list.qsize() != 0:
            list.put(new_list.get())
        print(sorted(list.queue))
        #print(seedset)
    # print(ISE_function(graph_1, seedset, "IC"))
    # print(seedset)
    for i in seedset:
        print(i)
    sys.exit(0)
