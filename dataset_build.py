import os
import pandas as pd
from emerge import languages
from generate import GraphGenerator


class DatasetBuilder:
    def __init__(self,data_directory,project_name,language) -> None:
        self.data_directory:str=data_directory
        self.project_name:str= project_name
        self.language:str= language
        # self.code
    def start(self,version):
        graphGenerator =GraphGenerator()
        source_directory=os.path.join(self.data_directory,"src",self.project_name,self.project_name+"-"+version)
        output_dir=os.path.join(self.data_directory,"metric",self.project_name,self.project_name+"-"+version)
        local_metric_df:pd.DataFrame
        local_metric_df=graphGenerator.generate_metricDF(source_directory,self.language,
            self.project_name,version,"graphml,feature,d3",os.path.join(output_dir,"emerge"))
        print(local_metric_df)
        if not os.path.exists(os.path.join(output_dir,"emerge")):
            os.makedirs(os.path.join(output_dir,"emerge"))
        local_metric_df.to_csv(os.path.join(output_dir,"emerge","metric.csv"))
        print(len(local_metric_df))
        csv_file=os.path.join(self.data_directory,"csv",self.project_name,self.project_name+"-"+version+".csv")
        csv_data=pd.read_csv(csv_file)
        csv_data['abs_path']=csv_data["File"].apply(lambda x:os.path.join(source_directory,x))
        print(csv_data)
    def mergeBug(self,version):
        source_directory=os.path.join(self.data_directory,"src",self.project_name,self.project_name+"-"+version)
        output_dir=os.path.join(self.data_directory,"metric",self.project_name,self.project_name+"-"+version)
        
        local_metric_df=pd.read_csv(os.path.join(output_dir,"emerge","metric.csv"))
        local_metric_df=local_metric_df[~local_metric_df["sna-abs-path"].isna()].set_index("sna-abs-path")

        csv_file=os.path.join(self.data_directory,"csv",self.project_name,self.project_name+"-"+version+".csv")
        csv_data=pd.read_csv(csv_file)
        csv_data['abs_path']=csv_data["File"].apply(lambda x:os.path.join(source_directory,x).replace("/","\\"))
        csv_data=csv_data.set_index('abs_path')

        local_metric_df['RealBugCount']=csv_data['RealBugCount']
        local_metric_df.to_csv(os.path.join(output_dir,"emerge","merged.csv"))
        print(len(local_metric_df))
if __name__ == '__main__':
    data_directory=r"D:\data_sci\dataset_jira"
    project_name="activemq"
    version="5.0.0"
    language="java"
    datasetBuilder =DatasetBuilder(data_directory,project_name,language)
    # datasetBuilder.start(version)
    datasetBuilder.mergeBug(version)



