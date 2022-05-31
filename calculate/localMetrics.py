# -*- coding: utf-8 -*-
import networkx as nx
from networkx.algorithms.traversal import depth_first_search as dfs
class LocalMetrics:
    
    def getDegree(self,ids):   #计算每个点的度
        degree=self.__G.degree(ids)
        return dict(degree)
    
    def getIn_degree(self,ids):   #计算每个点的入度
        indegree=self.__G.in_degree(ids)
        return dict(indegree)
    
    def getOut_degree(self,ids):     #计算每个点的出度
        outdegree=self.__G.out_degree(ids)
        return dict(outdegree)
            
    def getBetweenness(self,ids):    #计算介数
        betw=nx.betweenness_centrality(self.__G)    
        if(ids==None):
            return betw
        result={}
        for id in ids:
            result[id]=betw.get(id)
        return result 
    def getCloseness_vitality(self,ids):     #计算紧密度活性 
        close=nx.closeness_vitality(self.__G,weight=None)
        if(ids==None):
            return close
        result={}
        for id in ids:
            result[id]=close.get(id)
        return result 
        
    def getKatz_centrality(self,ids):    #计算K氏系数
#        katz=nx.katz_centrality(self.__G, alpha=0.1, beta=1.0, max_iter=1000, tol=1e-06, nstart=None, normalized=True,weight='weight')
#        katz=nx.katz_centrality(self.__G)
#        print('katz_centrality',katz)
        katz=nx.katz=nx.katz_centrality_numpy(self.__G)
#        print('katz_centrality_numpy',katz)
        if(ids==None):
            return katz
        result={}
        for id in ids:
            result[id]=katz.get(id)
        return result 
        
    def getPagerank(self,ids):     #计算pagerank
