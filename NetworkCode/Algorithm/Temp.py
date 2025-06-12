import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import sys
sys.path.append('../Algorithm')
import re
import json
from ConstructNetwork import *




# # # 读取 GraphML 文件
# G_Imp = nx.read_graphml('../Data/US2019/USImport2019.graphml')
# G_Exp = nx.read_graphml('../Data/US2019/USExport2019.graphml')
# G = nx.read_graphml('../Data/BR2019/BRExport2019.graphml')

# # 合并两个图
# G_combined = nx.compose(G_Imp, G_Exp)

# print("N:",G.number_of_nodes())
# print("M:",G.number_of_edges())
ConstructNetwork.Save_Network_INImport2019()

# port_name = "new york,ny".lower()
# port_name = re.sub(r'[^a-zA-Z]', '', port_name)
# print(port_name)

# Port_Data = ConstructNetwork.Read_Port_Data()
# path = 'D:/PortData/CountryGeo.csv'
# # 提取所有country_english的值到列表中
# country_list = set(item["country_english"] for item in Port_Data.values())
# print(country_list)
# print(len(country_list))


# # nrows = 1000000
# DataFrame = pd.read_csv(path, header=None)
# DataFrame.columns = ['countryId', 'country', 'isoCountry2' , 'isoCountry3', 'regionId','region']
#
# error_port = []
# for index, row in DataFrame.iterrows():
#     match = False
#     for item in country_list:
#         if item == row['country']:
#             print(item + ":" + row['country'])
#             match = True
#     if not match:
#         error_port.append(row['country'])
# for port in error_port:
#     print(port)
# US_data_path = 'D:/PortData/USImport2019.csv'


# # # 过滤数据，只保留美国的港口
# # us_data = {
# #     port_code: info
# #     for port_code, info in port_data.items()
# #     if "United States of America" in info.get("country_english", "")
# # }
# # us_data_dict = {value["english_name"]: key for key, value in us_data.items()}

# # # nrows = 1000000
# port_data = ConstructNetwork.Read_Port_Data()
# data_path = 'D:/PortData/COExport2019.csv'
# DataFrame = pd.read_csv(data_path, header=None)
# DataFrame.columns = ['panjivaRecordId', 'shpmtDate', 'conCountry','shpCountry', 'shpmtOrigin',
# 		                     'shpmtDestination', 'shpmtDestinationCountry', 'portOfLading', 'portOfLadingCountry',
# 		                     'transportMethod', 'hsCode', 'volumeTEU', 'itemQuantity', 'itemUnit',
# 		                     'grossWeightKg', 'netWeightKg', 'valueOfGoodsFOBUSD', 'valueOfGoodsFOBCOP']
# # 剔除重复数据
# DataFrame = DataFrame.drop_duplicates()
# # 将 相关列转换为字符串类型
#
#
# DataFrame['portOfLadingCountry'] = DataFrame['portOfLadingCountry'].astype(str)
# DataFrame['shpmtDestinationCountry'] = DataFrame['shpmtDestinationCountry'].astype(str)
#
#
# # # 剔除重复数据
# # 删除 'panjivaRecordId' 列重复的行，只保留第一次出现的行
# DataFrame = DataFrame.drop_duplicates(subset=['panjivaRecordId'], keep='first')
# print(f"剔除重复数据后DataFrame大小:{len(DataFrame)}")
#
# # 检查 volumeTEU、weightKg、valueOfGoodsUSD 字段中的空值数量
# null_counts = DataFrame.isnull().sum()
# print("每个字段的null值情况：")
# print(null_counts / len(DataFrame))
#
# # 1 使用均值填充 TEU
# DataFrame.fillna({'volumeTEU': DataFrame['volumeTEU'].mean()}, inplace=True)
# # 2 删除 某某 列为空的行
# DataFrame = DataFrame.dropna(subset=['shpmtDestination', 'portOfLading'])
# print("DataFrame处理完毕")
#
#
# error_port = set()
# timer = 0
#
# for index, row in DataFrame.iterrows():
#     timer += 1
#     if timer / len(DataFrame) > 0.01:
#         print('构建网络当前进度：{:.2%}'.format(index / len(DataFrame)))
#         timer = 0
#
#     # 声明港口唯一代码
#     UnLading_Code = str()
#     Lading_Code = str()
#
#
#     # 声明一个 是否匹配 的bool值
#     match_Lading = False
#     match_UnLading = False
#
#     portOfLading_country = row['portOfLadingCountry'].lower()
#     portOfUnLading_country = row['shpmtDestinationCountry'].lower()
#
#     for port in port_data:
#         port_country = port_data[port]["country_english"].lower()
#         if port_country == portOfLading_country:
#             match_Lading = True
#         if port_country == portOfUnLading_country:
#             match_UnLading = True
#
#     if not match_Lading:
#         error_port.add(portOfLading_country)
#     if not match_UnLading:
#         error_port.add(portOfUnLading_country)
#
#
# for item in error_port:
#     print(item)