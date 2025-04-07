import matplotlib.pyplot as plt
import pandas as pd
import csv
import time
import networkx as nx
import sys
from collections import Counter
from mpl_toolkits.basemap import Basemap

from Algorithm.K_Shell import degree

sys.path.append('..')
import Algorithm.Basic_Topology
import Algorithm.Map

# startTime = time.time()

def ReadDataAndSave():
    data_path = 'E:/panjivaUSImport2019vessels.csv'
    # 原文件列名有点问题 不对应
    # df = pd.read_csv(data_path, usecols=['shpmtDestinationRegion', 'portOfUnladingRegion'])
    df = pd.read_csv(data_path, header=None)

    # 删除包含null值的行
    df.dropna(inplace=True)
    # item = df.memory_usage(deep=True)
    # print(item.sum() / (1024 ** 2))  # 查看内存占用
    # print(df.head())
    # print(df.dtypes)


    # Add edges
    G = nx.Graph()
    for index, row in df.iterrows():
        start, end = row[1], row[2]
        if G.has_edge(start, end):
            G[start][end]['weight'] += 1
        else:
            G.add_edge(start, end, weight=1)
    # print(G.nodes())
    #
    # 保存成边列表文件  这里没有保存权重
    nx.write_weighted_edgelist(G, "../Data/USExport2019/USImport2019.edgelist", comments='#', delimiter=':', encoding='utf-8')
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


# G_Export = nx.read_weighted_edgelist("../Data/USExport2019/USExport2019.edgelist", nodetype=str, delimiter=':')
# G_Import = nx.read_edgelist("graph.edgelist", nodetype=str, delimiter=':')



# G_2019 = nx.Graph()
# G_2019.add_nodes_from(G_Import.nodes())
# G_2019.add_edges_from(G_Import.edges())
# G_2019.add_nodes_from(G_Export.nodes())
# G_2019.add_edges_from(G_Export.edges())




# Algorithm.Basic_Topology.basic_topology_metrics(G_2019)
# Algorithm.Map.draw_world_ports_degree_heat_map(G_2019)
# communities = nx.community.louvain_communities(G_2019, seed=123)
# Algorithm.Map.draw_world_ports_communities_map(G_2019, communities)
# print(nx.community.modularity(G_2019, communities))


# 读取csv文件 并 保存成 edgelist 格式的图文件
# ReadDataAndSave()
# # G1 = Algorithm.Basic_Topology.zero_model(G)       # 生成一个零模型

# 加权网络的读取
G = nx.read_weighted_edgelist("graph_weighted.edgelist",nodetype=str, delimiter=':')
# G_null = nx.double_edge_swap(G.copy(), nswap=10000, max_tries=50000, seed=1)

#
#
# N = G_weighted.number_of_nodes()
# # 计算每个节点的强度
# port_strengths = {node: val for (node, val) in G_weighted.degree(weight='weight')}
#
# strengths = port_strengths.values()
#
# strengths_counts = Counter(strengths)
# print(strengths_counts)
#
# # sorted_strengths_counts = sorted(strengths_counts.items(), key=lambda item: item[0])
# # print(sorted_strengths_counts)
# # print(sum(strengths_counts.values()))
#
# # strengths_counts_frequency = {key : value / N for key,value in strengths_counts.items()}
# # print(strengths_counts_frequency)
# #
# # plt.scatter(list(strengths_counts_frequency.keys()), list(strengths_counts_frequency.values()), s=2, c='darkblue')
# # plt.xscale("log")
# # plt.yscale("log")
# # plt.xlabel("strength")
# # plt.ylabel("P(K=k)")
# # plt.show()
#
# BC = nx.betweenness_centrality(G_weighted)
# print(BC)
# BC_weighted = nx.betweenness_centrality(G_weighted, weight='weight')
# print(BC_weighted)
# # endTime = time.time()
# # print("usedTime:",endTime-startTime)

degree = dict(G.degree())
sorted_degree = dict(sorted(degree.items(), key=lambda item: item[1], reverse=True))
print(sorted_degree)

# #
# BC = nx.betweenness_centrality(G)
# sorted_BC = dict(sorted(BC.items(), key=lambda item: item[1], reverse=True))
# print(sorted_BC)



# CC = nx.closeness_centrality(G)
# sorted_CC = dict(sorted(CC.items(), key=lambda item: item[1], reverse=True))
# print(sorted_CC)
Algorithm.Map.draw_world_ports_degree_heat_map(G,degree)


# Latitude = {}
# Longitude = {}
#
# # 逐行读取txt文档 记录经纬度 有一些Ports有问题就不读取了
# with open('../Data/PortInfo.txt', 'r', encoding='utf-8') as file:
#     lines = file.readlines()
# for line in lines:
#     try:
#         # 去掉行尾的换行符号
#         line = line.strip()
#         # 切分
#         parts = line.split(":")
#
#         # 切分后第一段是港口 第二段是经纬度信息
#         Port = parts[0].strip()
#         coordinates = parts[1].strip()
#
#         # 因为有一些是泛指 没有经纬度坐标
#         if len(coordinates.split(",")) != 2:
#             raise ValueError("没有具体经纬度坐标")
#
#         latitude = coordinates.split(",")[0].strip()
#         longitude = coordinates.split(",")[1].strip()
#
#         Port = Port[2:]
#
#         sign = latitude[-1]  # 记录latitude最后一个字符是 N还是S
#
#         latitude = latitude[:-2]
#         longitude = longitude[:-2]
#
#         # 如果是 N 则为 ＋  是 S 则为 -
#         latitude = float(latitude) if sign == 'N' else -float(latitude)
#         longitude = float(longitude)
#
#         Latitude[Port] = latitude
#         Longitude[Port] = longitude
#         # print(f"Port: {Port}")
#         # print(f"Latitude: {latitude}")
#         # print(f"Longitude: {longitude}")
#     except ValueError as e:
#         pass  # 异常后什么都不执行
#
# world_map = Basemap()
# # 绘制地图边界，并设置背景颜色为灰色（海洋颜色）
# world_map.drawmapboundary(fill_color='#D0CFD4')
# world_map.fillcontinents(color='#EFEFEF', lake_color='#D0CFD4')
# world_map.drawcoastlines()
#
# # 在经纬度字典查找 G.nodes()
# Latitude_nodes = [Latitude.get(port, None) for port in g.nodes()]
# Longitude_nodes = [Longitude.get(port, None) for port in g.nodes()]
#
# x, y = world_map(Longitude_nodes, Latitude_nodes)
# scatter = world_map.scatter(x, y, marker='o', s=3, zorder=10, color='darkblue')
#
#
# plt.show()

# CC = nx.closeness_centrality(G)
# sorted_CC = dict(sorted(CC.items(), key=lambda item: item[1], reverse=True))
# print(sorted_CC)