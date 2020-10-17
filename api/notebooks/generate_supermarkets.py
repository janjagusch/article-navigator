# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.6.0
#   kernelspec:
#     display_name: easy-way-api
#     language: python
#     name: easy-way-api
# ---

import sys
sys.path.append("..")

import random
import functools
import pickle

import networkx as nx
from tqdm import tqdm
from nx_concorde import calc_distance_matrix, calc_path_matrix
from scipy.spatial.distance import minkowski

from api.supermarket import Supermarket

block_distance = functools.partial(minkowski, p=1)


def _generate_random_grid_graph(m=10, n=10, frac=0.7):
    '''
    Generates a random 2d grid graph of space (m, n) with a sample of frac nodes.
    '''
    graph = nx.grid_2d_graph(m, n)
    graph = graph.subgraph(random.sample(graph.nodes(), int(frac * m * n)))
    graph = graph.subgraph(max(nx.connected_components(graph), key=len))
    nx.set_node_attributes(graph, {key: key for key in graph.nodes().keys()}, "pos")
    pos_to_idx = lambda x, y: n * y + x
    graph = nx.relabel_nodes(graph, {key: pos_to_idx(*value["pos"]) for key, value in graph.nodes().items()})
    nx.set_node_attributes(graph, "aisle", "type")
    graph.nodes()[min(graph.nodes())]["type"] = "entrance"
    graph.nodes()[max(graph.nodes())]["type"] = "checkout"
    return graph


N_SUPERMARKETS = 20
DIM_RANGE = range(8, 20)

supermarkets = {idx: Supermarket.from_graph(idx, f"Supermarket {idx}", _generate_random_grid_graph(random.choice(DIM_RANGE), random.choice(DIM_RANGE)), heuristic=block_distance, nodes=None) for idx in tqdm(range(N_SUPERMARKETS))}

with open("../supermarkets.pkl", "wb") as fp:
    pickle.dump(supermarkets, fp)
