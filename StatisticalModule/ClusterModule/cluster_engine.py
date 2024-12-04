import sys
sys.path.append('../../')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits import mplot3d
import pandas as pd
from sklearn.cluster import KMeans
from ErrorHandleModule.general import time_stamped_msg
from FileManager.file_manager import FileManager
from DataStorageModule.GraphicalStorageModule.pfd_creator import PDFGenerator


class ClusterCreator(PDFGenerator):
    def __init__(self, outputDirectory, sizeScale = 1):
        super().__init__(outputDirectory)
        self.__sizeScale = sizeScale
    
    def set_size_scale(self, multiplier):
        self.__sizeScale = multiplier
    
    def wcss_elbow_cluster(self, K_limit, dataset,title):
        plt.clf()       
        within_cluster_sum_sqr = []
        for k_clusters in range(1, K_limit+1):
            kmeans = KMeans(
                n_clusters=k_clusters,
                init='k-means++'
                )
            kmeans.fit(dataset)
            sum_squares = kmeans.inertia_  
            within_cluster_sum_sqr.append(sum_squares)  

        plt.plot(range(1,K_limit+1), within_cluster_sum_sqr)
        plt.title(title)
        plt.xlabel("Number of clusters")
        plt.ylabel("WCSS")
        self.save_pdf('elbow',title)
        
        return within_cluster_sum_sqr
     
    def cluster_model(self, K, dataset, title, xlabel, ylabel=None):
        kmeans = KMeans(n_clusters=K,
                        init='k-means++')
        y_kmeans = kmeans.fit_predict(dataset)

        colors = cm.rainbow(np.linspace(0,1,K+1))
        plt.clf()
        fig = plt.figure()
        plt.title = title
        
        for i in range(K):
            x = dataset[y_kmeans==i,0]
            y = dataset[y_kmeans==i,1]
            ax = plt.axes()
            ax.scatter(x,
                        y,
                        marker='s',  s=20*self.__sizeScale,
                        c=colors[i])
                
            ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
                        s=20,color = colors[K], label="Centroids" )
            
            ax.set_xlabel(xlabel, fontsize=15)
            ax.set_ylabel(ylabel, fontsize=15)
            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)


            plt.legend()
            
            self.save_pdf('cluster-model',title)
            
        return y_kmeans
                
        


class ClusterEngine(ClusterCreator):
    def __init__(self, outputDirectory, errLogDirectory, dataset, c1,c2):
        super().__init__(outputDirectory)
        self.__file_manaer = FileManager('fm',errLogDirectory)
        self.__file_manaer.assure_directory(outputDirectory)
        self.__file_manaer.assure_directory(errLogDirectory)
        self.__dataset = dataset
        self.__X = None
        self.__assign(c1,c2)
        
    
    
    def __assign(self,c1,c2):
        self.__X = self.__dataset.iloc[:,c1].copy().values
        self.__X = self.__dataset.iloc[:,[c1,c2]].copy().values
         
    def set_dataset(self,dataset, col1, col2):
        self.__dataset = dataset
        self.__assign(col1, col2)
            
    def set_columns(self, c1,c2):
        self.__assign(c1,c2)

    def elbow(self, K_limit, title):
        return self.wcss_elbow_cluster(K_limit, self.__X, title)
            
    def cluster_model(self, K, title, xlabel, ylabel=None):
        return super().cluster_model(K,self.__X,title, xlabel,ylabel)



# Example
# import sys
# sys.path.append('../../')
# from DataStorageModule.GraphicalStorageModule.dataframe_store import CSVToDataFrameStore
# name = 'testing'
# out = './Testing/'
# log = './Testing/Log/'
# CSVTDS = CSVToDataFrameStore(name, out, log)
#csv1 = '../../testing.csv'
#csv2 = '../../testing2.csv'
#csv3 = '../../testing3.csv'
#CSVTDS.load_and_store('t1',csv1)
#CSVTDS.load_and_store('t2',csv2)
#CSVTDS.load_and_store('t3',csv3)
#data = CSVTDS.to_pandas('t3')
#print(data)
#CE = ClusterEngine(out,log,data, 4,5)
#testing = CE.elbow(3,'test-elbow1')
#print(testing)
#testing2 = CE.cluster_model(1,'testing model','traffic count','traffic value')
