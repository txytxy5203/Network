from fontTools.misc.bezierTools import epsilon
from matplotlib.colors import LogNorm
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import networkx as nx
import  matplotlib.cm as cm




def draw_world_ports_communities_map(g, communities):
    '''

    :param g: 传入一个图
    :param communities: 图的社团检测结果
    :return:
    '''
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

            sign = latitude[-1]  # 记录latitude最后一个字符是 N还是S

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
            pass  # 异常后什么都不执行

    Port_Colors = {}  # 存放每个港口的颜色
    Colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'black']
    # Colors = ['white', 'white','white', 'white','white', 'red','white']

    for i, com in enumerate(communities):
        for port in com:
            # 这里加一行判断 因为原始数据中有 1386个港口 但是处理后只有 1210个港口有经纬度坐标可以使用
            # if port in Latitude.keys():
            Port_Colors[port] = Colors[i]

    # 按照画图时港口的顺序 生成一个 Draw_Color list
    Draw_Color = []
    for port in g.nodes():
        Draw_Color.append(Port_Colors[port])

    world_map = Basemap()
    # 绘制地图边界，并设置背景颜色为灰色（海洋颜色）
    world_map.drawmapboundary(fill_color='#D0CFD4')
    world_map.fillcontinents(color='#EFEFEF', lake_color='#D0CFD4')
    world_map.drawcoastlines()

    # 在经纬度字典查找 G.nodes()
    Latitude_nodes = [Latitude.get(port, None) for port in g.nodes()]
    Longitude_nodes = [Longitude.get(port, None) for port in g.nodes()]

    x, y = world_map(Longitude_nodes, Latitude_nodes)
    world_map.scatter(x, y, marker='o', color=Draw_Color, s=10, zorder=10)
    plt.show()
def draw_world_ports_degree_heat_map(g, centrality):
    '''
    画中心性指标热力图  使用该函数时 可能需要调整base_size的大小
    :param g: 传入一个图
    :param centrality: 节点中心性指标dict  例如： 度中心性，BC，CC等； key为港口名称，value为中心性指标的值
    :return:
    '''
    # 对数归一化 可能会有 0  所以用一个非常小的正数代替
    centrality = {key:value if value != 0 else epsilon for key,value in centrality.items()}

    # 对数归一化
    norm = LogNorm(vmin=min(centrality.values()), vmax=max(centrality.values()))


    # 创建颜色映射  已弃用
    # cmap = plt.colormaps['viridis']
    # norm = plt.Normalize(min(degree_dict.values()), max(degree_dict.values()))  # 归一化度值
    # node_colors = [cmap(norm(degree)) for degree in degree_dict.values()]

    # 节点大小映射
    base_size = 0.1
    node_sizes = [base_size * degree for degree in centrality.values()]

    Latitude = {}
    Longitude = {}

    # 逐行读取txt文档 记录经纬度 有一些Ports有问题就不读取了
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

            sign = latitude[-1]  # 记录latitude最后一个字符是 N还是S

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
            pass  # 异常后什么都不执行

    world_map = Basemap()
    # 绘制地图边界，并设置背景颜色为灰色（海洋颜色）
    world_map.drawmapboundary(fill_color='#D0CFD4')
    world_map.fillcontinents(color='#EFEFEF', lake_color='#D0CFD4')
    world_map.drawcoastlines()

    # 在经纬度字典查找 G.nodes()
    Latitude_nodes = [Latitude.get(port, None) for port in g.nodes()]
    Longitude_nodes = [Longitude.get(port, None) for port in g.nodes()]

    x, y = world_map(Longitude_nodes, Latitude_nodes)
    scatter = world_map.scatter(x, y, marker='o', s=node_sizes, zorder=10, cmap='Reds',
                                c=[norm(degree) for degree in centrality.values()])

    print([norm(degree) for degree in centrality.values()])

    # 添加颜色条   shrink是为了缩小颜色条保持与世界地图一致
    colorbar = plt.colorbar(scatter, orientation='vertical', pad=0.05, shrink=0.7)
    colorbar.set_label('Node Degree (log-scaled)')
    plt.show()
