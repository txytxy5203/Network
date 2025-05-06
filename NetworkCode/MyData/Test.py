import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import sys
import difflib
import csv

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

data_path = 'E:/panjivaUSImport2019.csv'
DataFrame = pd.read_csv(data_path, header=None)
DataFrame.columns = ['billOfLadingNumber',  'arrivalDate', 'conCountry', 'shpCountry', 'portOfUnlading', 'portOfLading',
                     'portOfLadingCountry', 'portOfLadingRegion', 'transportMethod', 'vessel', 'volumeTEU', 'weightKg',
                     'valueOfGoodsUSD']
# panjivaUSExport.csv
# data_path = 'E:/panjivaUSExport.csv'
# DataFrame = pd.read_csv(data_path, header=None)
# DataFrame.columns = ['arrivalDate', 'portOfUnlading', 'portOfLading', 'vessel']

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

# error_port = set()
# G = nx.Graph()
# for index, row in DataFrame.iterrows():
#     portOfUnlading = row['portOfUnlading']
#     portOfLading = row['portOfLading']
#
#     if portOfUnlading not in Port_Name.keys():
#         error_port.add(portOfUnlading)
#     if portOfLading not in Port_Name.keys():
#         error_port.add(portOfLading)
# print(error_port)
# print(len(error_port))
#
# # 打开一个新的文本文件，准备写入
# with open('temp.txt', 'w', encoding='utf-8') as file:
#     # 遍历集合中的每个元素
#     for port in error_port:
#         # 将每个元素写入文件，每个元素后跟一个换行符
#         file.write(port + '\n')


# for item in error_port:
#     # matches = difflib.get_close_matches(item, Latitude.keys(), n=1, cutoff=0.8)
#     # if matches:
#     #     matched_port = matches[0]
#     #     print(f"{item}:{matched_port}")
#     # else:
#     #     print(item)
#     print(item)


Error_Port = set()
Port_Name = Algorithm.Read.read_port_name_info()
G = nx.Graph()
for index, row in DataFrame.iterrows():
    portOfUnlading = row['portOfUnlading']
    portOfLading = row['portOfLading']

    if portOfUnlading in Port_Name.keys():
        portOfUnlading = Port_Name[portOfUnlading]
    else:
        Error_Port.add(portOfUnlading)

    if portOfLading in Port_Name.keys():
        portOfLading = Port_Name[portOfLading]
    else:
        Error_Port.add(portOfLading)
    G.add_edge(portOfLading,portOfUnlading)

print(Error_Port)
Algorithm.Map.draw_world_ports_map(G)