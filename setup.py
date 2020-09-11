from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()
print(long_description)
setup(
  name='PDFSegmenter',
  packages=['PDFSegmenter', 'PDFSegmenter.util', 'PDFSegmenter.clustering', 'PDFSegmenter.detection',
            'PDFSegmenter.merging', 'PDFSegmenter.structure_recognition'],
  version='0.1',
  license='MIT',
  description='This library builds a graph-representation of the content of PDFs. The graph is then clustered, resulting page segments are classified and returned. Tables are retrieved formatted as a CSV.',
  long_description=long_description,
  author='Michael Aigner, Florian Preis',
  # author_email='your.email@domain.com',
  url='https://github.com/MBAigner/PDFSegmenter',
  download_url='https://github.com/MBAigner/PDFSegmenter/archive/v0.1.tar.gz',
  keywords=['pdf', 'document-processing', 'python', 'page-segmentation', 'layout-analysis',
            'cluster-analysis', 'annotations', 'csv', 'table', 'detection-model'],
  install_requires=[
      'numpy',
      'networkx==2.2',
      'scikit-learn==0.20.0',
      'GraphConverter==0.4',
      'editdistance==0.5.3'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
  ],
)
