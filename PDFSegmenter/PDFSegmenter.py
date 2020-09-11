from PDFSegmenter.structure_recognition.ResultParser import ResultParser
from util import constants
from PDFSegmenter.detection.LoopClassifier import LoopClassifier


class PDFSegmenter(object):

    def __init__(self, pdf, merge_boxes=False, regress_parameters=False,
                 use_font=True, use_width=True, use_rect=True, use_horizontal_overlap=False,
                 use_vertical_overlap=False,
                 page_ratio_x=2, page_ratio_y=2, x_eps=2, y_eps=2, font_eps_h=1, font_eps_v=1,
                 width_pct_eps=.4, width_page_eps=.5,
                 horizontal_merge_threshold=20, vertical_merge_threshold=20, weak_merge=True,
                 horizontal_weak_merge_threshold=20, vertical_weak_merge_threshold=20,
                 loop_tolerance=.4,
                 use_lev_distance=False, use_gower_distance=True, use_text=True, use_font_dist=True,
                 use_tokens=True, use_loops=True, token_weight=1, loop_weight=1, font_weight=3,
                 lev_dist_weight=1, horizontal_scaling=0, diagonal_scaling=0, classify_text=True,
                 classify_list=True, classify_plot=True
                 ):
        self.set_attributes(horizontal_merge_threshold, vertical_merge_threshold, weak_merge,
                             horizontal_weak_merge_threshold, vertical_weak_merge_threshold,
                             loop_tolerance,
                             use_lev_distance, use_gower_distance, use_text, use_font_dist,
                             use_tokens, use_loops, token_weight, loop_weight, font_weight,
                             lev_dist_weight, horizontal_scaling, diagonal_scaling, classify_text,
                             classify_list, classify_plot)
        self.classifier = LoopClassifier(pdf, merge_boxes=merge_boxes, regress_parameters=regress_parameters,
                                     use_font=use_font, use_width=use_width, use_rect=use_rect, use_horizontal_overlap=use_horizontal_overlap,
                                     use_vertical_overlap=use_vertical_overlap,
                                     page_ratio_x=page_ratio_x, page_ratio_y=page_ratio_y, x_eps=x_eps, y_eps=y_eps,
                                     font_eps_h=font_eps_h, font_eps_v=font_eps_v,
                                     width_pct_eps=width_pct_eps, width_page_eps=width_page_eps)
        self.json = None
        self.rp = None

    def set_attributes(self, horizontal_merge_threshold=20, vertical_merge_threshold=20, weak_merge=True,
                     horizontal_weak_merge_threshold=20, vertical_weak_merge_threshold=20,
                     loop_tolerance = .4,
                     use_lev_distance=False, use_gower_distance=True, use_text=True, use_font_dist=True,
                     use_tokens=True, use_loops=True, token_weight=1, loop_weight=1, font_weight=3,
                     lev_dist_weight=1, horizontal_scaling=0, diagonal_scaling=0, classify_text=True,
                     classify_list=True, classify_plot=True):
        """

        :param horizontal_merge_threshold:
        :param vertical_merge_threshold:
        :param weak_merge:
        :param horizontal_weak_merge_threshold:
        :param vertical_weak_merge_threshold:
        :param loop_tolerance:
        :param use_lev_distance:
        :param use_gower_distance:
        :param use_text:
        :param use_font_dist:
        :param use_tokens:
        :param use_loops:
        :param token_weight:
        :param loop_weight:
        :param font_weight:
        :param lev_dist_weight:
        :param horizontal_scaling:
        :param diagonal_scaling:
        :param classify_text:
        :param classify_list:
        :param classify_plot:
        :return:
        """
        constants.HORIZONTAL_MERGE_THRESHOLD = horizontal_merge_threshold
        constants.VERTICAL_MERGE_THRESHOLD = vertical_merge_threshold
        constants.WEAK_MERGE = weak_merge
        constants.HORIZONTAL_WEAK_MERGE_THRESHOLD = horizontal_weak_merge_threshold
        constants.VERTICAL_WEAK_MERGE_THRESHOLD = vertical_weak_merge_threshold
        constants.LOOP_TOLERANCE = loop_tolerance
        constants.USE_LEV_DISTANCE = use_lev_distance
        constants.USE_GOWER_DISTANCE = use_gower_distance
        constants.USE_TEXT = use_text
        constants.USE_FONT_DIST = use_font_dist
        constants.USE_TOKENS = use_tokens
        constants.USE_LOOPS = use_loops
        constants.TOKEN_WEIGHT = token_weight
        constants.LOOP_WEIGHT = loop_weight
        constants.FONT_WEIGHT = font_weight
        constants.LEV_DIST_WEIGHT = lev_dist_weight
        constants.HORIZONTAL_SCALING = horizontal_scaling
        constants.DIAGONAL_SCALING = diagonal_scaling
        constants.CLASSIFY_TEXT = classify_text
        constants.CLASSIFY_LIST = classify_list
        constants.CLASSIFY_PLOT = classify_plot

    def segment_document(self):
        """

        :return:
        """
        self.json = self.classifier.classify_table_regions()

    def get_labeled_graphs(self):
        """

        :return:
        """
        return self.classifier.get_graphs()

    def segments2json(self):
        """

        :return:
        """
        if self.json is None:
            self.segment_document()
        return self.json

    def segments2text(self, annotate=True):
        """

        :param annotate:
        :return:
        """
        if self.json is None:
            self.segment_document()
        if self.rp is None:
            self.rp = ResultParser(self.json)
        return self.rp.get_text(annotate)
