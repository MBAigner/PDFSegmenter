from PDFSegmenter.PDFSegmenter import PDFSegmenter

segmenter = PDFSegmenter("../pdf/eu-001.pdf")
segmenter.segment_document()
text = segmenter.segments2text(annotate=True)
plain_text = segmenter.segments2text(annotate=False)
json = segmenter.segments2json()
graphs = segmenter.get_labeled_graphs()
print(graphs)
