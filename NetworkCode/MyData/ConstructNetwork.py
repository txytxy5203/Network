import pandas as pd
import networkx as nx
from mpl_toolkits.basemap import Basemap
import MyData.Main
import matplotlib.pyplot as plt

data_path = 'E:/panjivaUSImport.csv'

df = pd.read_csv(data_path, nrows=10000000, usecols=['shpmtDestinationRegion','portOfUnladingRegion','transportMethod'])
df.columns = ['portOfUnlading','portOfLading','vessel']
# 剔除重复数据
df_unique = df.drop_duplicates()


unique_vessels = df_unique['vessel'].unique().tolist()

G = nx.Graph()

# Add edges
for vessel in unique_vessels:
    test = df_unique[df_unique['vessel'] == vessel]

    previous_port = test['portOfUnlading'].iloc[-1]
    # 直接遍历 portOfUnlading 列 和 portOfLading列
    for port in test['portOfUnlading']:
        if previous_port == port:
            previous_port = port
            continue
        else:
            G.add_edge(previous_port,port)
            previous_port = port

    previous_port = test['portOfLading'].iloc[-1]
    for port in test['portOfLading']:
        if previous_port == port:
            previous_port = port
            continue
        else:
            G.add_edge(previous_port,port)
            previous_port = port


for index, row in df_unique.iterrows():
    start, end = row[1], row[0]
    if G.has_edge(start, end):
        continue
    else:
        G.add_edge(start, end)
G.remove_node('Columbia Metropolitan Airport., Columbia, South Carolina')
G.remove_node('Will Rogers World Airport, Oklahoma City, Oklahoma')
G.remove_node('Portland International Airport, Portland, Washington')
G.remove_node('Gateway Freight Services Inc., Los Angeles, California')

Communities = nx.community.louvain_communities(G, seed=123, resolution=1.1)

print(len(Communities))

Latitude = {}
Longitude = {}

# 逐行读取txt文档 记录经纬度 有一些点有问题就不读取了
with open('../Data/PortInfo.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
for line in lines:
    try:
        # 去掉行尾的换行符号
        line = line.strip()
        # 切分
        parts = line.split(":")

        # 切分后第一段是港口 第二段是经纬度信息
        Port = parts[0].strip()
        coordinates = parts[1].strip()

        # 因为有一些是泛指 没有经纬度坐标
        if len(coordinates.split(",")) != 2:
            raise ValueError("没有具体经纬度坐标")

        latitude = coordinates.split(",")[0].strip()
        longitude = coordinates.split(",")[1].strip()

        Port = Port[2:]

        sign = latitude[-1]     # 记录latitude最后一个字符是 N还是S

        latitude = latitude[:-2]
        longitude = longitude[:-2]

        # 如果是 N 则为 ＋  是 S 则为 -
        latitude = float(latitude) if sign == 'N' else -float(latitude)
        longitude = float(longitude)

        Latitude[Port] = latitude
        Longitude[Port] = longitude
        # print(f"Port: {Port}")
        # print(f"Latitude: {latitude}")
        # print(f"Longitude: {longitude}")
    except ValueError as e:
        pass    # 异常后什么都不执行



Port_Colors = {}    # 存放每个港口的颜色
Colors = ['red','blue' ,'green' , 'yellow', 'purple', 'orange', 'black', 'cyan']


for i,com in enumerate(Communities):
    for port in com:
        Port_Colors[port] = Colors[i]
# print("Port_Colors",Port_Colors)
# print(len(Port_Colors))


# 按照画图时港口的顺序 生成一个 Draw_Color list
Draw_Color = []
for port in G.nodes():
    Draw_Color.append(Port_Colors[port])

# print(G.nodes())
# print(G.number_of_nodes())
# 要画的节点的经纬度坐标

Latitude_nodes = [Latitude.get(port,None) for port in G.nodes()]
Longitude_nodes = [Longitude.get(port,None) for port in G.nodes()]


# print(Latitude_nodes)
# print(len(Latitude_nodes))
# print(Longitude_nodes)
# print(len(Longitude_nodes))



world_map = Basemap()
world_map.drawcoastlines()
# world_map.drawcounties(color='grey', linewidth=2)



x,y = world_map(Longitude_nodes,Latitude_nodes)
world_map.scatter(x, y, marker='o', color=Draw_Color, s=10, zorder=10)
plt.show()








N = G.number_of_nodes()
M = G.number_of_edges()
R = nx.degree_assortativity_coefficient(G)
C = nx.average_clustering(G)
# L = nx.average_shortest_path_length(G)
L = MyData.Main.average_shortest_path_length_largest_component(G)
print("N:",N)
print("M:",M)
print("<Knn>:",R)
print("<C>:",C)
print("<L>",L)
