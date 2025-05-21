import pandas as pd
import networkx as nx
import difflib
import sys
import matplotlib.pyplot as plt
sys.path.append('..')
import Algorithm.Basic_Topology
import Algorithm.Draw
import Algorithm.Read
import Algorithm.Map
from mpl_toolkits.basemap import Basemap



def network_USImport2019_Improve():
    '''

    :return: 返回USImport2019 改进网络
    '''
    data_path = 'E:/panjivaUSImport2019vessels.csv'

    df = pd.read_csv(data_path, header=None)
    df.columns = ['arrivalDate', 'portOfUnlading', 'portOfLading', 'vessel']
    # # 剔除重复数据
    df = df.drop_duplicates()

    unique_vessels = df['vessel'].unique().tolist()

    g = nx.Graph()

    # Add edges
    for vessel in unique_vessels:
        test = df[df['vessel'] == vessel]

        previous_port = test['portOfUnlading'].iloc[-1]
        # 直接遍历 portOfUnlading 列 和 portOfLading列
        for port in test['portOfUnlading']:
            if previous_port == port:
                previous_port = port
                continue
            else:
                g.add_edge(previous_port, port)
                previous_port = port

        previous_port = test['portOfLading'].iloc[-1]
        for port in test['portOfLading']:
            if previous_port == port:
                previous_port = port
                continue
            else:
                g.add_edge(previous_port, port)
                previous_port = port

    for index, row in df.iterrows():
        start, end = row['portOfLading'], row['portOfUnlading']
        if g.has_edge(start, end):
            continue
        else:
            g.add_edge(start, end)

    return g
def Save_Network_USImport2019():
    '''
    保存USImport2019
    :return:
    '''
    data_path = 'D:/PortData/USImport2019.csv'
    HSCode = Algorithm.Read.read_USImpHSCode()
    DataFrame = pd.read_csv(data_path, header=None)
    DataFrame.columns = ['panjivaRecordId', 'billOfLadingNumber',  'arrivalDate', 'conCountry', 'shpCountry', 'portOfUnlading', 'portOfLading',
                         'portOfLadingCountry', 'portOfLadingRegion', 'transportMethod', 'vessel', 'volumeTEU', 'weightKg',
                         'valueOfGoodsUSD']
    # 剔除重复数据
    DataFrame = DataFrame.drop_duplicates()


    # 1 使用均值填充 TEU
    DataFrame.fillna({'volumeTEU': DataFrame['volumeTEU'].mean()}, inplace=True)
    # 2 删除 'portOfLadingCountry' 列为空的行
    DataFrame = DataFrame.dropna(subset=['portOfLadingCountry'])
    # 3 使用 'fillna()' 方法填充 'conCountry' 列的空值
    DataFrame.fillna({'conCountry': 'United States'}, inplace=True)

    # 将 'panjivaRecordId' 列转换为字符串类型
    DataFrame['panjivaRecordId'] = DataFrame['panjivaRecordId'].astype(str)

    print("DataFrame加载完毕")


    # port name 映射
    Port_Name = Algorithm.Read.read_port_name_info()
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


    Error_Port = set()
    Port_Name = Algorithm.Read.read_port_name_info()
    Remove_Port = Algorithm.Read.read_remove_port_info()

    timer = 0
    i = 0
    j = 0
    G = nx.DiGraph()
    for index, row in DataFrame.iterrows():
        timer += 1
        if timer / len(DataFrame) > 0.1:
            print(type(row['panjivaRecordId']))
            print('构建网络当前进度：{:.2%}'.format(index / len(DataFrame)))
            timer = 0


        # 赋值给 portOfUnlading 和 portOfLading
        portOfUnlading = row['portOfUnlading']
        portOfLading = row['portOfLading']

        # 检查是否在排除名单里
        if portOfUnlading in Remove_Port or portOfLading in Remove_Port:
            continue

        # 查看是否在 Port_Name 中
        if portOfUnlading in Port_Name.keys():
            portOfUnlading = Port_Name[portOfUnlading]
        else:
            Error_Port.add(portOfUnlading)
        if portOfLading in Port_Name.keys():
            portOfLading = Port_Name[portOfLading]
        else:
            Error_Port.add(portOfLading)

        # 注意这里的字符串是 str 类型
        if row['panjivaRecordId'] not in HSCode.keys():
            i = i + 1
            continue
        if HSCode[row['panjivaRecordId']] is None:
            j = j + 1
            continue

        # 创建一个字典来存储边的属性
        edge_attrs = {
            'volumeTEU': row['volumeTEU'],
            'HSCode': HSCode[row['panjivaRecordId']]
        }
        # 给 edge 和 node 添加属性
        G.add_edge(portOfLading, portOfUnlading, **edge_attrs)
        G.nodes[portOfLading]['Country'] = row['shpCountry']
        G.nodes[portOfUnlading]['Country'] = row['conCountry']

    # 打印节点属性
    for node, attrs in G.nodes(data=True):
        print(f"Node: {node}, Attributes: {attrs}")
    print(Error_Port)
    print(len(Error_Port))
    print(i)
    print(j)


    # 使用 GraphML 保存图
    nx.write_graphml(G, '../Data/US2019/USImport2019.graphml')
