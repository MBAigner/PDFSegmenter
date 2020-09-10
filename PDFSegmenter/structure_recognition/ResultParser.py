
class ResultParser(object):

    MARK_SEGMENTS = True

    def __init__(self, doc):
        self.doc = doc
        self.parsed = False

    def parse_content(self):
        for page in self.doc:
            # sort clusters
            bbox = self.doc[page]["bounding_box"]
            del self.doc[page]["bounding_box"]
            page_content = list(self.doc[page].values())
            page_clusters = list(self.doc[page].keys())
            for i, elt in enumerate(page_content):
                elt["cluster"] = page_clusters[i]
            page_content = sorted(page_content,
                                  key=lambda x: [x["bounding_box"][2], x["bounding_box"][0]],
                                  reverse=False)
            page_content = {x["cluster"]: x for x in page_content}
            self.doc[page] = page_content
            # iterate and convert
            for cluster in self.doc[page]:
                contents = self.doc[page][cluster]["content"]
                contents = sorted(contents,
                                  key=lambda x: [round(x["y_0"]), round(x["x_0"])],
                                  reverse=False)
                element = self.doc[page][cluster]["element"]
                if element in ["text", "none"]:
                    self.doc[page][cluster]["text"] = "\n".join(list(map(lambda x: x["text"], contents)))
                else:
                    text = ""
                    prev_y = 0
                    for el in contents:
                        # print(str(round(el["y_0"])) + " " + str(round(el["x_0"])))
                        text += ("\n" if round(el["y_0"]) != prev_y else ";") + el["text"].strip()
                        prev_y = round(el["y_0"])
                    self.doc[page][cluster]["text"] = text[1:]
            self.doc[page]["bounding_box"] = bbox
        self.parsed = True
        return self.doc

    def get_text(self):
        if not self.parsed:
            self.parse_content()
        text = ""
        for page in self.doc:
            for cluster in self.doc[page]:
                if cluster != "bounding_box":

                    text += self.get_segment_marker(self.doc[page][cluster])
                    text += self.doc[page][cluster]["text"] + "\n"
        return text

    def get_segment_marker(self, segment):
        return "\n[!" + segment["element"].upper() + "]\n" if self.MARK_SEGMENTS else ""
