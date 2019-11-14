from Graph import *
from node import *
import argparse
import random
import numpy as np
import multiprocessing as mp
import sys
import time
from queue import Empty

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
        # print(len(graph.nodes[1].connects))
        graph.nodes[int(begin)].add_edge(graph.nodes[int(end)], float(value))
    return graph


def file_to_seeds(seed_name):
    readed_files = open(seed_name, mode='r', encoding='UTF-8')
    seeds = []
    while True:
        try:
            seed = int(readed_files.readline())
        except ValueError:
            break
        seeds.append(seed)
    return seeds


def IC_1(graph, seed):
    count_set = set()
    for i in seed:
        count_set.add(i)
    count = len(seed)
    while len(seed) != 0:
        next_seed = set()
        for i in seed:
            nexts = graph.nodes[i].connects
            for j in nexts:
                conn_node, possibility = j[0], j[1]
                temp = np.random.rand()
                if temp < possibility:
                    next_seed.add(conn_node.order)
                    count_set.add(conn_node.order)
        for i in seed:
            next_seed.discard(i)
        count += len(next_seed)
        seed = list(next_seed)
    return (count + len(count_set)) / 2


def IC_2(graph, seed):
    had_activity = set()
    while len(seed) != 0:
        next_seed = set()
        for i in seed:
            had_activity.add(i)
        for i in seed:
            for j in graph.nodes[i].connects:
                node, possibility = j[0].order, j[1]
                if np.random.rand() < possibility and node not in had_activity:
                    next_seed.add(node)
        seed = list(next_seed)
    for i in seed:
        had_activity.add(i)
    return len(had_activity)


def IC(graph, seed):
    count = len(seed)
    while len(seed) != 0:
        next_seed = []
        for i in seed:
            nexts = graph.nodes[i].connects
            for j in nexts:
                conn_node, possibility = j[0], j[1]
                temp = np.random.rand()
                if temp < possibility:
                    next_seed.append(conn_node.order)
        count += len(next_seed)
        seed = next_seed
    return count


def LT(graph, seed):
    had_activity = set()
    for i in seed:
        had_activity.add(i)
    np.random.seed(np.random.randint(0, 1145141919))
    value_array = np.random.random(len(graph.nodes))
    # print(value_array)
    for i in range(1, len(graph.nodes), 1):
        if value_array[i] == 0 and i not in had_activity:
            had_activity.add(i)
    addition = -1
    while addition != 0:
        length1 = len(had_activity)
        # print(len(had_activity), addition, time.time())
        thresh_array = np.zeros(len(graph.nodes))
        for i in had_activity:
            for j in graph.nodes[i].connects:
                thresh_array[j[0].order] += j[1]
        next_add = set()
        for i in had_activity:
            for j in graph.nodes[i].connects:
                if value_array[j[0].order] < thresh_array[j[0].order]:
                    next_add.add(j[0].order)
        for i in next_add:
            had_activity.add(i)
        addition = len(had_activity) - length1
    return len(had_activity)


def LT_1(graph, seed):
    had_activity = set()
    addition = set()
    for i in seed:
        had_activity.add(i)
        addition.add(i)
    np.random.seed(np.random.randint(0, 1919810))
    value_array = np.random.random(len(graph.nodes))
    for i in range(1, len(graph.nodes), 1):
        if value_array[i] == 0 and i not in had_activity:
            had_activity.add(i)
            addition.add(i)
    thresh_array = np.zeros(len(graph.nodes))
    while len(addition) != 0:
        for i in addition:
            for j in graph.nodes[i].connects:
                thresh_array[j[0].order] += j[1]
        next_add = set()
        for i in addition:
            for j in graph.nodes[i].connects:
                if value_array[j[0].order] < thresh_array[j[0].order]:
                    next_add.add(j[0].order)
        addition = set()
        for i in next_add:
            if i not in had_activity:
                addition.add(i)
            had_activity.add(i)
    return len(had_activity)


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
    parser.add_argument('-i', '--file_name', type=str, default=file_pair_2[0])
    parser.add_argument('-s', '--seed', type=str, default=file_pair_2[1])
    parser.add_argument('-m', '--model', type=str, default='LT')
    parser.add_argument('-t', '--time_limit', type=int, default=60)
    args = parser.parse_args()
    file_name = args.file_name
    seed = args.seed
    model = args.model
    time_limit = args.time_limit
    # print(np.random.randint(0, 10, 2) for i in range(16))
    # begin to write my code
    graph_1 = file_to_graph(file_name)
    seedset = file_to_seeds(seed)
    np.random.seed(114514)
    worker = []
    create_worker(worker_num, time_limit)
    assert_value = -1
    lt1 = lt = 0
    # print(LT(graph_1, seedset) - LT_1(graph_1, seedset))
    for i in range(work_times):
        if model == "IC":
            assert_value = 0
            # print(len(graph_1.nodes))
            worker[i % worker_num].inQ.put((graph_1, seedset, IC_2))
        else:
            assert_value = 1
            worker[i % worker_num].inQ.put((graph_1, seedset, LT_1))
    results = []
    # print(time.time(), "----------------------------")
    time.sleep(time_limit * 5 / 6)
    for i in range(0, worker_num, 1):
        worker[i].terminate()
    items = 0
    count_braek = 0
    for i in range(work_times):
        try:
            results.append(worker[i % worker_num].outQ.get(block=False))
            items += 1
        except Empty:
            count_braek += 1
            if count_braek > 7:
                break
    # print("-------------------------------")
    # print(time.time())
    count = 0
    for i in results:
        count += i
        # results.append(worker[i % worker_num].outQ.get())
    print(count / items)
    # print(items)
    # print(time.time() - times + 2)
    # assert abs(count / items - result_pair_2[assert_value]) / result_pair_2[assert_value] < 0.01, print(result_pair_2[assert_value])
    finish_worker()
    sys.stdout.flush()
    sys.exit(0)
