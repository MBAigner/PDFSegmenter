
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


    def set_attributes(self, horizontal_merge_threshold=20, vertical_merge_threshold=20, weak_merge=True,
                     horizontal_weak_merge_threshold=20, vertical_weak_merge_threshold=20,
                     loop_tolerance = .4,
                     use_lev_distance=False, use_gower_distance=True, use_text=True, use_font_dist=True,
                     use_tokens=True, use_loops=True, token_weight=1, loop_weight=1, font_weight=3,
                     lev_dist_weight=1, horizontal_scaling=0, diagonal_scaling=0, classify_text=True,
                     classify_list=True, classify_plot=True):
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

    def get_graphs(self):
        return self.classifier.get_graphs()
