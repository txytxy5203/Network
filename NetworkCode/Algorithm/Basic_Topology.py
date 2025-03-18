from collections import Counter
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms.bipartite.centrality import betweenness_centrality, closeness_centrality

# 定义幂律函数
def power_law(x, a, b):
    return a * np.power(x, b)
def read_data():
    # Read the data
    path_to_data = 'C:/Users/Rong/Downloads/ca-GrQc/ca-GrQc.mtx'
    data = pd.read_csv(path_to_data, delim_whitespace=True, skiprows=2, header=None)
    data = data.astype(int)

    # Add edges
    g = nx.Graph()
    for index, row in data.iterrows():
        g.add_edge(row[0], row[1])
    return g
def draw_degree_frequency_distribution(g):
    '''
    画图后续还要修改 没有图例 美化一下
    :param g: 传入一个图graph
    :画出 度分布图
    '''

    degree_frequency_numbers = nx.degree_histogram(g)       # 度的频数
    # [0, 675, 789, 676, 428, 258, 205, 153, 140, 99, 92, 65, 45, 57, 38, 48, 25, 44, 20, 18, 28, 16, 12, ...]
    # print(len(nx.degree_histogram(G)))  # 82
    x_degree = list(range(len(degree_frequency_numbers)))  # 所有的度数 作为下面画图的x坐标

    # 删去 度为0的元素
    for i in sorted(x_degree, reverse=True):     # 注意这里要反向遍历 不然索引会出问题
        if degree_frequency_numbers[i] == 0:
            del degree_frequency_numbers[i]
            del x_degree[i]

    degree_frequency = [x / N for x in degree_frequency_numbers]  # 度的频率
    # print(degree_frequency)

    # 线性拟合
    coeffs = np.polyfit(np.log10(x_degree), np.log10(degree_frequency),1)
    b_fitted = coeffs[0]
    a_fitted = np.exp(coeffs[1])

    plt.scatter(x_degree, degree_frequency, c='darkblue', label='Nodes')
    plt.plot(x_degree, a_fitted * np.power(x_degree,b_fitted), c='red', linestyle='--',
             label='Fit' +' '+ fr'$k^{{{b_fitted:.3f}}}$')      # 注意这里的label的写法
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.show()
def draw_degree_frequency_cumulative_distribution(g):
    degree_frequency_numbers = nx.degree_histogram(g)  # 度的频数
    # [0, 675, 789, 676, 428, 258, 205, 153, 140, 99, 92, 65, 45, 57, 38, 48, 25, 44, 20, 18, 28, 16, 12, ...]
    # print(len(nx.degree_histogram(G)))  # 82
    x_degree = list(range(len(degree_frequency_numbers)))  # 所有的度数 作为下面画图的x坐标

    # 删去 度为0的元素
    for i in sorted(x_degree, reverse=True):  # 注意这里要反向遍历 不然索引会出问题
        if degree_frequency_numbers[i] == 0:
            del degree_frequency_numbers[i]
            del x_degree[i]

    degree_frequency = [x / N for x in degree_frequency_numbers]  # 度的频率

    # 累计度分布
    cumulative_degree_frequency = [1 - degree_frequency[0]]     # 累计度分布的第一个元素是1-degree_frequency[0]
    # 累计就这么算
    for i in degree_frequency[1:]:
        cumulative_degree_frequency.append(cumulative_degree_frequency[-1] - i)

    plt.scatter(x_degree, cumulative_degree_frequency, c='darkblue', label='Nodes')
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()
    plt.show()
def draw_length_frequency_distribution(g):
    '''
    :param g: 传入图 graph
    计算两点之间的距离所占比例 的分布图

    '''
    lengths_all_pairs = dict(nx.all_pairs_shortest_path_length(g))
    # 列子
    # {0: {0: 0, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 10: 1},
    #  1: {11: 1, 12: 1, 13: 1, 17: 1, 19: 1, 21: 1, 31: 1, 30: 2, 9: 2},
    #  2: {0: 1, 2: 1, 3: 1, 7: 1, 13: 1, 17: 1, 19: 1, 21: 1, 30: 1}}
    lengths_value = []
    # 遍历 lengths_all_pairs
    for i in lengths_all_pairs.values():
        for j in i.values():
            lengths_value.append(j)

    # 使用 Counter 统计每个值的出现次数
    lengths_value_counts = Counter(lengths_value)
    del lengths_value_counts[0]  # 删去距离为0的
    lengths_value_counts = {key: value / 2 for key, value in lengths_value_counts.items()}  # 这里要除以2 因为上面计算了两次
    lengths_value_counts_rate = {key: value / sum(lengths_value_counts.values()) for key, value in
                                 lengths_value_counts.items()}

    plt.scatter(lengths_value_counts.keys(), lengths_value_counts_rate.values(), c='red', marker='s')
    plt.yscale("log")
    plt.xlabel("Length")
    plt.ylabel("P(L)")
    plt.show()
def draw_degree_cluster(g):
    '''
    度 和 聚类系数 之间的关系图
    :param g: 传入 图
    '''
    # 存放 度 和 聚类系数 之间的关系
    degree_cluster = {}
    for node in g:
        if g.degree(node) in degree_cluster.keys():
            degree_cluster[g.degree(node)] += nx.clustering(g, node)
        else:
            degree_cluster[g.degree(node)] = nx.clustering(g, node)

    degree_frequency_numbers = nx.degree_histogram(g)  # 度的频数
    degree_cluster = {key: value / degree_frequency_numbers[key] for key, value in degree_cluster.items()}
    # print(degree_cluster)
    plt.scatter(degree_cluster.keys(), degree_cluster.values(), marker='^', c='blue')
    plt.xlabel("K")
    plt.ylabel("C(K)")
    plt.yscale("log")
    plt.show()
