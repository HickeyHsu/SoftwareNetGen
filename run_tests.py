"""
Discover and run all unit tests.
"""

# Authors: Grzegorz Lato <grzegorz.lato@gmail.com>
# License: MIT

# import unittest
# from interrogate import coverage

# # first check all available unit tests
# loader = unittest.TestLoader()
# start_dir = 'emerge'
# suite = loader.discover(start_dir)

# runner = unittest.TextTestRunner(verbosity=2)
# runner.run(suite)

# # now check docstring coverage with interrogate
# cov = coverage.InterrogateCoverage(paths=["."])
# results = cov.get_coverage()
# print(f'\nInterrogate docstring coverage: {(results.covered/results.total) * 100 :.2f}%')
import sys,json
from generate import GraphGenerator

if __name__ == '__main__':
    # dataset=json.load(open('/home/hickey/data/dataset_jira/data.json', 'r'))
    # print(dataset['camel'])
    
    # graphGenerator=GraphGenerator()
    sys.argv.pop(0)
    print(sys.argv)