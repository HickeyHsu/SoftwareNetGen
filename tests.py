import os,json
from generate import GraphGenerator
def generation():
    graphGenerator=GraphGenerator()
    setting={
        'project_name': 'joern-javaTools', 
        'ignore_dependencies_containing': [],
        'only_permit_file_extensions': ['.java'], 
        'source_directory': 'D:\\idea_workspace\\joern-javaTools', 
        'analysis_name': 'test', 
        'export': {'directory': 'out', 'graphml': '', 'd3': ''}, 
        'file_scan': [
            'number_of_methods', 
            'source_lines_of_code', 
            'dependency_graph', 
            'louvain_modularity', 
            'fan_in_out',
            "sna"
        ]}
    graphGenerator.start_with_config(setting,True,False,False)

def read_content():
    dataset=json.load(open('/home/hickey/data/dataset_jira/data.json', 'r'))
    print(dataset)