#        pagerank=nx.pagerank(self.__G, alpha=0.85, personalization=None, max_iter=100, tol=1e-06, nstart=None, weight='weight',dangling=None)
        pagerank=nx.pagerank(self.__G)
        if(ids==None):
            return pagerank
        result={}
        for id in ids:
            result[id]=pagerank.get(id)
        return result
    
    def getEigenvector_centrality(self,ids):     #计算特征向量中心性
        eigenvector_centrality=nx.eigenvector_centrality_numpy(self.__G, weight=None)
        if(ids==None):
            return eigenvector_centrality
        result={}
        for id in ids:
            result[id]=eigenvector_centrality.get(id)
        return result
    
    def getAverage_neighbor_degree(self,ids):
        average_neighbor_degree=nx.average_neighbor_degree(self.__G)
        if(ids==None):
            return average_neighbor_degree
        result={}
        for id in ids:
            result[id]=average_neighbor_degree.get(id)
        return result
        
    def getClustering_Coefficient(self,ids):
        W=self.__G.to_undirected()
        clustering=nx.clustering(W,ids)
        return clustering
    
    def getSquare_clustering(self,ids):
        W=self.__G.to_undirected()
        square_clustering=nx.square_clustering(W,ids)
        return square_clustering
    
    
    def getCloseness_centrality(self,ids):
        #W=self.__G.to_undirected()
        closeness_centrality=nx.closeness_centrality(self.__G)
        if(ids==None):
            return closeness_centrality
        result={}
        for id in ids:
            result[id]=closeness_centrality.get(id)
        return result
        
    def getDegree_centrality(self,ids):
        #W=self.__G.to_undirected()
        degree_centrality=nx.degree_centrality(self.__G)
        if(ids==None):
            return degree_centrality
        result={}
        for id in ids:
            result[id]=degree_centrality.get(id)
        return result
    
    def getOut_degree_centrality(self,ids):
        #W=self.__G.to_undirected()
        out_degree_centrality=nx.out_degree_centrality(self.__G)
        if(ids==None):
            return out_degree_centrality
        result={}
        for id in ids:
            result[id]=out_degree_centrality.get(id)
        return result
    
    def getIn_degree_centrality(self,ids):
        #W=self.__G.to_undirected()
        in_degree_centrality=nx.in_degree_centrality(self.__G)
        if(ids==None):
            return in_degree_centrality
        result={}
        for id in ids:
            result[id]=in_degree_centrality.get(id)
        return result
        
    def getBetweenness_centrality(self,ids):
        #W=self.__G.to_undirected()
        betweenness_centrality=nx.betweenness_centrality(self.__G)
        if(ids==None):
            return betweenness_centrality
        result={}
        for id in ids:
            result[id]=betweenness_centrality.get(id)
        return result
    
    def getCommunicability(self,ids):
        W=self.__G.to_undirected()
        communicability=nx.communicability(W)
        if(ids==None):
            return communicability
        result={}
        for id in ids:
            result[id]=communicability.get(id)
        return result
        
    def getCommunicability_exp(self,ids):
        W=self.__G.to_undirected()
        communicability_exp=nx.communicability_exp(W)
        if(ids==None):
            return communicability_exp
        result={}
        for id in ids:
            result[id]=communicability_exp.get(id)
        return result
    
    
    def getLoad_centrality(self,ids):
        #W=self.__G.to_undirected()
        load_centrality=nx.load_centrality(self.__G)
        if(ids==None):
            return load_centrality
        result={}
        for id in ids:
            result[id]=load_centrality.get(id)
        return result
        
    def getNumber_of_cliques(self,ids):
        W=self.__G.to_undirected()
        number_of_cliques=nx.number_of_cliques(W)
        if(ids==None):
            return number_of_cliques
        result={}
        for id in ids:
            result[id]=number_of_cliques.get(id)
        return result
        
    def getCore_number(self,ids):
        G=self.__G.copy()
        G.remove_edges_from(nx.selfloop_edges(G))
        core_number=nx.core_number(G)
        if(ids==None):
            return core_number
        result={}
        for id in ids:
            result[id]=core_number.get(id)
        return result
    
    def getNumber_ancestors(self,ids):
        dictnumber={}
        nodes=nx.nodes(self.__G)
        for v in nodes:
            number_ancestors=nx.ancestors(self.__G,v)
            dictnumber[v]=len(number_ancestors)
        if(ids==None):
            return dictnumber
        result={}
        for id in ids:
            result[id]=dictnumber.get(id)
        return result
        
    def getNumber_descendants(self,ids):
        dictnumber={}
        nodes=nx.nodes(self.__G)
        for v in nodes:
            number_ancestors=nx.descendants(self.__G,v)
            dictnumber[v]=len(number_ancestors)
        if(ids==None):
            return dictnumber
        result={}
        for id in ids:
            result[id]=dictnumber.get(id)
        return result
        
    def getEccentricity(self,ids):
        dictnumber={}
        nodes=nx.nodes(self.__G)
        for v in nodes:
            eccentricity=nx.single_source_shortest_path_length(self.__G,v)
            dictnumber[v]=len(eccentricity)
        if(ids==None):
            return dictnumber
        result={}
        for id in ids:
            result[id]=dictnumber.get(id)
        return result
    
    def getRipple_Degree(self,ids):#波及度
        rds={}
        nodes=nx.nodes(self.__G)
        for v in nodes:
            poster=list(dfs.dfs_postorder_nodes(self.__G,v))
            rds[v]=len(poster)
        if(ids==None):
            return rds
        result={}
        for id in ids:
            result[id]=rds.get(id)
        return result
    def getMinimax_Criterion(self,ids):   #最小最大准则
        G=self.__G
        H=G.to_undirected()
        length_list=[]                   #创建空列表用于存放点的距离长度
        max_list=[]                      #存放所有点的可连接点的最大距离
        max_dic={}                       #以点为key，以最大距离为value
        for node in H:                         #对于H图里的所有点迭代
            path_length=nx.single_source_dijkstra_path_length(H, node,weight=None)   #点node对能连接到的所有点的路径长度
            for i in path_length.values():
                length_list.append(i)
            max_len=max(length_list) 
            max_list.append(max_len)
            max_dic[node]=max_len
            #print node,1/float(max_len)
        Minimax=min(max_list)
        result={}
        for node in H:
            if max_dic[node]==Minimax:
                result[node]=max_dic[node]
