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

if __name__ == '__main__':
    metrics='degree,in_degree,out_degree,betweenness,katz_centrality,pagerank,eigenvector_centrality,average_neighbor_degree,clustering_coefficient,square_clustering,closeness_centrality,degree_centrality,out_degree_centrality,in_degree_centrality,betweenness_centrality,load_centrality,number_of_cliques,core_number,number_ancestors,number_descendants,eccentricity,ripple_degree,inneredge_count,out_edge_count,in_variable_edge_count,strength,reverse_ripple'
    metrics=metrics.split(",")
    m:str
    for m in metrics:
        # print("SNA_"+m.upper()+"_DEPENDENCY_GRAPH = auto()")
        print("self.Keys.SNA_"+m.upper()+"_DEPENDENCY_GRAPH.value: nodeValues[\""+m+"\"][nodeID],")