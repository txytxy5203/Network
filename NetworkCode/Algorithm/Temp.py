import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np


# 定义数据
data = {
    'portOfUnlading': ['New York', 'Los Angeles', 'London', 'Tokyo', 'Hong Kong'],
    'portOfLading': ['Shanghai', 'Dubai', 'Rotterdam', 'Singapore', 'Buenos Aires'],
    'conCountry': ['USA', 'UAE', 'Netherlands', 'Japan', 'Argentina'],
    'shpCountry': ['China', 'India', 'UK', 'South Korea', 'Brazil'],
    'volumeTEU': [np.random.randint(100, 500) for _ in range(5)]  # 随机生成100到500之间的整数
}

# 创建DataFrame
df = pd.DataFrame(data)
# 显示DataFrame
print(df)

G = nx.DiGraph()
for index, row in df.iterrows():
    # 赋值给 portOfUnlading 和 portOfLading
    portOfUnlading = row['portOfUnlading']
    portOfLading = row['portOfLading']

    # 创建一个字典来存储边的属性
    edge_attrs = {
        'volumeTEU': row['volumeTEU']
    }
    G.add_edge(portOfLading, portOfUnlading, **edge_attrs)
    G.nodes[portOfLading]['Country'] = row['shpCountry']
    G.nodes[portOfUnlading]['Country'] = row['conCountry']
# 打印节点属性
for node, attrs in G.nodes(data=True):
    print(f"Node: {node}, Attributes: {attrs}")
# 检查图中的边和边的属性
for u, v, attrs in G.edges(data=True):
    print(f"Edge between {u} and {v} has attributes: {attrs}")