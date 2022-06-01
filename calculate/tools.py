import logging
import os
from typing import Dict, Any
import pandas as pd




from emerge.log import Logger
LOGGER = Logger(logging.getLogger('analysis'))    
def export_features_json(local_metric_results: Dict[str, Dict[str, Any]],export_directory,project_name,analysis_name:str):
    export_name=analysis_name+"-features.json"
    LOGGER.info_start(f'the following local metrics were transformed to dataframe in {analysis_name}')
    local_metric_df=local_metrics_to_df(local_metric_results)
    export_path=os.path.join(export_directory,project_name,export_name)
    local_metric_df.to_json(export_path,orient="index" )


def local_metrics_to_df(local_metric_results: Dict[str, Dict[str, Any]])->pd.DataFrame:
    if local_metric_results is not None and bool(local_metric_results):
        
        results=[]
        for node,metrics in local_metric_results.items():
            if("fan-in-inheritance-graph" in metrics.keys()):   
                m={"node-id":node}
                for key in metrics.keys():                    
                    if("tag_" not in key) and ("entity" not in key) : 
                        m[key]=metrics[key]                        
                results.append(m)
    df=pd.DataFrame(results).set_index("node-id")
    return df
