import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import sys
sys.path.append('../Algorithm')
import re
import json
import powerlaw
from ConstructNetwork import *





# 假设有一个MultiDiGraph对象G
G_multi = nx.MultiDiGraph()
G_multi.add_edge(1, 2)  # 添加多条边
G_multi.add_edge(1, 2)
G_multi.add_edge(2, 1)  # 反向边
G_multi.add_edge(1, 3)  # 反向边

print(list(range(1,4)))

# # 转换为无向图（忽略多重边和方向）
# G_1 = nx.Graph(G_multi)  # 或使用G_multi.to_undirected(as_view=False)
# G_2 = nx.Graph()
# G_2.add_edge(1, 2)
# G_2.add_edge(1, 3)
#
# g = nx.Graph()
# g.add_edge(0, 1)
# # g.add_edge(0, 2)
# g.add_edge(1, 2)
# g.add_edge(3, 2)
# # g.add_edge(1, 3)
# # g.add_edge(0, 3)

# G_combined = nx.compose(G_1, G_2)
# G_combined = nx.compose(G_combined, G_3)
# # 使用 GraphML 保存图
# # nx.write_graphml(G_combined, '../Data/FinalGraph/test.graphml')
#
# # # 验证结果
# print(G_combined.edges())

