from typing import Dict, Any
import pandas as pd
import logging
import coloredlogs
from emerge.analysis import Analysis


from emerge.graph import GraphRepresentation, GraphType
from emerge.log import Logger
LOGGER = Logger(logging.getLogger('analysis'))
def export_df(analysis:Analysis):
    local_metric_results: Dict[str, Dict[str, Any]] = analysis.get_local_metric_results()
    export_name=analysis.analysis_name+"-"
    export_metrics_as_df(local_metric_results,export_name, analysis.export_directory+"/"+analysis.project_name)
def export_metrics_as_df(
    # overall_metric_results: Dict[str, Any],
    local_metric_results: Dict[str, Dict[str, Any]], analysis_name: str, export_dir: str):
    if local_metric_results is not None and bool(local_metric_results):
        lms=local_metric_results.copy()
        LOGGER.info_start(f'the following local metrics were collected in {analysis_name}')
        results={}
        for node,metrics in lms.items():
            if("fan-in-inheritance-graph" in metrics.keys()):   
                m={}             
                for key in metrics.keys():                    
                    if"tag_" not in key:    
                        m[key]=metrics[key]
                        results[node]=m

    df=pd.DataFrame(results).T
    print(df)