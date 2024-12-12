#!/usr/bin/env python3

"""

    Wraps the DataKeyManager implementation so as to specify the functionality of managing
    dictionary encodings.
"""

import sys
sys.path.append('../../')
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from FileManager.file_manager import FileManager
from DataStorageModule.PreprocessorStorageModule.data_key_manager import DataKeyManager
from DataStorageModule.PreprocessorStorageModule.dictionary_database import DictionaryDatabase
from typing import Union

class DictionaryManager(DataKeyManager):
    """
    Wraps the DataKeyManager implementation so as to specify the functionality of managing
    dictionary encodings.
    """
    def __init__(self, name :str, outputDirectory :str, errLogDirectory :str, verbose=True) -> None:
        super().__init__(name, outputDirectory, errLogDirectory, verbose)
        self.__name = name
        m = time_stamped_msg("data-key-manager-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))
        self.__database = DictionaryDatabase()
        self.__verbose = verbose
        self.__file_manager = FileManager(self.__name,verbose)
        self.__file_manager.assure_directory(errLogDirectory)
        
    def add_encode(self,dictionary : dict, name : str) -> None:
        """
            Provided a dictionary and the name under which to store it, the function encodes teh dictionary
            and charts its presence in the structure for later retrieval and use.
        """
        try:
            n = "{}-{}".format(self.__name,name)
            self.__database.add(n, dictionary)
            self.encode_dictionary(n,dictionary)
        except Exception as e:
            m = "(DictionaryManager) unexpected error while encoding dictionary...({})...\nerror --> {}".format(str(name),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)
            
    def add_load(self, dictionary : dict, name : str, DKM_file : str) -> None:
        """
            Add a dictionary to the manager and load its preexisting encoding.
        """
        try:
            n = "{}-{}".format(self.__name,name)
            self.__database.add(n,dictionary)
            self.load(n,DKM_file)
        except Exception as e:
            m = "(DictionaryManager) unexpected error while loading DKM file...({})...\nerror --> {}".format(str(DKM_file),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)
        
        
    def get(self, name : str, code : Union[str,int]):
        """
            Requires the name alias used to store the dictionary and the code within the dictionary
            desired to pull.
        """
        try:
            n = "{}-{}".format(self.__name,name)
            keytrail = self.fetch_keytrail(n,code)
            d = self.__database.get(n)
            while (keytrail != []):
                d = d[keytrail[0]]
                keytrail = keytrail[1:]
            return d
        except Exception as e:
            m = "(DictionaryManager) unexpected error while decoding...({} > {})...\nerror --> {}".format(str(name),code,str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)
    
# Example
#from WebsiteGathering.websites import WEBSITE_DATASET
#output_file = '../../OutputFiles/SearchData/'
#log_file = '../../OutputFiles/Errors/'
#name = 'tester'
#verbose = True
#file = '../../OutputFiles/SearchData/WEBSITES-DKM-tester-encode_map-05_59PM-on-November-29.json'

#DM = DictionaryManager(name,output_file,log_file,verbose)
#DM.add_load(WEBSITE_DATASET,'WEB', file)
#print(DM.get('WEB',8))