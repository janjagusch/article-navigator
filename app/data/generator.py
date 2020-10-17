import random
import pickle
import networkx as nx

def get_boundary_nodes(graph, m, n):
    '''
    Function that returns the boundary nodes of a given graph with dimensions mxn
    '''
    boundary_nodes = []
    for node_label in list(graph):
        if node_label[0] == 0 or node_label[1] == n - 1 or node_label[0] == m - 1 or node_label[1] == 0:
            boundary_nodes.append(node_label)

    return boundary_nodes

def generate_random_supermarket(identifier, location):
    '''
    Function that generates a random supermarket given an id and location.

    Returns a dictionary and the graph object
    '''
    # dimensions
    m, n = random.randint(5, 10), random.randint(5, 10)

    graph = nx.grid_2d_graph(m, n)
    graph = graph.subgraph(random.sample(graph.nodes(), int(0.8 * m * n)))
    graph = graph.subgraph(max(nx.connected_components(graph), key=len))

    boundary_nodes = get_boundary_nodes(graph, m, n)

    # randomly assign 2 boundary nodes as entry and exit
    entrance_node, exit_node = random.sample(boundary_nodes, 2)
    nx.set_node_attributes(graph, {entrance_node: {"type": 'entrance'}})
    nx.set_node_attributes(graph, {exit_node: {"type": 'exit'}})

    # randomly assign 10% of nodes as aisles, that are not the entrance and exit node
    aisle_nodes = random.sample([node for node in graph.nodes
                                 if node not in (entrance_node, exit_node)]
                                , int(0.1 * m * n))

    aisle_attrs = {node: {"type": 'aisle'} for node in aisle_nodes}
    nx.set_node_attributes(graph, aisle_attrs)

    sections = generate_sections(graph)

    return {
        "id": identifier,
        "name": f"{random.sample(('Lidl', 'Kaufland'), 1)[0]} {location}",
        "sections": sections
    }, graph

def generate_sections(graph):
    '''
    Function that returns the sections of a particular supermarket
    '''
    index = 0
    sections = {}
    for node in graph.nodes():
        node_attr = graph.nodes[node]
        if node_attr:
            section_dict = {
                "id": 0,
                "type": node_attr['type'],
                "location": {
                    "x": node[0],
                    "y": node[1]
                }
            }
            section_id = hash(pickle.dumps(section_dict))
            sections[section_id] = section_dict

    return sections