#                print 'the minimaxcriterion of' ,node,'is' ,max_dic[node]       
                #print Minimax 
        return result      
    #计算内部调用边数
    def getInnerEdge_Count(self,ids):
        nodes=self.__G.nodes()
        inners={}
        for key in nodes:
            
            node=nodes[key]
            innerEdgeCount=0
            if('innerEdgeCount' in node):
                innerEdgeCount=node['innerEdgeCount']
                inners[key]=int(innerEdgeCount)
            else:
                inners[key]=0
        if(ids==None):
            return inners
        result={}
        for id in ids:
            result[id]=inners[id]
        return result
    
     #计算内部变量调用边数
    def getInnerVariable_Edge_Count(self,ids):
        nodes=self.__G.nodes()
        inners={}
        for key in nodes:
            
            node=nodes[key]
            innerEdgeCount=0
            if('innerVariableEdgeCount' in node):
                innerEdgeCount=node['innerVariableEdgeCount']
                inners[key]=int(innerEdgeCount)
            else:
                inners[key]=0
        if(ids==None):
            return inners
        result={}
        for id in ids:
            result[id]=inners[id]
        return result   
    
     #计算公共节点数
    def getPublic_Function_Count(self,ids):
        nodes=self.__G.nodes()
        inners={}
        for key in nodes:
            
            node=nodes[key]
            innerEdgeCount=0
            if('publicNodeCount' in node):
                innerEdgeCount=node['publicNodeCount']
                inners[key]=int(innerEdgeCount)
            else:
                inners[key]=0
        if(ids==None):
            return inners
        result={}
        for id in ids:
            result[id]=inners[id]
        return result  
    
         #计算私有节点数
    def getPrivate_Function_Count(self,ids):
        nodes=self.__G.nodes()
        inners={}
        for key in nodes:
            
            node=nodes[key]
            innerEdgeCount=0
            if('privateNodeCount' in node):
                innerEdgeCount=node['privateNodeCount']
                inners[key]=int(innerEdgeCount)
            else:
                inners[key]=0
        if(ids==None):
            return inners
        result={}
        for id in ids:
            result[id]=inners[id]
        return result  
    
             #计算共有变量数
    def getPublic_Variable_Count(self,ids):
        nodes=self.__G.nodes()
        inners={}
        for key in nodes:
            
            node=nodes[key]
            innerEdgeCount=0
            if('publicVariable' in node):
                innerEdgeCount=node['publicVariable']
                inners[key]=int(innerEdgeCount)
            else:
                inners[key]=0
        if(ids==None):
            return inners
        result={}
        for id in ids:
            result[id]=inners[id]
        return result 
    
                 #计算私有变量数
    def getPrivate_Variable_Count(self,ids):
        nodes=self.__G.nodes()
        inners={}
        for key in nodes:
            
            node=nodes[key]
            innerEdgeCount=0
            if('privateVariable' in node):
                innerEdgeCount=node['privateVariable']
                inners[key]=int(innerEdgeCount)
            else:
                inners[key]=0
        if(ids==None):
            return inners
        result={}
        for id in ids:
            result[id]=inners[id]
        return result 
    
    #计算调出边数，这里是类中函数调类外部函数的出边，不是节点的出度
    def getOut_Edge_Count(self,ids):
        nodes=self.__G.nodes()
        inners={}
        for key in nodes:
            
            node=nodes[key]
            innerEdgeCount=0
            if('outEdgeCount' in node):
                innerEdgeCount=node['outEdgeCount']
                inners[key]=int(innerEdgeCount)
            else:
                inners[key]=0
        if(ids==None):
            return inners
        result={}
        for id in ids:
            result[id]=inners[id]
        return result 
    
        #计算调出边数，这里是类中函数调类被外部函数的调用的入边，不是节点的入度
    def getIn_Edge_Count(self,ids):
        nodes=self.__G.nodes()
        inners={}
        for key in nodes:
            
            node=nodes[key]
            innerEdgeCount=0
            if('inEdgeCount' in node):
                innerEdgeCount=node['inEdgeCount']
                inners[key]=int(innerEdgeCount)
            else:
                inners[key]=0
        if(ids==None):
            return inners
        result={}
        for id in ids:
            result[id]=inners[id]
        return result 
        #计算调用外部变量的边
        
    def getOut_Variable_Edge_Count(self,ids):
        nodes=self.__G.nodes()
        inners={}
        for key in nodes:
            
            node=nodes[key]
            innerEdgeCount=0
            if('outVariableEdgeCount' in node):
                innerEdgeCount=node['outVariableEdgeCount']
                inners[key]=int(innerEdgeCount)
            else:
                inners[key]=0
        if(ids==None):
            return inners
        result={}
        for id in ids:
            result[id]=inners[id]
        return result 
    
    #计算内部变量被调用的边
    def getIn_Variable_Edge_Count(self,ids):
        nodes=self.__G.nodes()
        inners={}
        for key in nodes:
            
            node=nodes[key]
            innerEdgeCount=0
            if('inVariableEdgeCount' in node):
                innerEdgeCount=node['inVariableEdgeCount']
                inners[key]=int(innerEdgeCount)
            else:
                inners[key]=0
        if(ids==None):
            return inners
        result={}
        for id in ids:
            result[id]=inners[id]
        return result

    #计算内部变量被内部调用的边
    def getInner_Variable_Edge_Count(self,ids):
        nodes=self.__G.nodes()
        inners={}
        for key in nodes:
            
            node=nodes[key]
            innerEdgeCount=0
            if('innerVariableEdgeCount' in node):
                innerEdgeCount=node['innerVariableEdgeCount']
                inners[key]=int(innerEdgeCount)
            else:
                inners[key]=0
        if(ids==None):
            return inners
        result={}
        for id in ids:
            result[id]=inners[id]
        return result 
        #计算调用最多的两个节点组
    def getLinkcount_Between_Nodes(self,ids):
        edges=self.__G.edges()
        inners={}
        for key in edges:
            edge=edges[key]
            linkedCount=0
            if('linkCount' in edge):
                linkedCount=edge['linkCount']
                inners[key]=int(linkedCount)
            else:
                inners[key]=0
        if(ids==None):
            return inners
        result={}
        for id in ids:
            result[id]=inners[id]
        return result 