def Save_Network_USExport2019():
    '''
    保存USExport2019
    :return:
    '''
    data_path = 'D:/PortData/USExport2019.csv'
    HSCode = Algorithm.Read.read_USExpHSCode()
    DataFrame = pd.read_csv(data_path, header=None)
    DataFrame.columns = ['panjivaRecordId', 'billOfLadingNumber', 'shpmtDate', 'shpCountry', 'shpmtDestination',
                         'portOfUnlading', 'portOfLading', 'portOfLadingCountry', 'portOfUnladingCountry', 'vessel', 'volumeTEU',
                         'weightKg', 'valueOfGoodsUSD']
    # 剔除重复数据
    DataFrame = DataFrame.drop_duplicates()

    # 1 使用均值填充 TEU
    DataFrame.fillna({'volumeTEU': DataFrame['volumeTEU'].mean()}, inplace=True)
    # 2 删除 'portOfUnladingCountry' 列为空的行
    DataFrame = DataFrame.dropna(subset=['portOfUnladingCountry'])
    # 3 使用 'fillna()' 方法填充 'portOfLadingCountry' 列的空值
    DataFrame.fillna({'portOfLadingCountry': 'United States'}, inplace=True)

    # 将 'panjivaRecordId' 列转换为字符串类型
    DataFrame['panjivaRecordId'] = DataFrame['panjivaRecordId'].astype(str)

    print("DataFrame加载完毕")

    # # 检查 volumeTEU、weightKg、valueOfGoodsUSD 字段中的空值数量
    # null_counts = DataFrame[['shpCountry', 'shpmtDestination','volumeTEU', 'shpCountry', 'portOfLadingCountry',
    #                          'portOfUnladingCountry','weightKg', 'valueOfGoodsUSD']].isnull().sum()
    # # 打印每个字段的空值数量
    # print(null_counts / len(DataFrame))

    # port name 映射
    Port_Name = Algorithm.Read.read_port_name_info()
    # # print(Port_Name)
    #
    # # # 检查有没有相似的port
    # # for item in Port_Name.keys():
    # #     matches = difflib.get_close_matches(item, Port_Name.keys(), n=2, cutoff=0.6)
    # #     if matches:
    # #         for matched_port in matches:
    # #             if item != matched_port:
    # #                 print(f"{item}:{matched_port}")
    #
    # #
    # # # 打开一个新的文本文件，准备写入
    # # with open('temp.txt', 'w', encoding='utf-8') as file:
    # #     # 遍历集合中的每个元素
    # #     for port in error_port:
    # #         # 将每个元素写入文件，每个元素后跟一个换行符
    # #         file.write(port + '\n')

    Error_Port = set()
    Port_Name = Algorithm.Read.read_port_name_info()
    Remove_Port = Algorithm.Read.read_remove_port_info()

    timer = 0
    i = 0
    j = 0
    G = nx.DiGraph()
    for index, row in DataFrame.iterrows():
        timer += 1
        if timer / len(DataFrame) > 0.1:
            print(type(row['panjivaRecordId']))
            print('构建网络当前进度：{:.2%}'.format(index / len(DataFrame)))
            timer = 0

        # 赋值给 portOfUnlading 和 portOfLading
        portOfUnlading = row['portOfUnlading']
        portOfLading = row['portOfLading']

        # 检查是否在排除名单里
        if portOfUnlading in Remove_Port or portOfLading in Remove_Port:
            continue

        # 查看是否在 Port_Name 中
        if portOfUnlading in Port_Name.keys():
            portOfUnlading = Port_Name[portOfUnlading]
        else:
            Error_Port.add(portOfUnlading)
        if portOfLading in Port_Name.keys():
            portOfLading = Port_Name[portOfLading]
        else:
            Error_Port.add(portOfLading)

        # 注意这里的字符串是 str 类型
        if row['panjivaRecordId'] not in HSCode.keys():
            i = i + 1
            continue
        if HSCode[row['panjivaRecordId']] is None:
            j = j + 1
            continue

        # 创建一个字典来存储边的属性
        edge_attrs = {
            'volumeTEU': row['volumeTEU'],
            'HSCode': HSCode[row['panjivaRecordId']]
        }
        # 给 edge 和 node 添加属性
        G.add_edge(portOfLading, portOfUnlading, **edge_attrs)
        G.nodes[portOfLading]['Country'] = row['portOfLadingCountry']
        G.nodes[portOfUnlading]['Country'] = row['portOfUnladingCountry']

    # 打印节点属性
    for node, attrs in G.nodes(data=True):
        print(f"Node: {node}, Attributes: {attrs}")
    print(Error_Port)
    print(len(Error_Port))
    print(i)
    print(j)


    # 使用 GraphML 保存图
    nx.write_graphml(G, '../Data/US2019/USExport2019.graphml')

