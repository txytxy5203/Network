import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import sys
import difflib
import csv
import re

sys.path.append('..')
import Algorithm.Basic_Topology
import Algorithm.Draw
import Algorithm.Read
import Algorithm.Map
from mpl_toolkits.basemap import Basemap


def Read_and_save_port_region():
    data_path = 'E:/panjivaUSImport.csv'

    df = pd.read_csv(data_path, usecols=['portOfUnladingRegion', 'portOfLading'])
    df.columns = ['portOfLading', 'portOfLadingRegion']
    # print(df.head())

    # 删除包含null值的行
    df.dropna(inplace=True)
    # 删除完全重复的行
    df = df.drop_duplicates()
    # 保存成csv文件
    df.to_csv('../Data/port_Region.csv', index=False, sep=';', encoding='utf-8')
def draw_world_region_map(g):
    world_map = Basemap()
    # 绘制地图边界，并设置背景颜色为灰色（海洋颜色）
    world_map.drawmapboundary(fill_color='#D0CFD4')
    world_map.fillcontinents(color='#EFEFEF', lake_color='#D0CFD4')
    world_map.drawcoastlines()

    for node in g.nodes():
        try:
            # if port_Region[node] == 'South America':
            for neighbor in g.neighbors(node):
                if node in Longitude and neighbor in Longitude and node in Latitude and neighbor in Latitude:
                    x1, y1 = world_map(Longitude[node], Latitude[node])
                    x2, y2 = world_map(Longitude[neighbor], Latitude[neighbor])
                    # world_map.drawgreatcircle(x1, y1, x2, y2, linewidth=0.5, color='blue')
                    world_map.plot([x1, x2], [y1, y2], linewidth=0.1, color='b')
        except KeyError as k:
            pass
    plt.show()

# # 读取port经纬度坐标
# Latitude = {}
# Longitude = {}
# # 逐行读取txt文档 记录经纬度 有一些Ports有问题就不读取了
# with open('../Data/Port/PortCoordinateInfo.txt', 'r', encoding='utf-8') as file:
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
#         print(Port)



# # 检查有没有相似的port
# for item in Latitude.keys():
#     matches = difflib.get_close_matches(item, Latitude.keys(), n=2, cutoff=0.1)
#     if matches:
#         matched_port = matches[0]
#         if item != matched_port:
#             print(f"{item}:{matched_port}")




# panjivaUSImport2019.csv




HSCode = Algorithm.Read.read_USImpHSCode_Origin()
Algorithm.Read.save_USImpHSCode(HSCode)
# print(len(HSCode))
#
# i = 0
# for key,value in HSCode.items():
#     i += 1
#     print(key +': ' + str(value))
#     if i > 100:
#         break

# data_path = 'D:/PortData/USImport2019.csv'
# DataFrame = pd.read_csv(data_path, header=None)
# DataFrame.columns = ['panjivaRecordId', 'billOfLadingNumber',  'arrivalDate', 'conCountry', 'shpCountry', 'portOfUnlading', 'portOfLading',
#                      'portOfLadingCountry', 'portOfLadingRegion', 'transportMethod', 'vessel', 'volumeTEU', 'weightKg',
#                      'valueOfGoodsUSD']
# # 剔除重复数据
# DataFrame = DataFrame.drop_duplicates()
#
#
# # 1 使用均值填充 TEU
# DataFrame.fillna({'volumeTEU': DataFrame['volumeTEU'].mean()}, inplace=True)
# # 2 删除 'portOfLadingCountry' 列为空的行
# DataFrame = DataFrame.dropna(subset=['portOfLadingCountry'])
# # 3 使用 'fillna()' 方法填充 'conCountry' 列的空值
# DataFrame.fillna({'conCountry': 'United States'}, inplace=True)

# # 检查 volumeTEU、weightKg、valueOfGoodsUSD 字段中的空值数量
# null_counts = DataFrame[['volumeTEU', 'conCountry', 'portOfLadingCountry']].isnull().sum()
# # 打印每个字段的空值数量
# print(null_counts / len(DataFrame))

