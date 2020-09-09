
from PDFSegmenter.detection.BaseClassifier import BaseClassifier
from PDFSegmenter.util import constants


class LoopClassifier(BaseClassifier):

    def __init__(self, file):
        super().__init__(file)

    def classify_table_regions(self):
        return super().get_result(self.classify_table)

    # count rectangle-vertices
    def classify_table(self, graph_cluster, graph=None, bounding_box=None):
        return loop_score(graph_cluster) > constants.LOOP_TOLERANCE


def loop_score(graph_cluster):
    nodes = graph_cluster.nodes(data=True)
    rect_count = 0
    for node in nodes:
        if node[1]["is_loop"] > 0:
            rect_count += 1
    return rect_count / len(nodes)
