# -*- coding: utf-8 -*-
from calculate.localMetrics import LocalMetrics
import pandas as pd
class GraphCalculator:
    def __init__(self,classGraph,metrics):
        self._classGraph = classGraph
        self.__metrics=[]
        self.__metrics=metrics
    def getDataDF(self):
        nodeData=[]
        G=self._classGraph
        nodes=G.nodes()
        for i in nodes:
            # if(nodes[i]['bug']=='Yes'):
            #     nd=(i,1)
            #     nodeData.append(nd)#got falut nodes list
            # else:
            #     nd=(i,0)
            #     nodeData.append(nd)
            nd=(i,0)
            nodeData.append(nd)
        results=self.__calMetrics(nodeData,G)
        data_dict=results['values']
        dataDF=self.__result2df(data_dict,results['goodMetrics'])
        return dataDF

    #此函数的功能是具体计算网络文件中点的不同参数值
    def __calMetrics(self,data,G):
        results={}
        result=[]
        nodeIDs=[]
        bugs=[]
        for d in data:
            nodeID=d[0]
            bug=d[1]
            nodeIDs.append(nodeID)
            bugs.append(bug)
        mlMetric=LocalMetrics(G)
        nodeValues=[]
        badMetrics={}
        goodMetrics=[]
        for m in self.__metrics:
            value=mlMetric.calMetric(m,nodeIDs)
            if(value):
                nodeValues.append(value)
                goodMetrics.append(m)
            else:
                badMetrics[m]=m
#        print(self.__metrics)
        for i in range(0,len(nodeIDs)):
#        for nodeID in nodeIDs:
            nodeID=nodeIDs[i]
            bug=bugs[i]
            nodeMetrics=[]
            bug=bug
            for m in range(0,len(goodMetrics)):
                nodeMetrics.append(nodeValues[m][nodeID])
            nodeData=(nodeID,nodeMetrics,bug)
            result.append(nodeData)
        results['badMetrics']=badMetrics
        results['goodMetrics']=goodMetrics
        results['values']=result
        return results 

    def __result2df(self,dataset,metricList):
        columns=metricList
        columns.append('bug')
        index=[]
        matrix=[]
        for nodeData in dataset:
            value = nodeData[1]
            value.append(nodeData[2])
            index.append(nodeData[0])
            matrix.append(value)
        datasetDF=pd.DataFrame(columns=columns,index=index,data=matrix)
        return datasetDF



