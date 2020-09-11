
import networkx as nx
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from util import GraphUtil, constants
import editdistance


class AgglomerativeGraphCluster(object):

    def __init__(self, graphs, name=None, meta=None):
        self.graphs = graphs
        self.name = name
        self.graph = None
        self.nodes = None
        self.meta = meta

    def assign_clusters(self):
        """

        :return:
        """
        graphs_labeled = []
        for graph in self.graphs:
            labels = self.create_clusters(graph)
            nx.set_node_attributes(graph, labels, 'cluster_label')
            graphs_labeled.append(graph)
        return graphs_labeled

    def create_clusters(self, graph):
        """

        :param graph:
        :return:
        """
        # use subgraph with edges weighted by Levenshtein distance
        G_lev = graph.edge_subgraph(
            [(e[0], e[1], e[2]) for e in graph.edges(keys=True, data=True)
             if e[2].startswith("v") or e[2] == "h" or e[2] == "l"])
        UG = G_lev.to_undirected()

        # extract subgraphs
        clustering_labels = dict()
        max_label = 1
        for i, SG in enumerate(GraphUtil.connected_component_subgraphs(UG)):
            self.graph = SG
            self.nodes = dict(self.graph.nodes(data=True))
            lengths = dict(
                nx.all_pairs_dijkstra_path_length(SG, weight=self.calculate_distance_weight)  # weight="lenghty")
            )
            num_nodes = len(SG)
            distances = np.empty((num_nodes, num_nodes))
            distances[:] = np.nan
            nodes_list = list(SG.nodes)
            max_length = 0
            for i in range(num_nodes):
                id1 = nodes_list[i]
                if id1 in lengths:
                    for j in range(num_nodes):
                        id2 = nodes_list[j]
                        if id2 in lengths[id1] and lengths[id1] != 0:
                            length = lengths[id1][id2]
                            distances[i, j] = length
                            if max_length < length:
                                max_length = length
            k_opt = 2
            score_opt = -1
            for k in range(2, min(num_nodes - 1, 15)):
                clustering = AgglomerativeClustering(n_clusters=k, linkage="average",
                                                     affinity="precomputed").fit(distances)
                if max(clustering.labels_) == 0 or max(clustering.labels_) > num_nodes:
                    continue
                score = silhouette_score(distances, labels=clustering.labels_, metric="precomputed")
                if np.isnan(score):
                    break
                if score > score_opt:
                    score_opt = score
                    k_opt = k
            if score_opt > 0:
                clustering = AgglomerativeClustering(n_clusters=k_opt, linkage="average",
                                                     affinity="precomputed").fit(distances)
                labels = list(clustering.labels_ + max_label)
                clustering_labels.update(dict(zip(list(SG.nodes()), labels)))
                max_label = max(labels) + 1
            else:
                labels = [max_label] * num_nodes
                clustering_labels.update(dict(zip(list(SG.nodes()), labels)))
                max_label = max_label + 1

        return clustering_labels

    def calculate_distance_weight(self, id_start, id_end, edge):
        """

        :param id_start:
        :param id_end:
        :param edge:
        :return:
        """
        node_start = self.nodes[id_start]
        node_end = self.nodes[id_end]
        scaling = 1
        key = list(edge.keys())[0]
        if key == "l":
            scaling = constants.DIAGONAL_SCALING
        elif key == "h":
            scaling = constants.HORIZONTAL_SCALING
        length = edge[next(iter(edge))]["length"] * scaling

        if constants.USE_LEV_DISTANCE:
            # old setting
            text1 = node_start["masked"]
            text2 = node_end["masked"]
            lev_dist = self.get_normalized_lev_dist(text1, text2)
            length = length * lev_dist

        elif constants.USE_GOWER_DISTANCE:
            lev_dist = 0
            token_dist = 0
            loop_dist = 0
            font_dist = 0
            normalization = 0
            if constants.USE_TOKENS and key.startswith("v"):
                n1 = node_start["n_tokens"]
                n2 = node_end["n_tokens"]
                if n1 > 0 or n2 > 0:
                    token_dist = (1 - min(n1, n2) / max(n1, n2)) * constants.TOKEN_WEIGHT
                else:
                    token_dist = constants.TOKEN_WEIGHT
                normalization = normalization + constants.TOKEN_WEIGHT
            if constants.USE_LOOPS and key.startswith("v"):
                if node_start["is_loop"] != node_end["is_loop"]:
                    loop_dist = constants.LOOP_WEIGHT
                normalization = normalization + constants.LOOP_WEIGHT
            if constants.USE_FONT_DIST and key.startswith("v"):
                font_dist = abs(node_start["font_size"]-node_end["font_size"]) * constants.FONT_WEIGHT / max(node_start["font_size"],node_end["font_size"])
                normalization = normalization + constants.FONT_WEIGHT
            if constants.USE_TEXT and key.startswith("v"):
                text1 = node_start["masked"]
                text2 = node_end["masked"]
                lev_dist = self.get_normalized_lev_dist(text1, text2) * constants.LEV_DIST_WEIGHT
                normalization = normalization + constants.LEV_DIST_WEIGHT
            if normalization > 0 and key.startswith("v"):
                length = length * (lev_dist + token_dist + loop_dist + font_dist) / normalization

        return length

    @staticmethod
    def get_normalized_lev_dist(text1, text2):
        """

        :param text1:
        :param text2:
        :return:
        """
        len_text1 = len(text1)
        len_text2 = len(text2)
        if len_text1 > 0 and len_text2 > 0:
            dist = editdistance.eval(text1, text2) * 2 / \
                   (min(len_text1, len_text2) + max(len_text1, len_text2))
        else:
            dist = 1
        return dist
