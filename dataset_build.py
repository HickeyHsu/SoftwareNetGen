import os,sys
import pandas as pd
from emerge import languages
from generate import GraphGenerator
from calculate.metrics.javaCodeMetric import extractCK
CK_METRICS=['cbo', 'cboModified', 'wmc',
    'dit', 'noc', 'rfc', 'lcom',  'totalMethodsQty',
    'staticMethodsQty', 'publicMethodsQty', 'privateMethodsQty',
    'protectedMethodsQty', 'defaultMethodsQty', 'visibleMethodsQty',
    'abstractMethodsQty', 'finalMethodsQty', 'synchronizedMethodsQty',
    'totalFieldsQty', 'staticFieldsQty', 'publicFieldsQty',
    'privateFieldsQty', 'protectedFieldsQty', 'defaultFieldsQty',
    'finalFieldsQty', 'synchronizedFieldsQty', 'nosi', 'returnQty',
    'loopQty', 'comparisonsQty', 'tryCatchQty', 'parenthesizedExpsQty',
    'stringLiteralsQty', 'numbersQty', 'assignmentsQty',
    'mathOperationsQty', 'variablesQty', 'maxNestedBlocksQty',
    'anonymousClassesQty', 'innerClassesQty', 'lambdasQty',
    'uniqueWordsQty', 'modifiers', 'logStatementsQty']
    # 排除的特征有 'tcc', 'lcc','lcom*', 'fanin', 'fanout', 'loc'
class DatasetBuilder:
    def __init__(self,data_directory,project_name,language) -> None:
        self.data_directory:str=data_directory
        self.project_name:str= project_name
        self.language:str= language
        # self.code
    def genSNA(self,version):
        graphGenerator =GraphGenerator()
        source_directory=os.path.join(self.data_directory,"src",self.project_name,self.project_name+"-"+version)
        output_dir=os.path.join(self.data_directory,"metric",self.project_name,self.project_name+"-"+version)
        local_metric_df:pd.DataFrame
        #gen graph
        if not os.path.exists(os.path.join(output_dir,"emerge")):
            os.makedirs(os.path.join(output_dir,"emerge"))
        local_metric_df=graphGenerator.generate_metricDF(source_directory,self.language,
            self.project_name,version,"graphml,feature,d3",os.path.join(output_dir,"emerge"))
        # save SNA metric
        local_metric_df.to_csv(os.path.join(output_dir,"metric.csv"))

    def mergeMetrics(self,version,mergeCK=True,mergeBug=False,extractSNA=False,extractCK=False):
        source_directory=os.path.join(self.data_directory,"src",self.project_name,self.project_name+"-"+version)
        output_dir=os.path.join(self.data_directory,"metric",self.project_name,self.project_name+"-"+version)
        out_name="SNA"
        # extract graph
        SNA_path=os.path.join(output_dir,"metric.csv")
        if extractSNA:
            self.genSNA(version)
        elif not os.path.exists(SNA_path):
            print(f"ERROR:{SNA_path} doesn`t exist!!!")
            return
        # read sna metric
        local_metric_df=pd.read_csv(SNA_path)        
        local_metric_df=local_metric_df[~local_metric_df["sna-abs-path"].isna()]
        local_metric_df=local_metric_df[local_metric_df['sna-abs-path']!="EXTERNAL"].set_index("sna-abs-path")
        # mergeCK
        if mergeCK:
            ck_data=self.getCKMetric(version,extractCK)
            if ck_data is not None:
                ck_data=ck_data[~ck_data['class'].str.contains("\$")].set_index('file')
                local_metric_df[CK_METRICS]=ck_data[CK_METRICS]
                for code_metric in CK_METRICS:
                    rename_dict = {code_metric: "code-"+code_metric}
                local_metric_df=local_metric_df.rename(columns=rename_dict)
                out_name+="-CK"                
        # mergeBug
        if mergeBug:            
            csv_file=os.path.join(self.data_directory,"csv",self.project_name,self.project_name+"-"+version+".csv")
            if os.path.exists(csv_file):
                csv_data=pd.read_csv(csv_file)
                csv_data['abs_path']=csv_data["File"].apply(lambda x:os.path.join(source_directory,x).replace("/","\\"))
                csv_data=csv_data.set_index('abs_path')
                local_metric_df['RealBugCount']=csv_data['RealBugCount']
                out_name+="-label"
            else:
                print(f"ERROR:{csv_file} doesn`t exist!!!")
        out_name+=".csv"
        local_metric_df.to_csv(os.path.join(output_dir,out_name))
        print("%s generated!!!" % os.path.join(output_dir,out_name))
    def getCKMetric(self,version,extract=False):        
        source_directory=os.path.join(self.data_directory,"src",self.project_name,self.project_name+"-"+version)
        output_dir=os.path.join(self.data_directory,"metric",self.project_name,self.project_name+"-"+version)
        if extract:
            extractCK(source_directory,output_dir)
        elif not os.path.exists(os.path.join(output_dir,"class.csv")):
            print("ERROR:class.csv doesn`t exist!!!")
            return None
        ck_data=pd.read_csv(os.path.join(output_dir,"class.csv"))
        return ck_data
    def mergeCK(self,version):
        output_dir=os.path.join(self.data_directory,"metric",self.project_name,self.project_name+"-"+version)
        ck_data=self.getCKMetric(version,extract=False)
        
        ck_data=ck_data[~ck_data['class'].str.contains("\$")].set_index('file')
        local_metric_df=pd.read_csv(os.path.join(output_dir,"metric.csv"))
        local_metric_df=local_metric_df[~local_metric_df['sna-abs-path'].isna()]
        local_metric_df=local_metric_df[local_metric_df['sna-abs-path']!="EXTERNAL"].set_index('sna-abs-path')
        local_metric_df[CK_METRICS]=ck_data[CK_METRICS]
        print(local_metric_df[CK_METRICS])
        
if __name__ == '__main__':
    data_directory=r"D:\data_sci\dataset_jira"
    project_name="activemq"
    version="5.0.0"
    language="java"
    datasetBuilder =DatasetBuilder(data_directory,project_name,language)
    # datasetBuilder.mergeMetrics(version,mergeCK=True,mergeBug=True,extractSNA=True,extractCK=True)
    datasetBuilder.mergeMetrics(version,mergeCK=True,mergeBug=True,extractSNA=False,extractCK=False)

