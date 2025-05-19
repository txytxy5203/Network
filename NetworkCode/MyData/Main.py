import csv
import time

import numpy as np
import pandas as pd
import powerlaw
import networkx as nx
import matplotlib.pyplot as plt
import sys
from collections import Counter
from mpl_toolkits.basemap import Basemap

sys.path.append('..')
import Algorithm.Basic_Topology
import Algorithm.Map
import Algorithm.ConstructNetwork



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
    nx.write_weighted_edgelist(G, "../Data/US2019/USImport2019.edgelist", comments='#', delimiter=':', encoding='utf-8')
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


# G = nx.read_weighted_edgelist("../Data/US2019/USImport2019.edgelist", nodetype=str, delimiter=':')
# Algorithm.Basic_Topology.basic_topology_metrics(G)

G = Algorithm.ConstructNetwork.network_USImport2019_Improve()
N = G.number_of_nodes()
Algorithm.Basic_Topology.draw_degree_frequency_distribution(G)







# 读取csv文件 并 保存成 edgelist 格式的图文件
# ReadDataAndSave()
# # G1 = Algorithm.Basic_Topology.zero_model(G)       # 生成一个零模型

# 加权网络的读取
# G = nx.read_weighted_edgelist("graph_weighted.edgelist",nodetype=str, delimiter=':')
# # G_null = nx.double_edge_swap(G.copy(), nswap=10000, max_tries=50000, seed=1)
# # community = nx.community.louvain_communities(G, seed=123)
# # Algorithm.Map.draw_world_ports_communities_map(G, community)
# # print(nx.community.modularity(G, community))
#
# # nx.write_edgelist(G, "gephi.edges", data=False, delimiter=';')
#
# # 绘制大圆航线
# # map.drawgreatcircle(lon1, lat1, lon2, lat2, linewidth=2, color='b')
#
#
# Latitude = {}
# Longitude = {}
#
# # 逐行读取txt文档 记录经纬度 有一些Ports有问题就不读取了
# with open('../Data/PortCoordinateInfo.txt', 'r', encoding='utf-8') as file:
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
# # Panama_port = []
# # 这里先暂时这样直接给出  后续还是要仔细地洗一边数据
#
#
# world_map = Basemap()
#
# # try:
# #     for node in G.nodes():
# #         for neighbor in G.neighbors(node):
# #             world_map.drawgreatcircle(Longitude[node], Latitude[node], Longitude[neighbor], Latitude[neighbor],
# #                               linewidth=0.5, color='blue')
# # except KeyError as k:
# #     pass
#
#
#
# for node in G.nodes():
#     for neighbor in G.neighbors(node):
#         # 确保节点和邻居的经纬度信息都存在
#         if node in Longitude and neighbor in Longitude and node in Latitude and neighbor in Latitude:
#             x1, y1 = world_map(Longitude[node], Latitude[node])
#             x2, y2 = world_map(Longitude[neighbor], Latitude[neighbor])
#             # world_map.drawgreatcircle(x1, y1, x2, y2, linewidth=0.5, color='blue')
#             world_map.plot([x1,x2],[y1,y2], linewidth=0.1, color='b')
#
#
#
# # 绘制地图边界，并设置背景颜色为灰色（海洋颜色）
# world_map.drawmapboundary(fill_color='#D0CFD4')
# world_map.fillcontinents(color='#EFEFEF', lake_color='#D0CFD4')
# world_map.drawcoastlines()
#
# # 画 Panama_port
# Latitude_nodes = [Latitude.get(port, None) for port in G.nodes()]
# Longitude_nodes = [Longitude.get(port, None) for port in G.nodes()]
# x, y = world_map(Longitude_nodes, Latitude_nodes)
# world_map.scatter(x, y, marker='o', s=5, zorder=10, color='darkblue')
#
#
# plt.show()
# plt.savefig("../Figure/Panama.svg", dpi=300, format='svg')
