#!/usr/bin/env python3
"""
    Class is used to store and manipulate csv file datasets.
    The class is capable of generating variations on matrices/dataframes
    and returning pandas dataframes when requested.
"""

import sys
sys.path.append('../../')
import json
import csv
import pandas as pd
import numpy as np
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from FileManager.file_manager import FileManager
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from DataStorageModule.GraphicalStorageModule.feature_extractor import WASFeatureExtractor

class CSVToDataFrameStore:
    def __init__(self, name : str, outputDirectory : str, errLogDirectory : str, verbose=True) -> None:
        self.__database = {}
        self.__name = name
        self.__file_manager = FileManager(name, errLogDirectory)
        self.__outputDirectory = outputDirectory
        self.__verbose = verbose 
        m = "{}{}.txt".format(errLogDirectory,name)
        self.__err_database = ErrorDatabase(m)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
        self.__feature_extractor = WASFeatureExtractor(name,outputDirectory, errLogDirectory)
       
    def set_output_directory(self, directory : str) -> None:
        """
            Modify the location in which results will be written.
        """
        self.__file_manager.assure_directory(directory)
        self.__outputDirectory = directory
        
    def has(self, tag : str) -> None:
        return tag in self.__database
    
    def get(self, tag : str) -> None:
        if self.has(tag):
            return self.__database[tag]  
    
    def generate_variation(self, tag : str, out_name : str, column_order=[], row_exclusion=[], exceptions : dict =None) -> object:
        """
            Utilized to generate variations on data matrices.
            The column_order parameter variates and constricts the columns of the data set.
            columns excluded from the list will not be generated. The row_exclusion parameter specifies
            rows to leave out of the result.
            
            The expections dictionary expects column indices as keys and desired omissions (List[values]) on the associated row plane as the value.
            for example [
                            [ cats , dogs, gorillas ],
                            [whales, fish, torpedos]                
                       ]   execeptions = {
                                0: ['gorillas']   <- "I do not want the value 'gorilla' in my set at row 0"
                           
                       }
        """
        if not self.has(tag):
            return None

        var = self.get(tag)
        if exceptions != None:
            for index in exceptions:
                var = [ x for x in var if str(x[index]).strip() not in exceptions[index]]
        
        #Cache the update before dataset generation
        tag_temp = time_stamped_msg("{}".format(tag))
        self.__feature_extractor.add_dataset(tag_temp,var)
        #Process potential column adaptations
        var = self.__feature_extractor.generate_dataset(column_order,tag_temp)
        #Exclude rows as needed
        var = [x for i,x in enumerate(var) if i not in row_exclusion]
        #Cache and return update
        self,__feature_extractor.remove_dataset(tag_temp)
        self.__database[out_name] = var
        self.__feature_extractor.add_dataset(out_name,var)
        return var
        
    def load_and_store(self, tag : str, csv_file : str) -> None:
        """
            Load a csv_file to data matrix and store it in the database under the alias of
            tag.
        """
        try:
            with open(csv_file, 'r') as f:
                reader = csv.reader(f)
                data = list(reader)
            self.__feature_extractor.add_dataset(tag,data)
            self.__database[tag] = data
        except Exception as e:
            m = "(CSVToDataFrameStore) unexpected error in loading and storing csv file...({})\nerror --> {}".format(tag,str(e))
            self.__err_database.add(tag,m)
            maybe_print(self.__verbose, m)
            raise (e)
     
    def store(self, tag : str, dataset : object) -> None:
        self.__database[tag] = dataset
        self.__feature_extractor.add_dataset(tag,dataset)
         
    def to_csv(self, tag : str) -> str:
        """
            export the dataset stored under the tag to
            csv file in the set output directory
        """
        if not self.has(tag):
            return None
        
        data = self.__database[tag]
        csv_file_path = '{}{}.csv'.format(self.__outputDirectory, tag)
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        return  csv_file_path
            
    def to_pandas(self, tag : str) -> object:
        try:
            if tag in self.__database:
                data = self.__database[tag]
                cols = data[0]

                #data = data[1:]
                array = np.array(data[1:])
                dataframe = pd.DataFrame(array, columns=cols)
                return dataframe
        except Exception as e:
            m = "(CSVToDataFrameStore) unexpected error in panda creation...({})\nerror --> {}".format(tag,str(e))
            self.__err_database.add(tag,m)
            maybe_print(self.__verbose, m)
            raise (e)
            
    def to_json(self, tag):
        try:
            if self.has(tag):
                data = self.get(tag)
                d = {tag:data}
                m = time_stamped_msg("{}-{}".format(tag,self.__name))
                file = "{}{}.json".format(self.__outputDirectory,m)
                with open(file,'w') as f:
                    json.dump(d,file)
        except Exception as e:
            m = "(CSVToDataFrameStore) unexpected error in formatting json...({})\nerror --> {}".format(tag,str(e))
            self.__err_database.add(tag,m)
            maybe_print(self.__verbose, m)
            raise (e)
        
                
    def dump(self):
        try:
            m = time_stamped_msg('dumping-{}'.format(self.__name))
            file = '{}{}.json'.format(self.__outputDirectory,m)
            with open(file, 'w') as f :
                json.dump(self.__database,f)
        except Exception as e:
            m = "(CSVToDataFrameStore) unexpected error in dumping database..\nerror --> {}".format(str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise (e)
            
        
# Example
#name = 'testing'
#out = './Testing/'
#log = './Testing/Log/'
#CSVTDS = CSVToDataFrameStore(name, out, log)
#csv1 = '../../testing.csv'
#csv2 = '../../testing2.csv'
#csv3 = '../../testing3.csv'
#CSVTDS.load_and_store('t1',csv1)
#CSVTDS.load_and_store('t2',csv2)
#CSVTDS.load_and_store('t3',csv3)
#CSVTDS.dump()
#d = CSVTDS.get('t3')
#s = CSVTDS.generate_variation('t3',[1,0,2],'t3-var')
#print(d)
#print(s)

#data1 = CSVTDS.to_pandas('t3')
#data2 = CSVTDS.to_pandas('t3-var')
#print(data1)
#print('\n\n')
#print(data2)
