#!/usr/bin/env python3
"""
    Class functions by encoding strings to numerical values... that is
    encoding dictionary keys to numerical values. The EncoderDatabase words to 
    prescribe meaning to such bindings for ease of accessing a heirarchical dictionary
    tree at randomized locations.

"""

import sys
sys.path.append('../../')
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from FileManager.file_manager import FileManager
from DataStorageModule.PreprocessorStorageModule.encoding_database import EncoderDatabase

class KeyEncoder:
    def __init__(self, name :str, outputDirectory : str, errLogDirectory : str, verbose : bool =True) -> None:
        
        self.__name = name
        m = time_stamped_msg("key-encoder-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))
        self.__verbose = verbose
        self.__outputDirectory = outputDirectory
        self.__database = EncoderDatabase(errLogDirectory)
        self.__file_manager = FileManager(self.__name,verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)



    def encode(self, tag :str, key :str) -> None:
        """
            Add a key to the KeyEncoder's database under the alias of the tag
        """
        self.__database.add(str(tag).strip(),str(key).strip())
        
    def decode(self, tag : str, key : str) -> str:
        """
            Retrieve the key corresponding to a code for a particular tagged entity
        """
        return self.__database.get(str(tag).strip(),str(key).strip())
    
    def set(self, id : str,data : object) -> None:
        """
            Used to manually set the encodings for a given tag/id
        """
        self.__database.set(str(id), data )
        
    def dump(self, tag : str): 
        """
            Returns the entire encoding set for the given tag.
        
        """
        if self.__database.has(str(tag).strip()):
            return self.__database.get_total(tag)
    
    def save(self, name : str, filename : str) -> None:
        self.__file_manager.assure_directory(filename)
        file = "{}{}".format(self.__outputDirectory,filename)
        self.__database.to_json(str(name), file)