#6.强度	
    def getStrength(self,ids):
        nodes=self.__G.nodes()
        edges=self.__G.edges()
        strength={}
        for n in nodes:
            Strength = 0
            inStrength = 0
            outStrength = 0

            for s,t,edge in edges.data():
                source=s
                target=t
                if(n==source):
                    outStrength+=int(edge['linkCount'])
                if(n==target):
                    inStrength+=int(edge['linkCount'])
                Strength=inStrength+outStrength
            #print ('the strength of' ,n,'is' ,strength)
            strength[n]=Strength
        if(ids==None):
            return strength
        result={}
        for id in ids:
            result[id]=strength[id]
        return result  
#8.模块内部耦合 
    def getModule_InnerCouping(self,ids):
        nodes=self.__G.nodes()
        module_innercouping={}
        for n,node in nodes.data():
            publicNodeCount=0
            privateNodeCount=0
            innerEdgeCount=0
            if('publicNodeCount' in node):
               publicNodeCount= node['publicNodeCount']
            if('privateNodeCount' in node):
               privateNodeCount= node['privateNodeCount']
            fc=float(publicNodeCount+privateNodeCount)
            if('innerEdgeCount' in node):
               innerEdgeCount= node['innerEdgeCount']
            innerEdge=float(innerEdgeCount)
            if (fc==0):
                module_innercouping[n]=0
            else:
                module_innercouping[n]=innerEdge/fc
        if(ids==None):
            return module_innercouping
        result={}
        for id in ids:
            result[id]=module_innercouping[id]
        return result   
