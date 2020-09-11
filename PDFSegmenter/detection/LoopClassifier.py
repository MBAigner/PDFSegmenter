
from PDFSegmenter.detection.BaseClassifier import BaseClassifier
from PDFSegmenter.util import constants


class LoopClassifier(BaseClassifier):

    def __init__(self, file, merge_boxes=False, regress_parameters=False,
                 use_font=True, use_width=True, use_rect=True, use_horizontal_overlap=False,
                 use_vertical_overlap=False,
                 page_ratio_x=2, page_ratio_y=2, x_eps=2, y_eps=2, font_eps_h=1, font_eps_v=1,
                 width_pct_eps=.4, width_page_eps=.5):
        super().__init__(file, merge_boxes=merge_boxes, regress_parameters=regress_parameters,
                         use_font=use_font, use_width=use_width, use_rect=use_rect, use_horizontal_overlap=use_horizontal_overlap,
                         use_vertical_overlap=use_vertical_overlap,
                         page_ratio_x=page_ratio_x, page_ratio_y=page_ratio_y, x_eps=x_eps, y_eps=y_eps,
                         font_eps_h=font_eps_h, font_eps_v=font_eps_v,
                         width_pct_eps=width_pct_eps, width_page_eps=width_page_eps)

    def classify_table_regions(self):
        """

        :return:
        """
        return super().get_result(self.classify_table)

    # count rectangle-vertices
    def classify_table(self, graph_cluster, graph=None, bounding_box=None):
        """

        :param graph_cluster:
        :param graph:
        :param bounding_box:
        :return:
        """
        return loop_score(graph_cluster) > constants.LOOP_TOLERANCE


def loop_score(graph_cluster):
    """

    :param graph_cluster:
    :return:
    """
    nodes = graph_cluster.nodes(data=True)
    rect_count = 0
    for node in nodes:
        if node[1]["is_loop"] > 0:
            rect_count += 1
    return rect_count / len(nodes)
