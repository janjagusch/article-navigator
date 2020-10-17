def get_boundary_nodes(graph, m, n):
    boundary_nodes = []
    for node_label in list(graph):
        if node_label[0] == 0 or node_label[1] == n - 1 or node_label[0] == m - 1 or node_label[1] == 0:
            boundary_nodes.append(node_label)

    return boundary_nodes