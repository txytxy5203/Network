import csv
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


from Algorithm.ConstructNetwork import ConstructNetwork
from Algorithm.Basic_Topology import *
from Algorithm.Map import *


# # # # 读取 GraphML 文件
# BR_Im = nx.read_graphml('../Data/BR2019/BRImport2019.graphml')
# BR_Ex = nx.read_graphml('../Data/BR2019/BRExport2019.graphml')
# BR_Im_Graph = nx.Graph(BR_Im)
# BR_Ex_Graph = nx.Graph(BR_Ex)
# G_BR = nx.compose(BR_Im_Graph, BR_Ex_Graph)
# print("BR is ready")
#
# CL_Im = nx.read_graphml('../Data/CL2019/CLImport2019.graphml')
# G_CL = nx.Graph(CL_Im)
# print("CL is ready")
#
#
# CO_Ex = nx.read_graphml('../Data/CO2019/COExport2019.graphml')
# G_CO = nx.Graph(CO_Ex)
# print("CO is ready")
#
# IN_Im = nx.read_graphml('../Data/IN2019/INImport2019.graphml')
# IN_Ex = nx.read_graphml('../Data/IN2019/INExport2019.graphml')
# IN_Im_Graph = nx.Graph(IN_Im)
# IN_Ex_Graph = nx.Graph(IN_Ex)
# G_IN = nx.compose(IN_Im_Graph, IN_Ex_Graph)
# print("IN is ready")
#
# US_Im = nx.read_graphml('../Data/US2019/USImport2019.graphml')
# US_Ex = nx.read_graphml('../Data/US2019/USExport2019.graphml')
# US_Im_Graph = nx.Graph(US_Im)
# US_Ex_Graph = nx.Graph(US_Ex)
# G_US = nx.compose(US_Im_Graph, US_Ex_Graph)
# print("US is ready")
#
# VE_Im = nx.read_graphml('../Data/VE2019/VEImport2019.graphml')
# G_VE = nx.Graph(VE_Im)
# print("VE is ready")
#
# # 合并两个图
# G_combined = nx.compose(G_BR, G_CL)
# G_combined = nx.compose(G_combined, G_CO)
# G_combined = nx.compose(G_combined, G_IN)
# G_combined = nx.compose(G_combined, G_US)
# G_combined = nx.compose(G_combined, G_VE)
#
# print("N:",G_combined.number_of_nodes())
# print("M:",G_combined.number_of_edges())
#
# # 使用 GraphML 保存图
# nx.write_graphml(G_combined, '../Data/FinalGraph/Graph2019.graphml')

# G_2019 = nx.read_graphml('../Data/FinalGraph/Graph2019.graphml')
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

Port_Data = ConstructNetwork.Read_Port_Data()
# error = []
#
# for data in Port_Data.values():
#     try:
#         print(data["latitude"])
#     except:
#         error.append(data["english_name"])
# print(error)
world_map = Basemap()
# 绘制地图边界，并设置背景颜色为灰色（海洋颜色）
world_map.drawmapboundary(fill_color='#D0CFD4')
world_map.fillcontinents(color='#EFEFEF', lake_color='#D0CFD4')
world_map.drawcoastlines()

# # 在经纬度字典查找 G.nodes()
# Latitude_nodes = [port["latitude"] for port in Port_Data.values() if "latitude" in port and "longitude" in port]
#
# Longitude_nodes = [port["longitude"] for port in Port_Data.values() if "longitude" in port and "latitude" in port]
# for i in range(len(Longitude_nodes)):
#     print(Longitude_nodes[i], Latitude_nodes[i])
#     if i > 10:
#         break

coord = [(float(port["longitude"]),float(port["latitude"])) for port in Port_Data.values() if "latitude" in port and "longitude" in port]
print(coord)
x, y = world_map([data[0] for data in coord], [data[1] for data in coord])
world_map.scatter(x, y, marker='o', color='b', s=10, zorder=10)
plt.show()