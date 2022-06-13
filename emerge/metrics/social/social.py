"""
Contains an implementation of the louvain modularity graph metric.
"""

# Authors: Grzegorz Lato <grzegorz.lato@gmail.com>
# License: MIT

from datetime import datetime
from typing import Dict, Any
from enum import auto
import logging
import coloredlogs
from multiprocessing import Pool,Manager,cpu_count
from networkx import DiGraph
from calculate.localMetrics import LocalMetrics
from calculate.tools import max_min_dict_values
from emerge.abstractresult import AbstractResult
from emerge.log import Logger
from emerge.graph import GraphRepresentation
from emerge.core import format_timedelta

# enums and superclass of the given metric
from emerge.metrics.abstractmetric import EnumLowerKebabCase
from emerge.metrics.metrics import GraphMetric


LOGGER = Logger(logging.getLogger('metrics'))
coloredlogs.install(level='E', logger=LOGGER.logger(), fmt=Logger.log_format)

class SocialNetworkMetric(GraphMetric):
    class Keys(EnumLowerKebabCase):
        SNA_DEGREE_DEPENDENCY_GRAPH = auto()
        SNA_IN_DEGREE_DEPENDENCY_GRAPH = auto()
        SNA_OUT_DEGREE_DEPENDENCY_GRAPH = auto()
        SNA_BETWEENNESS_DEPENDENCY_GRAPH = auto()
        SNA_KATZ_CENTRALITY_DEPENDENCY_GRAPH = auto()
        SNA_PAGERANK_DEPENDENCY_GRAPH = auto()
        SNA_EIGENVECTOR_CENTRALITY_DEPENDENCY_GRAPH = auto()
        SNA_AVERAGE_NEIGHBOR_DEGREE_DEPENDENCY_GRAPH = auto()
        SNA_CLUSTERING_COEFFICIENT_DEPENDENCY_GRAPH = auto()
        SNA_SQUARE_CLUSTERING_DEPENDENCY_GRAPH = auto()
        SNA_CLOSENESS_CENTRALITY_DEPENDENCY_GRAPH = auto()
        SNA_DEGREE_CENTRALITY_DEPENDENCY_GRAPH = auto()
        SNA_OUT_DEGREE_CENTRALITY_DEPENDENCY_GRAPH = auto()
        SNA_IN_DEGREE_CENTRALITY_DEPENDENCY_GRAPH = auto()
        SNA_BETWEENNESS_CENTRALITY_DEPENDENCY_GRAPH = auto()
        SNA_LOAD_CENTRALITY_DEPENDENCY_GRAPH = auto()
        SNA_NUMBER_OF_CLIQUES_DEPENDENCY_GRAPH = auto()
        SNA_CORE_NUMBER_DEPENDENCY_GRAPH = auto()
        SNA_NUMBER_ANCESTORS_DEPENDENCY_GRAPH = auto()
        SNA_NUMBER_DESCENDANTS_DEPENDENCY_GRAPH = auto()
        SNA_ECCENTRICITY_DEPENDENCY_GRAPH = auto()
        SNA_RIPPLE_DEGREE_DEPENDENCY_GRAPH = auto()
        # SNA_INNEREDGE_COUNT_DEPENDENCY_GRAPH = auto()
        # SNA_OUT_EDGE_COUNT_DEPENDENCY_GRAPH = auto()
        # SNA_IN_VARIABLE_EDGE_COUNT_DEPENDENCY_GRAPH = auto()
        SNA_REVERSE_RIPPLE_DEPENDENCY_GRAPH = auto()    
        SNA_ABS_PATH = auto()  
    def __init__(self, analysis, graph_representations: Dict):
        super().__init__(analysis, graph_representations)
        # self.__metrics=['degree', 'in_degree', 'out_degree', 'betweenness',
        #      'katz_centrality', 'pagerank', 'eigenvector_centrality', 
        #     'average_neighbor_degree', 'clustering_coefficient',
        #     'square_clustering', 'closeness_centrality', 
        #     'degree_centrality', 'out_degree_centrality', 'in_degree_centrality', 
        #     'betweenness_centrality', 'load_centrality', 
        #     'number_of_cliques', 'core_number', 'number_ancestors', 'number_descendants', 
        #     'eccentricity', 'ripple_degree',
        #     # 'inneredge_count', 'out_edge_count', 'in_variable_edge_count',
        #     'reverse_ripple'
        # ]

        #重新排列计算顺序，使耗时长的先计算以充分利用cpu资源
        self.__metrics=['betweenness','betweenness_centrality','square_clustering',
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
        self.result={}

    def calculate_from_results(self, results: Dict[str, AbstractResult]):
        self._calculate_metric_data(results)
    
    def _calculate_metric_data(self, results: Dict[str, AbstractResult]):
        instances = [x for x in [self.dependency_graph_representation] if x]
        graph_instance: GraphRepresentation
        for graph_instance in instances:
            digraph: DiGraph = graph_instance.digraph
            mlMetric=LocalMetrics(digraph)
            nodesIDs=digraph.nodes()
            # 多进程
            cpu=cpu_count()
            if cpu<8:
                LOGGER.info(f"本机使用{cpu}核CPU，核数小于8,不启用多进程提取SNA指标")
                for m in self.__metrics:
                    self.result[m]=mlMetric.calMetric(m,nodesIDs)
            else:
                LOGGER.info(f"本机使用{cpu}核CPU，启用{cpu-2}进程提取SNA指标")
                pool = Pool(processes=cpu_count()-2)
                q=Manager().Queue()
                jobs=[] #线程储存
                for m in self.__metrics:
                    job=pool.apply_async(func=self.task, args=(q,mlMetric,m,))
                    jobs.append(job)
                pool.close()
                pool.join()
                mpResults = [q.get() for j in jobs] 
                for r in mpResults:
                    self.result[r[0]]=r[1]
            nodeValues=self.result
            #针对某些数值特殊处理
            need_zscore=["betweenness","eigenvector_centrality",'betweenness_centrality',
            'katz_centrality','closeness_centrality', 
            'degree_centrality', 'out_degree_centrality', 'in_degree_centrality', 
            'load_centrality']
            for column in need_zscore:
                nodeValues[column]=max_min_dict_values(nodeValues[column].copy())
            
            for node_with_unique_result_name in nodesIDs:
                nodeID=node_with_unique_result_name
                if "absolute_name" not in nodesIDs[nodeID]:
                    nodesIDs[nodeID]["absolute_name"]="EXTERNAL"
                data={
                    self.Keys.SNA_ABS_PATH.value:nodesIDs[nodeID]["absolute_name"],
                    self.Keys.SNA_DEGREE_DEPENDENCY_GRAPH.value: nodeValues["degree"][nodeID],
                    self.Keys.SNA_IN_DEGREE_DEPENDENCY_GRAPH.value: nodeValues["in_degree"][nodeID],
                    self.Keys.SNA_OUT_DEGREE_DEPENDENCY_GRAPH.value: nodeValues["out_degree"][nodeID],
                    self.Keys.SNA_BETWEENNESS_DEPENDENCY_GRAPH.value: nodeValues["betweenness"][nodeID],
                    self.Keys.SNA_KATZ_CENTRALITY_DEPENDENCY_GRAPH.value: nodeValues["katz_centrality"][nodeID],
                    self.Keys.SNA_PAGERANK_DEPENDENCY_GRAPH.value: nodeValues["pagerank"][nodeID],
                    #for json dump without science counting, eigenvector_centrality would be multipiped 10^12
                    self.Keys.SNA_EIGENVECTOR_CENTRALITY_DEPENDENCY_GRAPH.value: nodeValues["eigenvector_centrality"][nodeID]* 1e12,
                    self.Keys.SNA_AVERAGE_NEIGHBOR_DEGREE_DEPENDENCY_GRAPH.value: nodeValues["average_neighbor_degree"][nodeID],
                    self.Keys.SNA_CLUSTERING_COEFFICIENT_DEPENDENCY_GRAPH.value: nodeValues["clustering_coefficient"][nodeID],
                    self.Keys.SNA_SQUARE_CLUSTERING_DEPENDENCY_GRAPH.value: nodeValues["square_clustering"][nodeID],
                    self.Keys.SNA_CLOSENESS_CENTRALITY_DEPENDENCY_GRAPH.value: nodeValues["closeness_centrality"][nodeID],
                    self.Keys.SNA_DEGREE_CENTRALITY_DEPENDENCY_GRAPH.value: nodeValues["degree_centrality"][nodeID],
                    self.Keys.SNA_OUT_DEGREE_CENTRALITY_DEPENDENCY_GRAPH.value: nodeValues["out_degree_centrality"][nodeID],
                    self.Keys.SNA_IN_DEGREE_CENTRALITY_DEPENDENCY_GRAPH.value: nodeValues["in_degree_centrality"][nodeID],
                    self.Keys.SNA_BETWEENNESS_CENTRALITY_DEPENDENCY_GRAPH.value: nodeValues["betweenness_centrality"][nodeID],
                    self.Keys.SNA_LOAD_CENTRALITY_DEPENDENCY_GRAPH.value: nodeValues["load_centrality"][nodeID],
                    self.Keys.SNA_NUMBER_OF_CLIQUES_DEPENDENCY_GRAPH.value: nodeValues["number_of_cliques"][nodeID],
                    self.Keys.SNA_CORE_NUMBER_DEPENDENCY_GRAPH.value: nodeValues["core_number"][nodeID],
                    self.Keys.SNA_NUMBER_ANCESTORS_DEPENDENCY_GRAPH.value: nodeValues["number_ancestors"][nodeID],
                    self.Keys.SNA_NUMBER_DESCENDANTS_DEPENDENCY_GRAPH.value: nodeValues["number_descendants"][nodeID],
                    self.Keys.SNA_ECCENTRICITY_DEPENDENCY_GRAPH.value: nodeValues["eccentricity"][nodeID],
                    self.Keys.SNA_RIPPLE_DEGREE_DEPENDENCY_GRAPH.value: nodeValues["ripple_degree"][nodeID],
                    # self.Keys.SNA_INNEREDGE_COUNT_DEPENDENCY_GRAPH.value: nodeValues["inneredge_count"][nodeID],
                    # self.Keys.SNA_OUT_EDGE_COUNT_DEPENDENCY_GRAPH.value: nodeValues["out_edge_count"][nodeID],
                    # self.Keys.SNA_IN_VARIABLE_EDGE_COUNT_DEPENDENCY_GRAPH.value: nodeValues["in_variable_edge_count"][nodeID],
                    self.Keys.SNA_REVERSE_RIPPLE_DEPENDENCY_GRAPH.value: nodeValues["reverse_ripple"][nodeID]
                }
                
                if node_with_unique_result_name in self.local_data:
                    self.local_data[node_with_unique_result_name].update(data)
                else:
                    self.local_data[node_with_unique_result_name] = data
    def task(self,q,mlMetric:LocalMetrics,m):
        start_time = datetime.now()
        q.put((m,mlMetric.calMetric(m),))
        dur_time = format_timedelta(datetime.now()-start_time, '%H:%M:%S + %s ms')
        LOGGER.info_done(f"calculate {m} finished in time: {dur_time}")
if __name__ == '__main__':
    metrics='degree,in_degree,out_degree,betweenness,katz_centrality,pagerank,eigenvector_centrality,average_neighbor_degree,clustering_coefficient,square_clustering,closeness_centrality,degree_centrality,out_degree_centrality,in_degree_centrality,betweenness_centrality,load_centrality,number_of_cliques,core_number,number_ancestors,number_descendants,eccentricity,ripple_degree,inneredge_count,out_edge_count,in_variable_edge_count,strength,reverse_ripple'
    metrics=metrics.split(",")
    m:str
    for m in metrics:
        # print("SNA_"+m.upper()+"_DEPENDENCY_GRAPH = auto()")
        print("self.Keys.SNA_"+m.upper()+"_DEPENDENCY_GRAPH.value: nodeValues["+m+"][nodeID]")