#4.逆向波及度
    def getReverse_Ripple(self,ids):
        reverse_ripple={}
        nodes=self.__G.nodes()
        for n in nodes:
            key = n
            dir_bfs=len(list(nx.bfs_edges(self.__G, n, reverse=True)))
            T=dir_bfs+1
            reverse_ripple[key]=T
        if(ids==None):
            return reverse_ripple
        result={}
        for id in ids:
            result[id]=reverse_ripple[id]
        return result   
    #7.模块规模	
    def getFuncount(self,ids):
        nodes=self.__G.nodes()
        funcount={}
        for n,node in nodes.data():
            publicNodeCount=0
            privateNodeCount=0
            if('publicNodeCount' in node):
               publicNodeCount= int(node['publicNodeCount'])
            if('privateNodeCount' in node):
               privateNodeCount=int( node['privateNodeCount'])
            funcount[n]=int(publicNodeCount+privateNodeCount)
        if(ids==None):
            return funcount
        result={}
        for id in ids:
            result[id]=funcount[id]
        return result                                                                            				         
###############################################################    
    def calMetrics(self,metric,ids=None):
        metrics=metric.split(',')
        result={}
        for m in metrics:
            r=self.calMetric(m,ids)
            if(r):
                result[m]=r
        return result
    def calMetric(self,metric,ids=None,seq=True):
        result={}
        if (metric in self.__function):
            try:
                result=self.__function[metric](ids)
            except:
                print(metric,'is wrong')
                return None
        else:
            return  None
        return result
    def getTopRankedMetrics(self,metric,top=10,seq=True):
        r=self.calMetric(metric,None,seq)
        result=[]
        length=len(r)
        if(top<length):
            for i in range(top):
                result.append(r[i])
        else:
            result=r
        return result
    def allfunc(self):
        keys=self.__function.keys()
        return keys

    def __init__(self,G):
        self.__G=G
        self.__function={
        'degree':self.getDegree,
        'in_degree':self.getIn_degree,
        'out_degree':self.getOut_degree,
        'betweenness':self.getBetweenness,
        'closeness_vitality':self.getCloseness_vitality,
        'katz_centrality':self.getKatz_centrality,
        'pagerank':self.getPagerank,
        'eigenvector_centrality':self.getEigenvector_centrality,
        'average_neighbor_degree':self.getAverage_neighbor_degree,
        'clustering_coefficient':self.getClustering_Coefficient,
        'square_clustering':self.getSquare_clustering,
        'closeness_centrality':self.getCloseness_centrality,
        'degree_centrality':self.getDegree_centrality,
        'out_degree_centrality':self.getOut_degree_centrality,
        'in_degree_centrality':self.getIn_degree_centrality,
        'betweenness_centrality':self.getBetweenness_centrality,
        'communicability':self.getCommunicability,
        'communicability_exp':self.getCommunicability_exp,
        'load_centrality':self.getLoad_centrality,
        'number_of_cliques':self.getNumber_of_cliques,
        'core_number':self.getCore_number,
        'number_ancestors':self.getNumber_ancestors,
        'number_descendants':self.getNumber_descendants,
        'eccentricity':self.getEccentricity,  
        'minimax_criterion':self.getMinimax_Criterion,  
        'ripple_degree':self.getRipple_Degree,
        'inneredge_count':self.getInnerEdge_Count,
        'innervariable_edge_count':self.getInnerVariable_Edge_Count,
        'public_function_count':self.getPublic_Function_Count,
        'private_function_count':self.getPrivate_Function_Count,
        'public_variable_count':self.getPublic_Variable_Count,
        'private_variable_count':self.getPrivate_Variable_Count,
        'out_edge_count':self.getOut_Edge_Count,
        'in_edge_count':self.getIn_Edge_Count,
        'out_variable_edge_count':self.getOut_Variable_Edge_Count,
        'in_variable_edge_count':self.getIn_Variable_Edge_Count,
        'inner_variable_edge_count':self.getInner_Variable_Edge_Count,
        'linkcount_between_nodes':self.getLinkcount_Between_Nodes,
        'strength':self.getStrength,
        'module_inner_couping':self.getModule_InnerCouping,
        'reverse_ripple':self.getReverse_Ripple,
        'funcount':self.getFuncount
        }



