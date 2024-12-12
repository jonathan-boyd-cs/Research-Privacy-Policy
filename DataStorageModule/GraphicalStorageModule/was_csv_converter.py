#!/usr/bin/env python3
"""

    Class functions to convert WAS data, post cleaning pipeline, into a CSV file for analysis.
"""

import csv
import json
import sys
sys.path.append('../../')
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from FileManager.file_manager import FileManager
from DataStorageModule.PreprocessorStorageModule.data_key_manager import DataKeyManager
from typing import List

class WASToCSVConverter:
    """
        Specialized in converting WAS data, post clean, to CSV.
    """
    def __init__(self, name : str, WASF_file : str, columns : List[str], web_source_dict : dict, outputDirectory : str, errLogDirectory : str, verbose=True) -> None:
        self.__name = name 
        self.__columns = list(columns)
        self.__WASF_file = WASF_file
        self.__WASF = None
        self.__csv_data = []
        self.__web_sources = web_source_dict
        self.__outputDirectory = outputDirectory
        self.__verbose = verbose
        self.__file_manager = FileManager(self.__name, errLogDirectory)
        self.__file_manager.assure_directory(self.__outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
        m = time_stamped_msg(name)
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,name))
        self.__DKM = DataKeyManager(self.__name, outputDirectory, errLogDirectory, verbose)
        self.__DKM.encode_dictionary(self.__name,self.__web_sources)
        self.__level_keys = self.__DKM.get_levels(self.__name)
        self.__depth = len(list(self.__level_keys))
        self.__num_at_depth = 0
        
        reference = self.__DKM.get_level_keys(self.__name,self.__depth)
        # Determines number of terminal values in the tree.
        # assumes dataset is uniform in components per entry.
        # checking for point where the prior key trail changes, assuming thisis the point at which the terminal
        # values for the prior subject (end node)  have been fully traversed.
        while ((self.__num_at_depth < len(list(reference)))):
            if ((self.__num_at_depth == len(list(reference)) -1) and (reference[self.__num_at_depth][:-1] == reference[self.__num_at_depth-1][:-1])):
                self.__num_at_depth += 1
                continue
                
            if ((reference[self.__num_at_depth][:-1] == reference[self.__num_at_depth+1][:-1])):
                self.__num_at_depth += 1
            
        # Load WASF file
        with open(self.__WASF_file , 'r') as f:
            self.__WASF = json.load(f)
     
     
    def __value_extraction(self, container : List[any], reference : dict, key_trail : List[str], keys : List[str]) -> List[any]:
        """
            Method serves to retrieve dictionary value entries at a particular depth, reached via key trail.
        """
        while bool(key_trail):
            reference = reference[key_trail[0]]
            key_trail = key_trail[1:]
        for key in keys:
            if key in reference:
                container.append(reference[key])
            else:
                container.append('N/A')
    
    def get_columns(self) -> List[str]:
        return self.__columns
    
    
    def __dfs_header_helper(self, data : dict, container : List[str], depth : int=1):
        """
            Method traverses a heirarchical dictionary tree to a certain depth, extracting the utilized keys in the process.
            Produces a list to serve as the CSV header.
        """
        if depth == 0: return
        if type(data) != dict: return
        for key in data:
            container.append(key)
            self.__dfs_header_helper(data[key]['lower'],container, depth-1)
    
    
    
    def __dfs_value_helper(self, data, container, depth=1):
        """
            Traverse a dictionary tree to a specified depth, acquiring data on the way via each key encountered.
        """
        if depth == 0: return
        for key in data:
            container.append(data[key]['count'])
            self.__dfs_value_helper(data[key]['lower'],container,depth-1)
            
    
    def run(self, subj_idx : int, num_keyword_levels : int):
        """
            Implements the main functionality of the class. The subject index is the index of 
            website url's in the provided web source structure. The num keyword levels variable
            allows for the modulation of depth corresponding to the column legth and content. In other words,
            a higher keyword levels value would involve adding nodes at a lower heirarchical level to the CSV.
        """
        header = []
        test_key = list(self.__WASF.keys())[0]
        data__   = self.__WASF[test_key]
        # loading WASF
        # loading csv columns
        web_key = list(data__.keys())[0]
        
        for val in self.__columns:
            header.append(val)

        # gets the key trails at the bottom of the tree then...
        # takes a sample which consists of only enough to provide all trails to unique terminal values
        # keys is the key name for all of such terminal values
        keys = [
            x[-1] for x in list(self.__DKM.get_level_keys(self.__name, self.__depth))[:self.__num_at_depth]
        ]

        for k in keys:
            header.append(k)
        #statistics
        statistical = data__[web_key]['statistics']
        for key in statistical:
            header.append(key)
        # main suite
        self.__dfs_header_helper(data__[web_key]['primary'],header, num_keyword_levels)
        # accessory searches
        secondary = data__[web_key]['secondary']
        for key in secondary:
            header.append(key)      
        
        self.__columns = header
        self.__csv_data.append(header)
        
        for website in data__.keys():
            entry = self.__DKM.find( self.__name,website, subj_idx)
            
            row = list()
            for var in entry:
                row.append(var)
            

            
            self.__value_extraction(row, self.__web_sources, entry, keys)
        
            statistical = data__[web_key]['statistics']
            for key in statistical:
                row.append(statistical[key])
                
            web_key = entry[-1]
            reference = data__[web_key]['primary']
            self.__dfs_value_helper(reference,row, num_keyword_levels)

                
            secondary = data__[web_key]['secondary']
            for key in secondary:
                row.append(secondary[key])
                
            
            self.__csv_data.append(row)
        

    def to_file(self, tag):
        csv_file_path = '{}{}.csv'.format(self.__outputDirectory, tag)
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.__csv_data)
        return  csv_file_path


#from WebsiteGathering.Run1 import data
#WebData = data
#from PolicyQueryModule.privacy_policy_keywords import PRIVACY_POLICY_KEY_PHRASES
#output_file = '../../OutputFiles/WAS/Test/'
#log_file = '../../OutputFiles/WAS/Test/'
#name = 'tester'
#verbose = True
#file = '../../OutputFiles/WAS/CLEANING/Finalized-testing-testing-03_16AM-on-November-30.json'
#data = [
#    ['Industry', 'Country', 'State', 'Website']
#]

#    def __def__(self, name, WASF_file, columns, web_source_list, outputDirectory, errLogDirectory, verbose=True):

#WASCSVC = WASToCSVConverter(name, file, data, WebData, output_file, log_file, verbose)
#print(WASCSVC.get_columns(),"\n\n")
#WASCSVC.run(3,3)
#print(WASCSVC.get_columns())
#WASCSVC.to_file('testing3')
