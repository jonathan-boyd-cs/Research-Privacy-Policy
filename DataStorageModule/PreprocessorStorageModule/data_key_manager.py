#!/usr/bin/env python3
"""

 Class servers as an encoder for dictionaries and their heirarchical structure.
 Given the traversal of a dictionary's keys, a particular encoding is formed, with a
 unique code for each path. Aids in handling website and phrase data in this implementation.
 All concepts corresponding have not yet been integrated.

"""
from typing import List
import json
import sys
sys.path.append('../../')
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from FileManager.file_manager import FileManager
from DataStorageModule.PreprocessorStorageModule.key_encoder import KeyEncoder

class DataKeyManager(KeyEncoder):
    """
    Class servers as an encoder for dictionaries (Key trails) and their heirarchical structure.
    
    """
    def __init__(self, name : str, outputDirectory : str, errLogDirectory : str, verbose=True) -> None:
        super().__init__(name, outputDirectory, errLogDirectory, verbose)
        print(outputDirectory)
        self.__name = name
        m = time_stamped_msg("data-key-manager-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))
        self.__verbose = verbose
        self.__file_manager = FileManager(self.__name,verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
        self.__category_dict = {}
        
    def encode_dictionary(self, name : str, dictionary : dict) -> None:
        """
            Delegates action to internal functions... encodes the provided dictionary tree and
            identifies subcategory heirarchical levels.
        """
        self.__encode_dictionary(name, " ", dictionary)
        self.__categorize(name)
        
    def __categorize(self, tag : str) -> None:
        """
             Identifies dictionary tree subcategory heirarchical levels. Will pull the dictionary
             corresponding to the provided tag.
        """
        try:
            encoding = self.dump(tag)['data_bank']
            level = 1
            # to hold subcategories for each level (as a ' key trail ').
            cats = {level:{}}
            
            # chart the heirarchical level of each key trail (dictionary tree path)
            for code in encoding:
                entity = encoding[code].split("^^")
                level = len(entity)
                if level not in cats:
                    cats[level] = {}
                    
                cats[level][code] = entity
            self.__category_dict[tag] = cats
        except Exception as e:
            m = "(DataKeyManager) unexpected error while categorizing...({})...\nerror --> {}".format(str(tag),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)        

    def get_levels(self, tag : str) -> List[any]:
        """
            Function used to determine how many heirarchical levels a dictionary tree posesses.
        
        """
        if tag in self.__category_dict:
            return self.__category_dict[tag].keys()
    
    def get_level_keys(self, tag, level):
        """
        
        
        """
        if tag in self.__category_dict:
            if level in self.__category_dict[tag]:
                return [self.decode(tag,x).split("^^") 
                        for x in  self.__category_dict[tag][level].keys()]
        
    def find(self, tag, what, at_idx):
        """
        
        
        """
        try:
            keys = self.get_level_keys(tag, at_idx+1)   
            for var in keys:
                if var[at_idx] == what:
                    return var
        except Exception as e:
            m = "(DataKeyManager) unexpected error while processing find...({})...\nerror --> {}".format(str(tag),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)        
        
    def __encode_dictionary(self, name, tag, dictionary):
        """
        
        
        """
        try:
            for top_key in dictionary.keys():
                if tag == " ":
                    tag__ = str(top_key)
                else:
                    tag__ = "{}^^{}".format(tag,str(top_key))
                self.encode(name, tag__)
                if type(dictionary[top_key]) != dict:
                    continue
                self.__encode_dictionary(name, tag__, dictionary[top_key])

            m = time_stamped_msg("DKM-{}-encode_map".format(self.__name))
            self.save(name , "{}.json".format(m))
        
        except Exception as e:
            
            m = "(DataKeyManager) unexpected error while encoding dictionary...({})...\nerror --> {}".format(str(tag),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)
            
    def load(self, name, filename):
        data = None
        try:
            with open(filename,'r') as f:
                data = json.load(f)
            self.set(name, data)
            
        except Exception as e:
            m = "(DataKeyManager) unexpected error while loading file...({})...\nerror --> {}".format(str(filename),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)
            
    def fetch_keytrail(self, name, code):
        """
        
        
        """
        try:
            keys = self.decode(name,code)
            if keys == None:
                return None
            return keys.split("^^")
            
        except Exception as e:
            m = "(DataKeyManager) unexpected error while fetching key trail...({})...\nerror --> {}".format(str(name),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)
            
# Example
#output_file = '../../OutputFiles/WAS/'
#log_file = '../../OutputFiles/WAS/'
#name = 'tester'
#verbose = True

#DKM = DataKeyManager(name, output_file, log_file, verbose)
#DKM.encode_dictionary('PHRASES',PRIVACY_POLICY_KEY_PHRASES)
#DKM.encode_dictionary('WEBSITES',WebData)
#print(DKM.get_level_keys('WEBSITES',4)[4])
#level_keys = DKM.get_levels('WEBSITES')
#value_level = len(list(level_keys))

#reference = (DKM.get_level_keys('WEBSITES',value_level))

#top_level_value_count = 0
#while reference[top_level_value_count][:-1] == reference[top_level_value_count+1][:-1]:
#    top_level_value_count += 1

#print(top_level_value_count)


# load file created...

#DKM.load(name, '../../OutputFiles/SearchData/WEBSITES-DKM-tester-encode_map-05_59PM-on-November-29.json')

#i = None
#while i != 'end':
#    i = input('code: ')
#    keys = DKM.fetch_keytrail(name,i)
#    print(keys)