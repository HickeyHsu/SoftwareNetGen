import os,json
from emerge.metrics.social.social import SocialNetworkMetric
# from generate import GraphGenerator
# def generation():
#     graphGenerator=GraphGenerator()
#     setting={
#         'project_name': 'joern-javaTools', 
#         'ignore_dependencies_containing': [],
#         'only_permit_file_extensions': ['.java'], 
#         'source_directory': 'D:\\idea_workspace\\joern-javaTools', 
#         'analysis_name': 'test', 
#         'export': {'directory': 'out', 'graphml': '', 'd3': ''}, 
#         'file_scan': [
#             'number_of_methods', 
#             'source_lines_of_code', 
#             'dependency_graph', 
#             'louvain_modularity', 
#             'fan_in_out',
#             "sna"
#         ]}
#     graphGenerator.start_with_config(setting,True,False,False)

def read_content():
    dataset=json.load(open('/home/hickey/data/dataset_jira/data.json', 'r'))
    print(dataset)

def test_re():
    import re
    ori="\"sna-eigenvector-centrality-dependency-graph\":-126108311117.9454650879,"
    new=re.sub(r"-(\D)",r"_\1",ori)
    print(new)
def metric_test():
    # import pandas as pd
    # score1 = {'n1': 0.00000006727777777777777, 'n2': 0.0000000000004377777777777777777,'n3': 0.000002767777777777777777}
    # score2={'n1': 0.000000000000000000006727777777777777, 'n2': 0.000000000000000000004377777777777777777,'n3': 0.000000000000000000002767777777777777777}
    # mets={"score1":score1,"score2":score2}
    # df=pd. DataFrame.from_dict(mets,orient="columns")
    # print(df)
    rename_cols={}
    metrics=['betweenness','betweenness_centrality','square_clustering',
        'reverse_ripple','number_of_cliques','katz_centrality',
        'degree', 'in_degree', 'out_degree', 
        'pagerank', 'eigenvector_centrality', 
        'average_neighbor_degree', 'clustering_coefficient',
        'closeness_centrality', 
        'degree_centrality', 'out_degree_centrality', 'in_degree_centrality', 
        'load_centrality', 
        'core_number', 'number_ancestors', 'number_descendants', 
        'eccentricity', 'ripple_degree',
        # 'inneredge_count', 'out_edge_count', 'in_variable_edge_count',
        
    ]
    for k in metrics:
        newk=k.replace("_","-")
        rename_cols[k]=f"sna-{newk}-dependency-graph"
    print(rename_cols)
if __name__ == '__main__':
    metric_test()
