import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import sys
sys.path.append('..')
import Algorithm.Basic_Topology

data_path = 'E:/GLSN/Source Data-Fig. 1d.csv'

df = pd.read_csv(data_path, header=None)

G = nx.Graph()
for index, row in df.iterrows():
    start, end = row[0], row[1]
    G.add_edge(start,end)
# 零模型
G1 = Algorithm.Basic_Topology.zero_model(G)

# 这两个度分布的画图函数 的 拟合部分都有问题   改！！！
# Algorithm.Basic_Topology.draw_degree_frequency_distribution(G)
# Algorithm.Basic_Topology.draw_degree_frequency_cumulative_distribution(G)
# Algorithm.Basic_Topology.draw_betweenness_centrality_cumulative_distribution(G,G1)
# Algorithm.Basic_Topology.draw_closeness_centrality_cumulative_distribution(G,G1)
# Algorithm.Basic_Topology.draw_degree_frequency_distribution(G1)

# 一个由 set 组成的 list
Communities = nx.community.louvain_communities(G,seed=123)
# Q = nx.community.modularity(G, Communities)
# # for i in Communities:
# #     print(len(i),i)
# # print("Q:",Q)

# # 创建dict 存放每个节点的 Z值和B值 默认值为0
# inside_module_degree = dict.fromkeys(G.nodes(),0)
# outside_module_degree = dict.fromkeys(G.nodes(),0)
#
# # 遍历社团
# for com in Communities:
#     # 遍历节点
#     for node in com:
#         # 遍历节点的邻居
#         for neighbor in G.neighbors(node):
#             # 邻居在社团内就inside＋1   不在就outside＋1
#             if neighbor in com:
#                 inside_module_degree[node] += 1
#             else:
#                 outside_module_degree[node] += 1
#
# # 减去平均值 再除以标准差
# inside_module_degree_mean = np.mean(list(inside_module_degree.values()))
# inside_module_degree_std_dev = np.std(list(inside_module_degree.values()))
# Z = inside_module_degree.copy()
# Z = {key : (value- inside_module_degree_mean) / inside_module_degree_std_dev for key,value in Z.items()}
#
# outside_module_degree_mean = np.mean(list(outside_module_degree.values()))
# outside_module_degree_std_dev = np.std(list(outside_module_degree.values()))
# P = outside_module_degree.copy()
# P = {key : (value- outside_module_degree_mean) / outside_module_degree_std_dev for key,value in P.items()}
#
# P_values = list(P.values())
# P_values.sort(reverse=True)
# plt.scatter(range(len(P_values)), P_values, s=2, c='darkblue')
# plt.xticks([])  # 隐藏刻度线
# plt.ylabel("P")
# plt.show()


# Z_values = list(Z.values())
# Z_values.sort(reverse=True)
# plt.scatter(range(len(Z_values)), Z_values, s=2, c='darkblue')
# plt.xticks([])  # 隐藏刻度线
# plt.ylabel("Z")
# plt.show()

def draw_participation_coefficient(g,communities):
    '''
    画出 图的P值 图
    :param g: 要计算的图
    :param communities: 图的社团划分
    :return:
    '''
    # 给节点添加 社团ID属性
    com_ID = 0  # 社团ID
    for com in communities:
        for node in com:
            g.nodes[node]['comID'] = com_ID
        com_ID += 1

    # 存放每个节点的 P值
    P_dict = dict.fromkeys(g.nodes(), 0)
    for com in communities:
        for node in com:
            temp = [0] * 8
            for neighbor in g.neighbors(node):
                temp[g.nodes[neighbor]['comID']] += 1

            P = 1
            # 这里是P值的公式 其实就是 熵的概念
            for i in temp:
                P -= (i / g.degree[node]) ** 2
            P_dict[node] = P

    P_value = list(P_dict.values())
    P_value.sort(reverse=True)
    plt.scatter(range(len(P_value)), P_value, s=2, c='darkblue')
    plt.ylabel("P")
    plt.show()

