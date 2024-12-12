#!/usr/bin/env python3
"""
    Class makes up the database structure dedicated to storing statistical data for text
    in the WAS program.
"""

import json
import sys
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
sys.path.append('../../')
from FileManager.file_manager import FileManager
from StatisticalModule.TextAnalysisModule.text_analysis_report import TextAnalysisReport

class TextAnalysisDatabase:
    """
        Structure for generating and holding statistical text data provided by the WAS program pipeline.
    """
    def __init__(self, name : str,errLogDirectory :str , verbose=True) -> None:
        self.__database = {}
        self.__count = 0
        self.__name = name
        self.__verbose = verbose
        m = time_stamped_msg("text-analysis-database-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))
        self.__file_manager = FileManager(name,verbose)
        self.__errLogDirectory = errLogDirectory
        self.__file_manager.assure_directory(errLogDirectory)


    def add(self, id :str, text :str ) -> None:
        """
            Add/produce a TextAnalysisReport for the provided text under the alias of [id]
        """
        try:
            if not self.has(id):
                self.__database[id] = {}
            self.__database[id][text] = TextAnalysisReport(self.__count,text, self.__errLogDirectory)
            self.__count += 1
        except Exception as e:
            m = "(TextAnalysisDatabase) unexpected error while processing a text addition...({})...\nerror --> {}".format(str(id),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)
    
    def remove(self, id : str ,  text :str) -> None:
        if self.has(id):
            del self.__database[id]
            self.__count -= 1
       
    def has(self,id : str) -> bool:
        return id in self.__database
            
    def get_name(self):
        return self.__name
    
    def get_data(self, id : str) -> dict:
        """
            retrieve all data for a given id
        """
        if self.has(id):
            data = {}
            for text in self.__database[id]:
                data[text] = self.get_data_for(id,text)

            return data
    
    def get_data_for(self,id : str, text : str) -> dict:
        """
            retrieve all of a particular text for a given id
        """
        if self.has(id):
            if text in self.__database[id]:
                return self.__database[id][text].get_all()
    
    def get_keys(self):
        return self.__database.keys()
        
    def get_count(self) -> int:
        """
        returns number of unique IDs in the database
        """
        return self.__count
    
    def summary(self) -> None:
        for subject in self.__database.keys():
            d = self.__database[subject]
            for text in d.keys():
                print(d[text])
                
    def to_json(self, filename : str) -> None:
        try:
            self.__file_manager.assure_directory(filename)
            data = {}
            for id in self.__database:
                data[id] = self.get_data(id)
            
            with open(filename,'w') as f:
                json.dump(data,f)

        except Exception as e:
            m = "(TextAnalysisDatabase) unexpected error formatting json...({})...\nerror --> {}".format(str(filename),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)