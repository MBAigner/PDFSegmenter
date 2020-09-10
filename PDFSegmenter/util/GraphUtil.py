import networkx as nx
import numpy as np
from util import constants


def get_graph_bounding_box(graph):
    x_0 = nx.get_node_attributes(graph, "x_0")
    x_1 = nx.get_node_attributes(graph, "x_1")
    y_0 = nx.get_node_attributes(graph, "y_0")
    y_1 = nx.get_node_attributes(graph, "y_1")
    return (np.min(list(x_0.values())), np.max(list(x_1.values())),
            np.min(list(y_1.values())), np.max(list(y_0.values())))


def is_overlapping(bbox1, bbox2):
    overlap = (max(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),
               max(bbox1[2], bbox2[2]), min(bbox1[3], bbox2[3]))
    return overlap[0] < overlap[1] and overlap[2] < overlap[3]


def is_in_region(bbox1, bbox2, tol=5):
    return bbox1[0]+tol >= bbox2[0] and \
           bbox1[1]-tol <= bbox2[1] and \
           bbox1[2]+tol >= bbox2[2] and \
           bbox1[3]-tol <= bbox2[3]


def connected_component_subgraphs(G):
    """
    workaround for nx 2.4 or higher
    """
    for c in nx.connected_components(G):
        yield G.subgraph(c)


def get_unique_attr(graph_cluster, attr):
    return list(set(nx.get_node_attributes(graph_cluster, attr).values()))


def get_unique_rounded_attr(graph_cluster, attr):
    return list(set(map(lambda x: round(x),
                        nx.get_node_attributes(graph_cluster, attr).values())))


def get_unique_attr_from_filter(graph_cluster, attr, filter_attr, filter_value,
                                negate=False):
    if not negate:
        g = graph_cluster.subgraph([x for x, y in
                                    graph_cluster.nodes(data=True)
                                    if abs(y[filter_attr] - filter_value) < constants.BASELINE_THRESHOLD])
    else:
        g = graph_cluster.subgraph([x for x, y in
                                    graph_cluster.nodes(data=True)
                                    if abs(y[filter_attr] - filter_value) >= constants.BASELINE_THRESHOLD])
    return list(set(nx.get_node_attributes(g, attr).values()))
