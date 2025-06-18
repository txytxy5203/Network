import csv
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from Algorithm.ConstructNetwork import ConstructNetwork
from Algorithm.Basic_Topology import *
from Algorithm.Map import *

def generate_graph():
    # # # 读取 GraphML 文件
    BR_Im = nx.read_graphml('../Data/BR2019/BRImport2019.graphml')
    BR_Ex = nx.read_graphml('../Data/BR2019/BRExport2019.graphml')
    # BR_Im_Graph = nx.Graph(BR_Im)
    # BR_Ex_Graph = nx.Graph(BR_Ex)
    G_BR = nx.compose(BR_Im, BR_Ex)
    print("BR is ready")

    CL_Im = nx.read_graphml('../Data/CL2019/CLImport2019.graphml')
    # G_CL = nx.Graph(CL_Im)
    print("CL is ready")


    CO_Ex = nx.read_graphml('../Data/CO2019/COExport2019.graphml')
    # G_CO = nx.Graph(CO_Ex)
    print("CO is ready")

    IN_Im = nx.read_graphml('../Data/IN2019/INImport2019.graphml')
    IN_Ex = nx.read_graphml('../Data/IN2019/INExport2019.graphml')
    # IN_Im_Graph = nx.Graph(IN_Im)
    # IN_Ex_Graph = nx.Graph(IN_Ex)
    G_IN = nx.compose(IN_Im, IN_Ex)
    print("IN is ready")

    US_Im = nx.read_graphml('../Data/US2019/USImport2019.graphml')
    US_Ex = nx.read_graphml('../Data/US2019/USExport2019.graphml')
    # US_Im_Graph = nx.Graph(US_Im)
    # US_Ex_Graph = nx.Graph(US_Ex)
    G_US = nx.compose(US_Im, US_Ex)
    print("US is ready")

    VE_Im = nx.read_graphml('../Data/VE2019/VEImport2019.graphml')
    # G_VE = nx.Graph(VE_Im)
    print("VE is ready")

    # 合并两个图
    G_combined = nx.compose(G_BR, CL_Im)
    G_combined = nx.compose(G_combined, CO_Ex)
    G_combined = nx.compose(G_combined, G_IN)
    G_combined = nx.compose(G_combined, G_US)
    G_combined = nx.compose(G_combined, VE_Im)

    print("N:",G_combined.number_of_nodes())
    print("M:",G_combined.number_of_edges())

    # 使用 GraphML 保存图
    nx.write_graphml(G_combined, '../Data/FinalGraph/MultiDiGraph2019.graphml')


# print(G_2019.number_of_edges())

# G_null = G_2019.copy()

# # 进行n_swaps次边交换
# nx.double_edge_swap(G_null, nswap=100000, max_tries=1000000)
# # 确保没有自环
# G_null.remove_edges_from(nx.selfloop_edges(G_null))
# print(G_null.number_of_edges())


# community = nx.community.louvain_communities(G_2019)
# for com in community:
#     print(len(com))