# # panjivaUSExport.csv
# data_path = 'E:/panjivaUSExport2019vessels.csv'
# DataFrame = pd.read_csv(data_path, header=None)
# DataFrame.columns = ['shpmtDate', 'portOfUnlading', 'portOfLading', 'vessel']

# port name 映射
# Port_Name = Algorithm.Read.read_port_name_info()
# print(Port_Name)

# # 检查有没有相似的port
# for item in Port_Name.keys():
#     matches = difflib.get_close_matches(item, Port_Name.keys(), n=2, cutoff=0.6)
#     if matches:
#         for matched_port in matches:
#             if item != matched_port:
#                 print(f"{item}:{matched_port}")


#
# # 打开一个新的文本文件，准备写入
# with open('temp.txt', 'w', encoding='utf-8') as file:
#     # 遍历集合中的每个元素
#     for port in error_port:
#         # 将每个元素写入文件，每个元素后跟一个换行符
#         file.write(port + '\n')


# Error_Port = set()
# Port_Name = Algorithm.Read.read_port_name_info()
# Remove_Port = Algorithm.Read.read_remove_port_info()
#
# timer = 0
# G = nx.Graph()
# for index, row in DataFrame.iterrows():
#     timer += 1
#     if timer / len(DataFrame) > 0.1:
#         print('当前进度：{:.2%}'.format(index / len(DataFrame)))
#         timer = 0
#
#
#     # 赋值给 portOfUnlading 和 portOfLading
#     portOfUnlading = row['portOfUnlading']
#     portOfLading = row['portOfLading']
#
#     # 检查是否在排除名单里
#     if portOfUnlading in Remove_Port or portOfLading in Remove_Port:
#         continue
#
#     # 查看是否在 Port_Name 中
#     if portOfUnlading in Port_Name.keys():
#         portOfUnlading = Port_Name[portOfUnlading]
#     else:
#         Error_Port.add(portOfUnlading)
#
#     if portOfLading in Port_Name.keys():
#         portOfLading = Port_Name[portOfLading]
#     else:
#         Error_Port.add(portOfLading)
#
#     # 创建一个字典来存储边的属性
#     edge_attrs = {
#         'volumeTEU': row['volumeTEU']
#     }
#     # 给 edge 和 node 添加属性
#     G.add_edge(portOfLading, portOfUnlading, **edge_attrs)
#     G.nodes[portOfLading]['Country'] = row['shpCountry']
#     G.nodes[portOfUnlading]['Country'] = row['conCountry']
#
# # 打印节点属性
# for node, attrs in G.nodes(data=True):
#     print(f"Node: {node}, Attributes: {attrs}")
# print(Error_Port)
# print(len(Error_Port))
#
# Algorithm.Basic_Topology.basic_topology_metrics(G)


# Error_Port和Port_Name 相似度匹配
# for item in Error_Port:
#     # 有一些港口不是 str 类型  需要转换
#     item = str(item)
#
#     matches = difflib.get_close_matches(item, Port_Name.keys(), n=2, cutoff=0.6)
#     if matches:
#         for matched_port in matches:
#             if item != matched_port:
#                 print(f"{item}:{matched_port}")



# # 打开一个新的文本文件，准备写入
# with open('Error_Port.txt', 'a', encoding='utf-8') as file:
#     # 遍历集合中的每个元素
#     for port in Error_Port:
#         # 将每个元素写入文件，每个元素后跟一个换行符
#         file.write(str(port) + '\n')

# # 检查 volumeTEU、weightKg、valueOfGoodsUSD 字段中的空值数量
# null_counts = DataFrame[['volumeTEU', 'weightKg', 'valueOfGoodsUSD']].isnull().sum()
# # 打印每个字段的空值数量
# print(null_counts / len(DataFrame))