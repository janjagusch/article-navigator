from nx_concorde import calc_distance_matrix, calc_path_matrix, calc_tour
import random

def _graph_to_sections(graph):
    return {
        key: {
            "id": key,
            "type": data["type"],
            "location": {"x": data["pos"][0], "y": data["pos"][1]},
        }
        for key, data in graph.nodes().items()
    }

def _graph_to_articles(graph):
    return {
        node_id: {
            "id": node_info['article']['id'], ## NEEDS FIX?
            "name": node_info['article']['name']
        }
    for node_id, node_info in graph.nodes().items() if node_info['type'] == 'aisle'
    }

class Supermarket:
    def __init__(
        self, supermarket_id, name, sections, articles, graph, path_matrix, distance_matrix
    ):
        self._supermarket_id = supermarket_id
        self._name = name
        self._sections = sections
        self._articles = articles
        self._graph = graph
        self._path_matrix = path_matrix
        self._distance_matrix = distance_matrix
        self._entrance = [
            key for key, value in sections.items() if value["type"] == "entrance"
        ][0]
        self._checkout = [
            key for key, value in sections.items() if value["type"] == "checkout"
        ][0]

    @classmethod
    def from_graph(cls, supermarket_id, name, graph, **kwargs):
        sections = _graph_to_sections(graph)
        articles = _graph_to_articles(graph)
        path_matrix = calc_path_matrix(graph, **kwargs)
        distance_matrix = calc_distance_matrix(graph, path_matrix)
        return cls(
            supermarket_id=supermarket_id,
            name=name,
            graph=graph,
            sections=sections,
            articles=articles,
            path_matrix=path_matrix,
            distance_matrix=distance_matrix,
        )

    def to_dict(self):
        return {
            "id": self._supermarket_id,
            "name": self._name,
            "sections": list(self._sections.values()),
        }

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(id={self._supermarket_id}, name={self._name})"
        )

    def calc_tour(self, visit_nodes):
        return calc_tour(
            self._graph,
            self._entrance,
            self._checkout,
            visit_nodes,
            self._path_matrix,
            self._distance_matrix,
        )