# Port_Data = ConstructNetwork.Read_Port_Data()
# # error = []
# #
# # for data in Port_Data.values():
# #     try:
# #         print(data["latitude"])
# #     except:
# #         error.append(data["english_name"])
# # print(error)
#
# world_map = Basemap()
# # 绘制地图边界，并设置背景颜色为灰色（海洋颜色）
# world_map.drawmapboundary(fill_color='#D0CFD4')
# world_map.fillcontinents(color='#EFEFEF', lake_color='#D0CFD4')
# world_map.drawcoastlines()
# # 读经纬度时一定记得转成 float
# coord_all_port = [(float(port["longitude"]),float(port["latitude"])) for port in Port_Data.values() if "latitude" in port and "longitude" in port]
# x, y = world_map([data[0] for data in coord_all_port], [data[1] for data in coord_all_port])
# world_map.scatter(x, y, marker='o', color='g', s=10, zorder=10)
#
#
# coord = [(float(Port_Data[node]["longitude"]),float(Port_Data[node]["latitude"]))
#          for node in G_2019.nodes() if "latitude" in Port_Data[node].keys() and "longitude" in Port_Data[node].keys()]
# print(coord)
# print(len(coord))
#
#
# a, b = world_map([data[0] for data in coord], [data[1] for data in coord])
# world_map.scatter(a, b, marker='o', color='b', s=10, zorder=10)
# plt.show()
# MultiDiG_2019 = nx.read_graphml('../Data/FinalGraph/MultiDiGraph2019.graphml')
def draw_world_ports_communities_map():
    Colors = ['#670096', '#d78306', '#f205c1', '#3ba91e', '#0068d7', '#e64a03', '#020202', '#CCCCCC']
    Port_Data = ConstructNetwork.Read_Port_Data()
    G_2019 = nx.read_graphml('../Data/FinalGraph/Graph2019.graphml')

    communities = nx.community.louvain_communities(G_2019)
    Port_Colors = {}

    for i, com in enumerate(communities):
        print(len(com))
        for port in com:
            Port_Colors[port] = Colors[i]

    coord = [(float(Port_Data[node]["longitude"]), float(Port_Data[node]["latitude"]), Port_Colors[node])
             for node in G_2019.nodes() if "latitude" in Port_Data[node].keys() and "longitude" in Port_Data[node].keys()]

    world_map = Basemap()
    # 绘制地图边界，并设置背景颜色为灰色（海洋颜色）
    world_map.drawmapboundary(fill_color='#D0CFD4')
    world_map.fillcontinents(color='#EFEFEF', lake_color='#D0CFD4')
    world_map.drawcoastlines()

    x, y = world_map([data[0] for data in coord], [data[1] for data in coord])
    world_map.scatter(x, y, marker='o', color=[data[2] for data in coord], s=10, zorder=10)
    plt.show()
def draw_world_ports_degree_heat_map(g, centrality):

    Port_Data = ConstructNetwork.Read_Port_Data()


    coord = [(float(Port_Data[node]["longitude"]), float(Port_Data[node]["latitude"]), centrality[node])
             for node in g.nodes() if "latitude" in Port_Data[node].keys() and "longitude" in Port_Data[node].keys()]
    value = [data[2] for data in coord]

    # 计算散点大小 - 使用度值的线性映射，并添加最小尺寸
    min_size = 10
    max_size = 100
    min_value = min(value)
    max_value = max(value)

    # 线性映射函数：将度值映射到散点大小
    sizes = [min_size + (d - min_value) * (max_size - min_size) / (max_value - min_value) for d in value]
    # 计算与度值相关的透明度（0.3-1.0）
    alphas = [0.1 + (d - min_value) * (1.0 - 0.3) / (max_value - min_value) for d in value]

    world_map = Basemap()
    # 绘制地图边界，并设置背景颜色为灰色（海洋颜色）
    world_map.drawmapboundary(fill_color='#D0CFD4')
    world_map.fillcontinents(color='#EFEFEF', lake_color='#D0CFD4')
    world_map.drawcoastlines()

    x, y = world_map([data[0] for data in coord], [data[1] for data in coord])
    world_map.scatter(x, y, marker='o', color='b', s=sizes, zorder=10, alpha=alphas)
    plt.show()

G_2019 = nx.read_graphml('../Data/FinalGraph/Graph2019.graphml')
bc = nx.betweenness_centrality(G_2019)
degree = nx.degree_centrality(G_2019)
cc = nx.closeness_centrality(G_2019)


sorted_degree = sorted(degree.items(), key=lambda item : item[1], reverse=True)
print(sorted_degree)
bc_degree = [(degree[node], bc[node], cc[node] , node) for node in G_2019.nodes()]

plt.scatter([data[0] for data in bc_degree], [data[1] for data in bc_degree], marker='s', c='red')
plt.xlabel("degree")
plt.ylabel("BC")
plt.title("degree--BC")
plt.show()

plt.scatter([data[0] for data in bc_degree], [data[2] for data in bc_degree], marker='s', c='red')
plt.xlabel("degree")
plt.ylabel("CC")
plt.title("degree--CC")
plt.show()