def draw_degree_knn(g):
    degree_knn = nx.average_degree_connectivity(g)
    plt.scatter(degree_knn.keys(), degree_knn.values(), marker='s', c='red')
    plt.xlabel("K")
    plt.ylabel(r"$K_{nn}(k)$")
    plt.yscale("log")
    plt.show()
def draw_degree_betweenness_centrality(g):
    '''
    度 和 中介中心性 之间的关系
    :param g:
    :return:
    '''
    degree_betweenness = nx.betweenness_centrality(g)
    # 存放 度 和 中介中心性 之间的关系
    degree_betweenness_centrality = {}
    for node in g:
        if g.degree(node) in degree_betweenness_centrality.keys():
            degree_betweenness_centrality[g.degree(node)] += degree_betweenness[node]
        else:
            degree_betweenness_centrality[g.degree(node)] = degree_betweenness[node]

    degree_frequency_numbers = nx.degree_histogram(g)  # 度的频数
    degree_betweenness_centrality = {key: value / degree_frequency_numbers[key] for key, value in
                                     degree_betweenness_centrality.items()}
    plt.scatter(degree_betweenness_centrality.keys(), degree_betweenness_centrality.values(), marker='^', c='blue')
    plt.xlabel("K")
    plt.ylabel("C(K)")
    # plt.xscale("log")
    plt.yscale("log")
    plt.show()
def draw_betweenness_centrality_cumulative_distribution(g1, g2):
    '''
    中介中心性 的 累计概率分布图
    :param g:
    '''
    def calculate_BC_values_cumulative_distribution(g):
        '''
        计算BC_value_not_repeat 和 BC_values_cumulative_distribution
        :param g:
        :return:
        '''
        BC = nx.betweenness_centrality(g)
        BC_values = list(BC.values())
        BC_values.sort()

        # 用 set 排除重复  extend：将list添加到末尾
        BC_values_not_repeat.extend(list(set(BC_values)))
        BC_values_not_repeat.sort()

        # 遍历set 统计BC_values 中 大于 某个BC值的比例
        # BC_values_cumulative_distribution = []
        for i in BC_values_not_repeat:
            BC_values_cumulative_distribution.append(len([x for x in BC_values if x > i]) / len(BC_values))

    BC_values_not_repeat = []
    BC_values_cumulative_distribution = []
    calculate_BC_values_cumulative_distribution(g1)
    plt.scatter(BC_values_not_repeat, BC_values_cumulative_distribution, c='darkblue', label='Nodes', s=5)

    BC_values_not_repeat = []
    BC_values_cumulative_distribution = []
    calculate_BC_values_cumulative_distribution(g2)
    plt.scatter(BC_values_not_repeat, BC_values_cumulative_distribution, c='gray', label='Random', s=5)

    plt.yscale("log")
    plt.xlabel("BC")
    plt.ylabel("P(BC>bc)")
    plt.legend()
    plt.show()
def zero_model(g):
    '''

    :param g: 传入一个图
    :return:  返回一个零模型随机图  近似拥有相同度分布 因为删去了 平行边 和 自环
    '''
    degree = list(dict(g.degree()).values())

    # 零模型
    g1 = nx.configuration_model(degree)  # 保持度分布不变 随机重连
    # 删除平行边 和 自环  会导致度分布有一些不同
    g1 = nx.Graph(g1)
    g1.remove_edges_from(nx.selfloop_edges(g1))
    return g1


G = read_data()
# G = nx.karate_club_graph()
N = G.number_of_nodes()
# density = nx.density(G)
# degree_nodes = dict(G.degree())
# R = nx.degree_assortativity_coefficient(G)


def draw_closeness_centrality_cumulative_distribution(g1,g2):
    def obtain_CC_values_not_repeat(cc_values):
        cc_values_not_repeat = list(set(cc_values))
        cc_values_not_repeat.sort()
        return cc_values_not_repeat
    def obtain_CC_values_cumulative_distribution(cc_values_not_repeat):
        bc_values_cumulative_distribution = []
        for i in cc_values_not_repeat:
            bc_values_cumulative_distribution.append(len([x for x in CC_values if x > i]) / len(CC_values))
        return bc_values_cumulative_distribution
    # 先算原本的图
    CC = nx.closeness_centrality(g1)
    CC_values = list(CC.values())
    CC_values.sort()

    CC_values_not_repeat = obtain_CC_values_not_repeat(CC_values)
    CC_values_cumulative_distribution = obtain_CC_values_cumulative_distribution(CC_values_not_repeat)
    # print(CC_values_not_repeat)
    # print(CC_values_cumulative_distribution)

    plt.scatter(CC_values_not_repeat, CC_values_cumulative_distribution, c='darkblue', label='Nodes', s=5)

    # 再算零模型的图
    CC_zero = nx.closeness_centrality(g2)
    CC_values_zero = list(CC_zero.values())
    CC_values_zero.sort()

    CC_values_not_repeat_zero = obtain_CC_values_not_repeat(CC_values_zero)
    CC_values_cumulative_distribution_zero = obtain_CC_values_cumulative_distribution(CC_values_not_repeat_zero)
    # print(CC_values_not_repeat_zero)
    # print(CC_values_cumulative_distribution_zero)

    plt.scatter(CC_values_not_repeat_zero, CC_values_cumulative_distribution_zero, c='gray', label='Random', s=5)
    plt.yscale("log")
    plt.xlabel("CC")
    plt.ylabel("P(CC>cc)")
    plt.legend()
    plt.show()



G1 = zero_model(G)

# draw_length_frequency_distribution(G)
# draw_closeness_centrality_cumulative_distribution(G,G1)
