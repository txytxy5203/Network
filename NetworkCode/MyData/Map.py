from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import networkx as nx


G = nx.read_edgelist("graph.edgelist",nodetype=str, delimiter=':')
# Communities = nx.community.louvain_communities(G,seed=123)






# Communities = nx.community.greedy_modularity_communities(G)
# print(Communities)
# print(len(Communities))
#
# Latitude = {}
# Longitude = {}
#
# # 逐行读取txt文档 记录经纬度 有一些点有问题就不读取了
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
#         sign = latitude[-1]     # 记录latitude最后一个字符是 N还是S
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
#         pass    # 异常后什么都不执行
#
#
# # print(Longitude)
# # print("Latitude",Latitude)
# # print(len(Latitude))
# # print(len(Longitude))
# # print(len(Latitude))
# #
# Port_Colors = {}    # 存放每个港口的颜色
# # Colors = ['red','blue' ,'green' , 'yellow', 'purple', 'orange', 'black']
# Colors = ['white', 'white','white', 'white','white', 'red','white']
#
# for i,com in enumerate(Communities):
#     for port in com:
#         # 这里加一行判断 因为原始数据中有 1386个港口 但是处理后只有 1210个港口有经纬度坐标可以使用
#         # if port in Latitude.keys():
#         Port_Colors[port] = Colors[i]
# print("Port_Colors",Port_Colors)
# print(len(Port_Colors))
#
# # 按照画图时港口的顺序 生成一个 Draw_Color list
# Draw_Color = []
# for port in Latitude.keys():
#     Draw_Color.append(Port_Colors[port])
#
#
# world_map = Basemap()
# world_map.drawcoastlines()
# world_map.drawcounties(color='grey', linewidth=2)
#
# # 经纬度坐标
# Longitude_list = list(Longitude.values())  # 经度列表
# Latitude_list = list(Latitude.values())  # 纬度列表
#
# x,y = world_map(Longitude_list,Latitude_list)
# world_map.scatter(x, y, marker='o', color=Draw_Color, s=10, zorder=10)
# plt.show()

