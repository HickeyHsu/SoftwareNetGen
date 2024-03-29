from hashlib import md5
import os
import pandas as pd
from calculate.tools import LOGGER
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
    'uniqueWordsQty', 'modifiers', 'logStatementsQty']# 排除的特征有 'tcc', 'lcc','lcom*', 'fanin', 'fanout', 'loc'
    
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
            self.project_name,version,
            None,"graphml,feature,d3",os.path.join(output_dir,"emerge"))
        # save SNA metric
        local_metric_df.to_csv(os.path.join(output_dir,"metric.csv"))

    def mergeMetrics(self,version,mergeCK=True,mergeBug=False,extractSNA=False,extractCK=False):
        source_directory=self.__source_directory(version)
        output_dir=self.__output_dir(version)
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
        local_metric_df["sna-abs-path"]=local_metric_df["sna-abs-path"].apply(lambda x:x.replace("\\","/"))
        local_metric_df=local_metric_df[local_metric_df['sna-abs-path']!="EXTERNAL"].set_index("sna-abs-path")
        # mergeCK
        if mergeCK:
            ck_data=self.getCKMetric(version,extractCK)            
            if ck_data is not None:
                ck_data=ck_data[~ck_data['class'].str.contains("\$")].groupby('file').sum()
                ck_data.index=ck_data.index.map(lambda x:x.replace("\\","/"))
                local_metric_df[CK_METRICS]=ck_data[CK_METRICS]
                for code_metric in CK_METRICS:
                    rename_dict = {code_metric: "code-"+code_metric}
                local_metric_df=local_metric_df.rename(columns=rename_dict)
                out_name+="-CK" 
            else:
                LOGGER.warning("ck_data doesn't exist")
        # mergeBug
        if mergeBug:
            # LOGGER.info_start(f"merge bug data for {self.project_name}-{version}")
            csv_file=os.path.join(self.data_directory,"csv",self.project_name,self.project_name+"-"+version+".csv")
            if os.path.exists(csv_file):
                csv_data=pd.read_csv(csv_file)
                csv_data['abs_path']=csv_data["File"].apply(lambda x:os.path.join(source_directory,x).replace("\\","/"))
                csv_data=csv_data.set_index('abs_path')
                local_metric_df['RealBugCount']=csv_data['RealBugCount']
                out_name+="-label"
            else:
                print(f"ERROR:{csv_file} doesn`t exist!!!")
        out_name+=".csv"
        local_metric_df.to_csv(os.path.join(output_dir,out_name))
        LOGGER.info_done("%s generated!!!" % os.path.join(output_dir,out_name))
    def getCKMetric(self,version,extract=False):        
        source_directory=self.__source_directory(version)
        output_dir=self.__output_dir(version)
        if extract:
            extractCK(source_directory,output_dir)
        elif not os.path.exists(os.path.join(output_dir,"class.csv")):
            print("ERROR:class.csv doesn`t exist!!!")
            return None
        ck_data=pd.read_csv(os.path.join(output_dir,"class.csv"))
        return ck_data
    def mergeCK(self,version):
        output_dir=self.__output_dir(version)
        ck_data=self.getCKMetric(version,extract=False)
        
        ck_data=ck_data[~ck_data['class'].str.contains("\$")].groupby('file').sum()
        local_metric_df=pd.read_csv(os.path.join(output_dir,"metric.csv"))
        local_metric_df=local_metric_df[~local_metric_df['sna-abs-path'].isna()]
        local_metric_df=local_metric_df[local_metric_df['sna-abs-path']!="EXTERNAL"].set_index('sna-abs-path')
        local_metric_df[CK_METRICS]=ck_data[CK_METRICS]
        print(local_metric_df[CK_METRICS])
    
    def dataset_build_seq(self,train_versions:list[str],CK=True):
        train_data=self.auto_gen_trainset(train_versions,CK)

    def auto_gen_trainset(self,versions:list[str],CK=True,force=False):
        datas=[]
        for version in versions:
            output_dir=self.__output_dir(version)
            out_name=self.__out_name(CK)
            if force:
                self.mergeMetrics(version,mergeCK=CK,mergeBug=True,extractSNA=True,extractCK=True)
            # elif not os.path.exists(os.path.join(output_dir,out_name)):
            else:
                extractSNA=False
                extractCK=False
                if not os.path.exists(os.path.join(output_dir,"metric.csv")):
                    extractSNA=True
                if not os.path.exists(os.path.join(output_dir,"class.csv")):
                    extractCK=True
                self.mergeMetrics(version,mergeCK=CK,mergeBug=True,extractSNA=extractSNA,extractCK=extractCK)

            data=pd.read_csv(os.path.join(output_dir,out_name))
            data['id']=version+"-"+data["node-id"]
            data=data.set_index("id")
            datas.append(data)
        train_data:pd.DataFrame=pd.concat(datas,join="inner",axis=0)
        train_data.to_csv(os.path.join(self.data_directory,"metric",self.project_name,"train.csv"))
        return train_data
    def __source_directory(self,version):
        return os.path.join(self.data_directory,"src",self.project_name,self.project_name+"-"+version)
    def __output_dir(self,version):
        return os.path.join(self.data_directory,"metric",self.project_name,self.project_name+"-"+version)
    def __out_name(self,CK):
        out_name="SNA"
        if CK : 
            out_name+="-CK"
        out_name+="-label.csv"
        return out_name
    def test(self,version):
        source_directory=self.__source_directory(version)
        output_dir=self.__output_dir(version)
        # read sna metric
        # SNA_path=os.path.join(output_dir,"metric.csv")
        # local_metric_df=pd.read_csv(SNA_path)        
        # local_metric_df=local_metric_df[~local_metric_df["sna-abs-path"].isna()]
        # local_metric_df=local_metric_df[local_metric_df['sna-abs-path']!="EXTERNAL"].set_index("sna-abs-path")
        # print(local_metric_df[local_metric_df.index.duplicated()])
        ck_data=self.getCKMetric(version)
        ck_data=ck_data[~ck_data['class'].str.contains("\$")].set_index('file')
        print(ck_data[ck_data.index.duplicated()])
        res=ck_data.groupby('file').sum()
        print(res)
        # print(type(res))
        # local_metric_df[CK_METRICS]=ck_data[CK_METRICS]
        # org.apache.activemq.perf.Producer
