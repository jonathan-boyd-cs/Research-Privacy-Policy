#!/usr/bin/env python3

"""
    Class serves as the second component in the WAS data cleaning pipeline.
    This class functions by taking the cleaned WAS successful data from the WASDC
    and combining text results per key phrase/word into a singular structure each,
    for processing later in the pipeline.

"""

import json
import sys
sys.path.append('../../')
from DataStorageModule.DataCleanerModule.cleaner_database import CleanerDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from FileManager.file_manager import FileManager
import copy


class WASDataMerger:
    def __init__(self, name : str, outputDirectory : str,errLogDirectory : str, verbose=True) -> str:
        self.__name = name
        self.__verbose = verbose
        self.__database = CleanerDatabase()
        self.__outputDirectory = outputDirectory
        m = time_stamped_msg("{}-WASDataMerger")
        file = "{}{}.txt".format(errLogDirectory, m)
        self.__err_database = ErrorDatabase(file)
        self.__file_manager = FileManager(self.__name,verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)

    def get(self, tag : str):
        return self.__database.get(tag)

    # cleaned_WAS_successful_dataset (cWASsd)
    def merge(self, cWASsd_file :str , tag : str) -> str:
        cWASsd = None
        
        try:
            with open(cWASsd_file,'r') as f:
                cWASsd = json.load(f)
            
            cWASsd = cWASsd[list(cWASsd.keys())[0]]
        except Exception as e:
            m = "(WASDataMerger) unexpected error while loading cQaAD file...({})...\nerror --> {}".format(str(cWASsd_file),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise(e)
        
        
        try:
            cleaned_data = {}
            for website in cWASsd:
                maybe_print(self.__verbose,
                                "(WASDataMerger) merging text result for {}...".format(
                                    website
                                ))
                # handling tricky format of cWASsd data...
                keys = list(cWASsd[website]['pages'].keys())
                handle = cWASsd[website]['pages'][keys[0]]
                
                merged_dataset = copy.deepcopy(handle)
                
                for key in keys[1:]:
                    maybe_print(self.__verbose,
                                "(WASDataMerger) merging required for page 0 to page {}...".format(
                                    key
                                ))
                    self.____merger(
                            base        = merged_dataset, 
                            addition    = cWASsd[website]['pages'][key])
                
                cleaned_data[website] = {}
                cleaned_data[website]['primary'] = {}
                cleaned_data[website]['secondary'] = {}
                cleaned_data[website]['primary'] = merged_dataset
                
                for k in cWASsd[website].keys():
                    if k != 'pages':
                        # capture secondary data...
                        cleaned_data[website]['secondary'][k] = cWASsd[website][k]
            self.__database.add(tag,cleaned_data)
        
        except KeyboardInterrupt:
            sys.exit()
        
        except Exception as e:
            m = "(WASDataMerger) merging failure...({})...\nerror --> {}".format(str(cWASsd_file),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise (e)
        # produce and return json file
        try:
            m = time_stamped_msg(tag)
            out = "{}{}-merge.json".format(self.__outputDirectory, m)
            self.__database.add(tag,cleaned_data)
            self.__database.to_json(out)
            return out
        except Exception as e:
            m = "(WASDataMerger) unexpected error while storing merge results...({})...\nerror --> {}".format(str(cWASsd_file),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)    
            raise(e)

    def __merger(self, base : dict, addition : dict):
        for key in base.keys():
            
            maybe_print(self.__verbose,
                            "(WASDataMerger) operation at top level: ({})...".format(
                                key
                            ))
            # seek merge location...
            self.__dfs_helper( 
                current   = base[key],
                previous  = base, 
                key       = key, 
                data_curr = addition[key],
                data_prev = addition) 
            
            maybe_print(self.__verbose,
                            "(WASDataMerger) operation at top level: ({}) finished...".format(
                                key
                            ))
            
    def __dfs_helper(self, current : dict, previous : dict, key : str, data_curr : dict, data_prev : dict) -> None:
        """
            Serves as a diver that seeks to merge lists at the edge of a tree structure as produced by the WASDC
        """
        if type(current) != dict:
            if data_prev[key] != []:
                maybe_print(self.__verbose,
                                "(WASDataMerger) conducting merge at({})...".format(
                                    key
                                ))
                previous[key] = (current) + ((data_prev[key]))
            return
        else:
            for key in current.keys():
                self.__dfs_helper(current[key],current, key, data_curr[key], data_curr) 

#Example
#WASDM = WASDataMerger('wasdm','../../OutputFiles/WAS/CLEANING/',"../../OutputFiles/Errors/WAS/") 
#WASDM.merge("../../OutputFiles/WAS/CLEANING/tester-WASDC-04_42PM-on-November-30.json",
#            'testing')  
