from PDFSegmenter.util import constants


class TableClusterMerging(object):

    def __init__(self, result):
        self.result = result

    def get_merged_results(self):
        for page in self.result:
            prev = None
            for elt in ["table"]:  # TODO possibly adapt for lists (but with consideration of none and text inbetween)
                delete_parts = []
                for tab_id in TableClusterMerging.get_elements(self.result[page], elt):
                    table = self.result[page][tab_id]
                    if prev is not None:
                        pt = self.result[page][prev]
                        if (constants.WEAK_MERGE and self.is_weak_adjacent(pt, table)) or \
                            (not constants.WEAK_MERGE and (self.is_included(pt, table)
                                                           or self.is_adjacent(pt, table))):
                            self.result[page][prev]["bounding_box"] = (min(pt["bounding_box"][0], table["bounding_box"][0]),
                                                                       max(pt["bounding_box"][1], table["bounding_box"][1]),
                                                                       min(pt["bounding_box"][2], table["bounding_box"][2]),
                                                                       max(pt["bounding_box"][3], table["bounding_box"][3]))
                            self.result[page][prev]["content"] = self.result[page][prev]["content"] + table["content"]
                            table = None
                            delete_parts.append(tab_id)
                    prev = tab_id if table is not None else prev
                for part in sorted(delete_parts, reverse=True):
                    del self.result[page][part]
        return self.result

    @staticmethod
    def get_elements(result_page, elt):
        return {k: v for k, v in result_page.items() if k != "bounding_box" and
                result_page[k]["element"] == elt}

    @staticmethod
    def is_adjacent(pt, table):
        # check if table1 y1 = table2 y0 or vice versa
        # or: table1 x1 = table2 x0 or vice versa
        return (
                # vertically adjacent tables
                abs(pt["bounding_box"][0] - table["bounding_box"][0]) < constants.HORIZONTAL_MERGE_THRESHOLD and
                abs(pt["bounding_box"][1] - table["bounding_box"][1]) < constants.HORIZONTAL_MERGE_THRESHOLD and
                (
                        abs(pt["bounding_box"][3] - table["bounding_box"][2]) < constants.VERTICAL_MERGE_THRESHOLD or
                        abs(pt["bounding_box"][2] - table["bounding_box"][3]) < constants.VERTICAL_MERGE_THRESHOLD

                )) or \
                (
                # horizontally adjacent tables
                abs(pt["bounding_box"][2] - table["bounding_box"][2]) < constants.VERTICAL_MERGE_THRESHOLD and
                abs(pt["bounding_box"][3] - table["bounding_box"][3]) < constants.VERTICAL_MERGE_THRESHOLD and
                (
                        abs(pt["bounding_box"][0] - table["bounding_box"][1]) < constants.HORIZONTAL_MERGE_THRESHOLD or
                        abs(pt["bounding_box"][1] - table["bounding_box"][0]) < constants.HORIZONTAL_MERGE_THRESHOLD
                ))

    @staticmethod
    # table contained in other table
    def is_included(pt, table):
        return (
                        pt["bounding_box"][0] >= table["bounding_box"][0] and
                        pt["bounding_box"][1] <= table["bounding_box"][1] and
                        pt["bounding_box"][2] >= table["bounding_box"][2] and
                        pt["bounding_box"][3] <= table["bounding_box"][3]
                ) or (
                        table["bounding_box"][0] >= pt["bounding_box"][0] and
                        table["bounding_box"][1] <= pt["bounding_box"][1] and
                        table["bounding_box"][2] >= pt["bounding_box"][2] and
                        table["bounding_box"][3] <= pt["bounding_box"][3]
                )

    @staticmethod
    def is_weak_adjacent(pt, table):
        shared_axis = TableClusterMerging.shares_same_axis(pt, table)
        overlap_axis = TableClusterMerging.is_one_dimensional_overlapping(pt, table)
        if overlap_axis == 0 or shared_axis == 0:
            return False
        return overlap_axis != shared_axis or overlap_axis == 3

    @staticmethod
    def is_one_dimensional_overlapping(pt, table):
        overlap_axis = 0
        if (max(pt["bounding_box"][0], table["bounding_box"][0]) <=
                min(pt["bounding_box"][1], table["bounding_box"][1])):
            overlap_axis += 1
        if (max(pt["bounding_box"][2], table["bounding_box"][2]) <=
                min(pt["bounding_box"][3], table["bounding_box"][3])):
            overlap_axis += 2
        return overlap_axis

    @staticmethod
    def shares_same_axis(pt, table):
        axis_shared = 0
        if abs(pt["bounding_box"][0] - table["bounding_box"][0]) < constants.HORIZONTAL_WEAK_MERGE_THRESHOLD or \
           abs(pt["bounding_box"][1] - table["bounding_box"][1]) < constants.HORIZONTAL_WEAK_MERGE_THRESHOLD or \
           abs(pt["bounding_box"][0] - table["bounding_box"][1]) < constants.HORIZONTAL_WEAK_MERGE_THRESHOLD or \
           abs(pt["bounding_box"][1] - table["bounding_box"][0]) < constants.HORIZONTAL_WEAK_MERGE_THRESHOLD:
            axis_shared += 1
        if abs(pt["bounding_box"][2] - table["bounding_box"][2]) < constants.VERTICAL_WEAK_MERGE_THRESHOLD or \
           abs(pt["bounding_box"][3] - table["bounding_box"][3]) < constants.VERTICAL_WEAK_MERGE_THRESHOLD or \
           abs(pt["bounding_box"][2] - table["bounding_box"][3]) < constants.VERTICAL_WEAK_MERGE_THRESHOLD or \
           abs(pt["bounding_box"][3] - table["bounding_box"][2]) < constants.VERTICAL_WEAK_MERGE_THRESHOLD:
            axis_shared += 2
        return axis_shared
