#!/usr/bin/env python3
"""
    Class handles minor cases of data matrix manipulation and storage.

"""
import sys
import csv
sys.path.append('../../')
from FileManager.file_manager  import FileManager
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from typing import List

class WASFeatureExtractor:
    """
        Class capable of holding matrix structures and reorganizing columns.
        Results may be outputted as json files.
    """
    def __init__(self, name : str, outputDirectory : str, errLogDirectory : str, verbose=True) -> None:
        self.__name = name
        self.__outputDirectory = outputDirectory
        self.__file_manager = FileManager(name, errLogDirectory, verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
        self.__dataset = {}



    def add_dataset(self,id : str, data) -> None:
        self.__dataset[id] = data
    
    def remove_dataset(self, id : str) -> Non:
        if self.has(id):
            del self.__dataset[id]
        
    def has(self,id : str) -> bool:
        return id in self.__dataset
    
    def get(self, id : str):
        if self.has(id):
            return self.__dataset[id]
        
    def generate_dataset(self, ordering_list : List[int], data_id : str):
        """
            Function allows for reordering of dataset columns via a provided
            list of desired index order.
        """
        if not self.has(data_id):
            return None
        
        dataset = self.get(data_id)
    
        n_rows = len(dataset)
        
        dataframe = [ [0]*(len(ordering_list)) for n in range(n_rows) ]
        
        for c,idx in enumerate(ordering_list):
            
            for i in range(1,n_rows):
                dataframe[i][c] = dataset[i][idx]
            dataframe[0][c] = dataset[0][idx]
        
        return dataframe
            
    def to_file(self, tag : str) -> str:
        if self.has(tag):
            csv_file_path = '{}{}-{}.csv'.format(self.__outputDirectory, tag)
            with open(csv_file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.get(tag))
            return  csv_file_path
        
# Example

#data = [
#    ['Dog','Cat','Pig'],
#    ['Biscuit','Tuna','Slop'],
#    ['Fast','Faster','Slow']
#]

#WASFE = WASFeatureExtractor('test','./Testing/','./Testing/')
#WASFE.add_dataset('animals',data)
#d = WASFE.generate_dataframe([2,1,0],'animals')
#print(d)
