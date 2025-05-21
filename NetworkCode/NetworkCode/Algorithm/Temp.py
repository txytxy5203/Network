import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np
import Algorithm.Basic_Topology


G_DiGraph = nx.read_graphml('../Data/US2019/USExport2019.graphml')
G_Graph = G_DiGraph.to_undirected()
Algorithm.Basic_Topology.basic_topology_metrics(G_Graph)