def Save_Network_BRImport2019():
    '''
    保存USBOImport2019
    :return:
    '''
    data_path = 'D:/PortData/BRImport2019.csv'

    DataFrame = pd.read_csv(data_path, header=None)
    # DataFrame的列名是一定不能乱的
    DataFrame.columns = ['panjivaRecordId', 'shpmtDate', 'conCountry', 'shpCountry', 'shpmtOrigin','shpmtOriginCountry','shpmtDestination',
                         'shpmtDestinationCountry','portOfOriginCountry','portOfUnlading','portOfUnladingCountry','portOfLading', 'vesselName',
                          'hSCode','volumeTEU', 'grossWeightKg', 'valueOfGoodsUSD']
    # 剔除重复数据
    DataFrame = DataFrame.drop_duplicates()


    # # 1 使用均值填充 TEU
    # DataFrame.fillna({'volumeTEU': DataFrame['volumeTEU'].mean()}, inplace=True)
    # # 2 删除 'portOfUnladingCountry' 列为空的行
    # DataFrame = DataFrame.dropna(subset=['portOfUnladingCountry'])
    # # 3 使用 'fillna()' 方法填充 'portOfLadingCountry' 列的空值
    # DataFrame.fillna({'portOfLadingCountry': 'United States'}, inplace=True)
    #
    # # 将 'panjivaRecordId' 列转换为字符串类型
    # DataFrame['panjivaRecordId'] = DataFrame['panjivaRecordId'].astype(str)
    #
    # print("DataFrame加载完毕")

    # # 检查 volumeTEU、weightKg、valueOfGoodsUSD 字段中的空值数量
    # null_counts = DataFrame[['shpCountry', 'shpmtDestination','volumeTEU', 'shpCountry', 'portOfLadingCountry',
    #                          'portOfUnladingCountry','weightKg', 'valueOfGoodsUSD']].isnull().sum()
    # # 打印每个字段的空值数量
    # print(null_counts / len(DataFrame))

    # port name 映射
    Port_Name = Algorithm.Read.read_port_name_info()

    # 将 需要的列转换为字符串类型
    DataFrame['portOfUnlading'] = DataFrame['portOfUnlading'].astype(str)
    DataFrame['portOfLading'] = DataFrame['portOfLading'].astype(str)
    DataFrame['panjivaRecordId'] = DataFrame['panjivaRecordId'].astype(str)


    #
    # #
    # # # 打开一个新的文本文件，准备写入
    # # with open('temp.txt', 'w', encoding='utf-8') as file:
    # #     # 遍历集合中的每个元素
    # #     for port in error_port:
    # #         # 将每个元素写入文件，每个元素后跟一个换行符
    # #         file.write(port + '\n')

    Error_Port = set()
    Port_Name = Algorithm.Read.read_port_name_info()
    Remove_Port = Algorithm.Read.read_remove_port_info()

    timer = 0
    i = 0
    j = 0
    G = nx.DiGraph()
    for index, row in DataFrame.iterrows():
        timer += 1
        if timer / len(DataFrame) > 0.1:
            print(type(row['panjivaRecordId']))
            print('构建网络当前进度：{:.2%}'.format(index / len(DataFrame)))
            timer = 0

        # 赋值给 portOfUnlading 和 portOfLading
        portOfUnlading = row['portOfUnlading']
        portOfLading = row['portOfLading']

        # 检查是否在排除名单里
        if portOfUnlading in Remove_Port or portOfLading in Remove_Port:
            continue

        # 查看是否在 Port_Name 中
        if portOfUnlading in Port_Name.keys():
            portOfUnlading = Port_Name[portOfUnlading]
        else:
            Error_Port.add(portOfUnlading)
        if portOfLading in Port_Name.keys():
            portOfLading = Port_Name[portOfLading]
        else:
            Error_Port.add(portOfLading)
    #
    #     # 注意这里的字符串是 str 类型
    #     if row['panjivaRecordId'] not in HSCode.keys():
    #         i = i + 1
    #         continue
    #     if HSCode[row['panjivaRecordId']] is None:
    #         j = j + 1
    #         continue
    #
    #     # 创建一个字典来存储边的属性
    #     edge_attrs = {
    #         'volumeTEU': row['volumeTEU'],
    #         'HSCode': HSCode[row['panjivaRecordId']]
    #     }
    #     # 给 edge 和 node 添加属性
    #     G.add_edge(portOfLading, portOfUnlading, **edge_attrs)
    #     G.nodes[portOfLading]['Country'] = row['portOfLadingCountry']
    #     G.nodes[portOfUnlading]['Country'] = row['portOfUnladingCountry']
    #
    # # 打印节点属性
    # for node, attrs in G.nodes(data=True):
    #     print(f"Node: {node}, Attributes: {attrs}")
    # print(Error_Port)
    # 在原地将集合中的每个元素转换为字符串
    # Error_Port.update(str(item) for item in Error_Port)
    print(len(Error_Port))

    # 检查有没有相似的port
    for item in Error_Port:
        matches = difflib.get_close_matches(item, Port_Name.keys(), n=2, cutoff=0.6)
        if matches:
            for matched_port in matches:
                # 直接一步到位
                pass
                # print(f"{item};{Port_Name[matched_port]}")

        else:
            print(item)

    # print(i)
    # print(j)

    # # 使用 GraphML 保存图
    # nx.write_graphml(G, '../Data/US2019/USExport2019.graphml')