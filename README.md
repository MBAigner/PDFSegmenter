# PDF Segmenter

This library builds a graph-representation of the content of PDFs. The graph is then clustered, resulting page segments are classified and returned. Tables are retrieved formatted as a CSV.

## How-to

* Pass the path of the PDF file which is wanted to be converted to ```PDFSegmenter```.
* Call the function ```convert()```. The document graph representations are returned page-wise as a list of ```networkx``` graphs.
* Media boxes of a PDF can be accessed using ```get_media_boxes()```, the page count over ```get_page_count()```

Example call: 

    segmenter = PDFSegmenter(pdf)
    result = segmenter.segments2json()
    text = segmenter.segments2text()

A file is the only parameter mandatory for the page segmentation.
Beside the graph conversion, media boxes of a document can be accessed using ```get_media_boxes()``` and the page count over ```get_page_count()```.
General document layout characteristics are stored in a ```converter.meta``` object.

A more detailed example usage is also given in ```Tester.py```.

## Example

The following image shows a resulting document graph representation when using the ```GraphConverter```.

<center><img src="./documentation/visibility_graph.png", height="300", width="200" /></center>


## Settings

General parameters:

* ```file```: file name
* ```merge_boxes```: indicating if PDF text boxes should be graph nodes, based on visual rectangles present in documents.
* ```regress_parameters```: indicating if graph parameters are regressed or used as a priori optimized default ones.

Edge restrictions:

* ```use_font```: differing font size
* ```use_width```: differing width
* ```use_rect```: nodes contained in differing visual structures
* ```use_horizontal_overlap```: indicating if horizontal edges should be built on overlap. If not, default deltas are used.
* ```use_vertical_overlap```: indicating if vertical edges should be built on overlap. If not, default deltas are used.

Edge thresholds:

* ```page_ratio_x```: maximal relative horizontal distance of two nodes where an edge can be created
* ```page_ratio_y```: maximal relative vertical distance of two nodes where an edge can be created
* ```x_eps```: alignment epsilon for vertical edges in points if ```use_horizontal_overlap``` is not enabled
* ```y_eps```: alignment epsilon for horizontal edges in points if ```use_vertical_overlap``` is not enabled
* ```font_eps_h```: indicates how much font sizes of nodes are allowed to differ as a constraint for building horizontal edges when ```use_font``` is enabled
* ```font_eps_v```: indicates how much font sizes of nodes are allowed to differ as a constraint for building vertical edges when ```use_font``` is enabled
* ```width_pct_eps```: relative width difference of nodes as a condition for vertical edges if ```use_width``` is enabled
* ```width_page_eps```: indicating at which maximal width of a node the width should act as an edge condition if ```use_width``` is enabled

## Project Structure

* ```GraphConverter.py```: contains the ```GraphConverter``` class for converting documents into graphs.
* ```models```:  contains regression models for layout-independent document processing
* ```document```: contains the ```DocumentMetaCharacteristics``` class for a layout-independent document processing or managing default thresholds
* ```merging```: contains the ```PDFTextBoxMerging``` class for an aggregation of layout elements treating the visual rectangle structures of a document
* ```util```:
  * ```constants```: paths, thresholds
  * ```StorageUtil```: store/load functionalities
  * ```RectangleUtil```: functionalities for visual rectangle constraints
* ```test/Tester.py```: Python script for testing the ```GraphConverter```
* ```pdf```: example PDF input files for tests

## Output Format

As a result, a list of ```networkx``` graphs is returned.
Each graph encapsulates a structured representation of a single page.

Edges are attributed with the following features:

* ```direction```: shows the direction of an edge.
    * ```v```: Vertical edge
    * ```h```: Horizontal edge
    * ```l```: Rectangular loop. This represents a novel concept encapsulating structural characteristics of document segments by observing if two different paths end up in the same node.
* ```length```: Scaled length of an edge
* ```lengthx_phys```: Horizontal edge length
* ```lengthy_phys```: Vertical edge length
* ```weight```: Scaled total length

All nodes contain the following content attributes:

* ```id```: unique identifier of the PDF element
* ```page```: page number, starting with 0
* ```text```: text of the PDF element
* ```x_0```: left x coordinate
* ```x_1```: right x coordinate
* ```y_0```: top y coordinate
* ```y_1```: bottom y coordinate
* ```pos_x```: center x coordinate
* ```pos_y```: center y coordinate
* ```abs_pos```: tuple containing a page independent representation of ```(pos_x,pos_y)``` coordinates
* ```original_font```: font as extracted by pdfminer
* ```font_name```: name of the font extracted from ```original_font```
* ```code```: font code as provided by pdfminer
* ```bold```: factor 1 indicating that a text is bold and 0 otherwise
* ```italic```: factor 1 indicating that a text is italic and 0 otherwise
* ```font_size```: size of the text in points
* ```masked```: text with numeric content substituted as #
* ```frequency_hist```: histogram of character type frequencies in a text, stored as a tuple containing percentages of textual, numerical, text symbolic and other symbols
* ```len_text```: number of characters
* ```n_tokens```: number of words
* ```tag```: tag for key-value pair extractions, indicating keys or values based on simple heuristics
* ```box```: box extracted by pdfminer Layout Analysis
* ```in_element_ids```: contains IDs of surrounding visual elements such as rectangles or lists. They are stored as a list [left, right, top, bottom]. -1 is indicating that there is no adjacent visual element.
* ```in_element```: indicates based on in_element_ids whether an element is stored in a visual rectangle representation (stored as "rectangle") or not (stored as "none").

The media boxes possess the following entries in a dictionary:

* ```x0```: Left x page crop box coordinate
* ```x1```: Right x page crop box coordinate
* ```y0```: Top y page crop box coordinate
* ```y1```: Bottom y page crop box coordinate
* ```x0page```: Left x page coordinate
* ```x1page```: Right x page coordinate
* ```y0page```: Top y page coordinate
* ```y1page```: Bottom y page coordinate


## Future Work

* The ```GraphConverter``` will be extended using OCR processing for images in order to support more unstructured types than solely PDFs.

## Acknowledgements

* Example PDFs are obtained from the ICDAR Table Recognition Challenge 2013 https://roundtrippdf.com/en/data-extraction/pdf-table-recognition-dataset/.

## Authors

* Michael Benedikt Aigner
* Florian Preis
