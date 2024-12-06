# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['reconstructor']

package_data = \
{'': ['*'], 'reconstructor': ['.ipynb_checkpoints/*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'cmake>=3.24.1,<4.0.0',
 'cobra==0.22.1',
 'python-libsbml>=5.19.0,<6.0.0',
 'symengine>=0.9.2,<0.10.0',
 'unipath==1.1',
 'wget>=3.2,<4.0']

setup_kwargs = {
    'name': 'reconstructor',
    'version': '1.1.1',
    'description': 'COBRApy Compatible Genome Scale Metabolic Network Reconstruction Tool: Reconstructor',
    'long_description': '# Reconstructor\n## Installation:\n### Install Reconstructor python package\nThis can be done via pip in the command line\n\n```\npip install reconstructor\n```\n\n*You must be running >= Python 3.8\n\n## Test suite:\n#### Use the following command to run the test suite\nRun the following test to ensure reconstruction was installed correctly and is functional. This series of tests should take about an hour to run, dependent on computer/processor speed. These are runtimes for reconstructor on a 2020 MacBook Pro with a 1.4 GHz Quad-Core Intel Core i5 processor.\n\nUse the command below to test reconstructor to ensure correct installation.\n```\npython -m reconstructor --test yes\n```\n*YOU MUST RUN THE TEST SUITE BEFORE PROCEEDING TO USE RECONSTRUCTOR\n## Usage:\n### Use reconstructor via command line\nNow that reconstructor and all dependency databases are installed, you can proceed to use reconstructor via command line. An example would be:\n```\npython -m reconstructor --input <input fasta file> --type <1,2,3> --gram <negative, positive> --other arguments <args>\n```\n#### Type 1: Build GENRE from annotated amino acid fasta files\n```\npython -m reconstructor --input Osplanchnicus.aa.fasta --type 1 --gram negative --other_args <args>\n```\n\n#### Type 2: Build GENRE from BLASTp hits\n```\npython -m reconstructor --input Osplanchnicus.hits.out --type 2 --gram negative --other_args <args>\n```\n\n#### Type 3: Additional gap-filling (if necessary)\n```\npython -m reconstructor --input Osplanchnicus.sbml --type 3 --other_args <args>\n```\n### Required and optional arguments\n```\n--input <input file, Required>\n```\n```\n--type <input file type, .fasta = 1, diamond blastp output = 2, .sbml = 3, Required, Default = 1> \n```\n```\n--gram <Type of Gram classificiation (positive or negative), default = positive>\n```\n```\n--media <List of metabolites composing the media condition. Not required.>\n```\n```\n--tasks <List of metabolic tasks. Not required>\n```\n```\n--org <KEGG organism code. Not required>\n```\n```\n--min_frac <Minimum objective fraction required during gapfilling, default = 0.01>\n```\n```\n--max_frac <Maximum objective fraction allowed during gapfilling, default = 0.5>\n```\n```\n--out <Name of output GENRE file, default = default>\n```\n```\n--name <ID of output GENRE, default = default>\n```\n```\n--cpu <Number of processors to use, default = 1>\n```\n\n```\n--test <run installation tests, default = no>\n```\n## Additional Information\nThank you for your interest in reconstructor. If you have any additional questions please email tfz5vy@virginia.edu.\n\nIf you encounter any problems, please file an [issue](https://github.com/emmamglass/reconstructor/issues) along with a detailed description.\n\nDistributed under the terms of the [MIT license](https://github.com/emmamglass/reconstructor/blob/main/reconstructor/LICENSE), "reconstructor" is free and open source software\n',
    'author': 'Matt Jenior and Emma Glass',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