if __name__ == '__main__':
    data_directory=r"/home/hickey/data/dataset_jira"
    language="java"
    project_name="activemq"
    versions= ['5.0.0', '5.1.0', '5.2.0', '5.3.0', '5.8.0']
    # project_name="camel"
    # versions=['1.4.0', '2.10.0', '2.11.0', '2.9.0']
    # project_name="derby"
    # versions=['10.2.1.6', '10.3.1.4', '10.5.1.1']
    # project_name="groovy"
    # versions=['1_5_7', '1_6_BETA_1', '1_6_BETA_2']
    # project_name="hive"
    # versions=['0.10.0', '0.12.0', '0.9.0']
    # project_name="hbase"
    # versions=['0.94.0', '0.95.0', '0.95.2']
    # project_name="jruby"
    # versions=['1.1', '1.4.0', '1.5.0', '1.7.0.preview1']
    # project_name="lucene"
    # versions=['2.3.0', '2.9.0', '3.0.0', '3.1.0']
    # project_name="wicket"
    # versions=['1.3.0-beta2', '1.3.0-incubating-beta-1', '1.5.3']
    datasetBuilder =DatasetBuilder(data_directory,project_name,language)
    # datasetBuilder.mergeMetrics(version,mergeCK=True,mergeBug=True,extractSNA=True,extractCK=True)
    # datasetBuilder.mergeMetrics(version,mergeCK=True,mergeBug=True,extractSNA=False,extractCK=False)
    datasetBuilder.auto_gen_trainset(versions,force=True)
    # datasetBuilder.test(version="5.1.0")

