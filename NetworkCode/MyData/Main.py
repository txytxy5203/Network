import pandas as pd
import csv
import time
import networkx as nx
import sys
sys.path.append('..')
import Algorithm.Basic_Topology

# startTime = time.time()

def ReadDataAndSave():
    data_path = 'E:/panjivaUSImport2019.csv'
    # 原文件列名有点问题 不对应
    # df = pd.read_csv(data_path, usecols=['shpmtDestinationRegion', 'portOfUnladingRegion'])
    df = pd.read_csv(data_path, header=None)

    # item = df.memory_usage(deep=True)
    # print(item.sum() / (1024 ** 2))  # 查看内存占用
    # print(df.head())
    # print(df.dtypes)


    # Add edges
    G = nx.Graph()
    for index, row in df.iterrows():
        start, end = row[1], row[0]
        if G.has_edge(start, end):
            G[start][end]['weight'] += 1
        else:
            G.add_edge(start, end, weight=1)
    # print(G.nodes())
    #
    # 保存成边列表文件  这里没有保存权重
    nx.write_edgelist(G, "graph.edgelist", data=False,delimiter=':')
def average_shortest_path_length_largest_component(g):
    '''

    :param g: 传入图
    :return:  最大连通分量的平均最短路径
    '''
    largest_component = max(nx.connected_components(g), key=len)  # 提取最大连通分量
    largest_subgraph = g.subgraph(largest_component)
    return nx.average_shortest_path_length(largest_subgraph)
def output_nodes():
    '''
    输出 一个csv文件  包含所有节点的名称
    :return:
    '''
    # 输出文件路径
    output_file = "nodes.csv"

    # 打开文件并写入数据
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # 每隔十个元素写入一行
        for i in range(0, len(list(G.nodes())), 10):
            writer.writerow(list(G.nodes())[i:i + 10])

    print(f"数据已成功写入 {output_file}")

# 读取csv文件 并 保存成 edgelist 格式的图文件
# ReadDataAndSave()

# G = nx.read_edgelist("graph.edgelist",nodetype=str, delimiter=':')
# G1 = Algorithm.Basic_Topology.zero_model(G)       # 生成一个零模型


# N = G.number_of_nodes()
# M = G.number_of_edges()
# R = nx.degree_assortativity_coefficient(G)
# C = nx.average_clustering(G)
# # L = nx.average_shortest_path_length(G)
# L = average_shortest_path_length_largest_component(G)  # 最大连通分支的平均最短路径
# print("N:",N)
# print("M:",M)
# print("<Knn>:",R)
# print("<C>:",C)
# print("<L>",L)







# endTime = time.time()
# print("usedTime:",endTime-startTime)