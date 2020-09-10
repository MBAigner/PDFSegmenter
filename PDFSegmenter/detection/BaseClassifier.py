import networkx as nx

from PDFSegmenter.clustering.Agglomerative_Clustering import AgglomerativeGraphCluster
from GraphConverter import GraphConverter
from PDFSegmenter.util import constants
from PDFSegmenter.util import StorageUtil
from PDFSegmenter.util import GraphUtil
import ast
import numpy as np


class BaseClassifier(object):

    def __init__(self, file, merge_boxes=False, regress_parameters=False,
                 use_font=True, use_width=True, use_rect=True, use_horizontal_overlap=False,
                 use_vertical_overlap=False,
                 page_ratio_x=2, page_ratio_y=2, x_eps=2, y_eps=2, font_eps_h=1, font_eps_v=1,
                 width_pct_eps=.4, width_page_eps=.5):
        if file is None:
            return
        self.file = file
        self.file_name = StorageUtil.get_file_name(self.file)
        self.graph_converter = GraphConverter(self.file, merge_boxes, regress_parameters,
                                              use_font, use_width, use_rect, use_horizontal_overlap,
                                              use_vertical_overlap,
                                              page_ratio_x, page_ratio_y, x_eps, y_eps, font_eps_h, font_eps_v,
                                              width_pct_eps, width_page_eps)
        self.graphs = self.graph_converter.convert()
        self.media_box = self.graph_converter.get_media_boxes()
        self.graphs = AgglomerativeGraphCluster(self.graphs, self.file).assign_clusters()
        self.meta = self.graph_converter.meta

    def get_result(self, classify_table):
        result = {}
        media_box = self.media_box
        for page, graph in enumerate(self.graphs):
            result[page + 1] = {}
            result[page + 1]["bounding_box"] = (media_box[page]["x0page"],
                                                media_box[page]["x1page"],
                                                media_box[page]["y0page"],
                                                media_box[page]["y1page"])
            for i, sg in enumerate(GraphUtil.connected_component_subgraphs(graph.to_undirected())):
                clusters = list(set(nx.get_node_attributes(sg, "cluster_label").values()))
                for cluster in clusters:
                    cid = str(i) + "_" + str(cluster)
                    graph_cluster = sg.subgraph([x for x, y in
                                                 sg.nodes(data=True)
                                                 if y['cluster_label'] == cluster])
                    result[page + 1][cid] = {}
                    result[page + 1][cid]["bounding_box"] = \
                        GraphUtil.get_graph_bounding_box(graph_cluster)
                    result[page + 1][cid]["element"] = self.classify_cluster_element(page, self.meta, graph_cluster,
                                                                                     graph,
                                                                                     result[page + 1][cid][
                                                                                         "bounding_box"],
                                                                                     classify_table)
                    result[page + 1][cid]["content"] = list(map(lambda x: x[1], graph_cluster.nodes(data=True)))
        return result

    @staticmethod
    def classify_cluster_element(page, meta, graph_cluster, graph, res_bounding, classify_table):
        if constants.CLASSIFY_LIST and BaseClassifier.classify_list(graph_cluster):
            return "list"
        elif constants.CLASSIFY_PLOT and BaseClassifier.classify_plot(graph_cluster):
            return "plot"
        elif constants.CLASSIFY_TEXT and BaseClassifier.classify_text(graph_cluster, meta, page):
            return "text"
        elif classify_table(graph_cluster=graph_cluster, bounding_box=res_bounding, graph=graph):
            return "table"
        else:
            return "none"

    @staticmethod
    def classify_list(graph_cluster):
        x0s = GraphUtil.get_unique_rounded_attr(graph_cluster, "x_0")
        x1s = GraphUtil.get_unique_rounded_attr(graph_cluster, "x_1")
        xcs = GraphUtil.get_unique_rounded_attr(graph_cluster, "pos_x")
        return (BaseClassifier.classify_list_on_x_set(graph_cluster, x0s, align="x_0") or
                BaseClassifier.classify_list_on_x_set(graph_cluster, x1s, align="x_1") or
                BaseClassifier.classify_list_on_x_set(graph_cluster, xcs, align="pos_x"))

    @staticmethod
    def classify_list_on_x_set(graph_cluster, xs, align):
        if len(xs) != 2:
            return False
        text_left = GraphUtil.get_unique_attr_from_filter(graph_cluster, "masked",
                                                          filter_attr=align,
                                                          filter_value=min(xs))
        return len(text_left) == 1

    @staticmethod
    def classify_text(graph_cluster, meta, page):
        x0s = list(map(lambda x: round(x),
                       list(nx.get_node_attributes(graph_cluster, "x_0").values())))
        x1s = list(map(lambda x: round(x),
                       list(nx.get_node_attributes(graph_cluster, "x_1").values())))
        widths = [i - j for i, j in zip(x1s, x0s)]
        avg_width = meta.avg_widths[page]
        if np.mean(widths) > avg_width:
            rgbs = list(nx.get_node_attributes(graph_cluster, "rgb").values())
            if len(rgbs) > 0 and type(rgbs[0]) is not tuple:
                rgbs = list(map(lambda x: ast.literal_eval(x), rgbs))
            avg_rgb = (np.mean(list(map(lambda x: x[0], rgbs))),
                       np.mean(list(map(lambda x: x[1], rgbs))),
                       np.mean(list(map(lambda x: x[2], rgbs))),
                       np.mean(list(map(lambda x: x[3], rgbs))))
            # test if RGB is primary textual
            return abs(max(avg_rgb) - avg_rgb[0]) < constants.FLOAT_EPS and avg_rgb[3] > 0
        return False

    @staticmethod
    def classify_plot(graph_cluster):
        # TODO
        return False

    def get_graphs(self):
        return self.graphs
