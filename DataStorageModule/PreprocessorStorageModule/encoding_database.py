#!/usr/bin/env python3

"""
    Encoder database module separated from other files for ease of extension in the future.
"""
import json
import copy
import sys
sys.path.append('../../')
from FileManager.file_manager import FileManager
from ErrorHandleModule.general import time_stamped_msg
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase

class EncoderDatabase:
    def __init__(self,errLogDirectory):
        self.__store = {}
        self.__count = 0
        self.__file_manager = FileManager('encoder',True)
        m = time_stamped_msg('encoder')
        self.__err_database = ErrorDatabase("{}{}-WASDC.txt".format(errLogDirectory,m))
        
    def add(self,id,data):
        if not str(id) in self.__store:
            self.__store[str(id)] = {
                'code_ptr' : 0,
                'data_bank': {}
                
            }
            self.__count += 1
        
        code = self.__store[str(id)]['code_ptr']
        self.__store[str(id)]['data_bank'][str(code)] = data
        self.__store[str(id)]['code_ptr'] += 1
       
    
    def remove(self, id):
        if str(id) in self.__store:
            del self.__store[str(id)]
            self.__count -= 1
            
    
    def remove(self, id, code):
        if str(id) in self.__store:
            if str(code) in self.__store[str(id)]['data_bank']:
                del self.__store[str(id)]['data_bank'][str(code)]
            
    def get_total(self,id):
        """
            returns entire encoding structure for the given id
        """
        if self.has(str(id)):
            return self.__store[str(id)]
    
    
    def get(self,id, code):
        """
            returns a specific item given the id and provided code
        """
        if self.has(str(id)):
            if str(code) in self.__store[str(id)]['data_bank']:
                return self.__store[str(id)]['data_bank'][str(code)]
    
    
    def set(self,id, database):
        """
            Force the identity of a database for the given id
        """
        if not self.has(str(id)):
            self.__store[str(id)] =  {
                'code_ptr' : 0,
                'data_bank': {}
            }
            self.__count += 1
        self.__store[str(id)] = copy.deepcopy(database)
    
    def keys(self):
        return list(self.__store.keys())    
    
    def dump(self):
        return self.__store
    
    def has(self,id):
        return (str(id) in self.__store)
    
    def flush(self):
        self.__store.clear()
        self.__count =0

    def get_count(self):
        return self.__count
  
    def to_json(self, name,filename):
        if self.has(name):
            try:
                self.__file_manager.assure_directory(filename)
                with open(filename,'w') as f:
                    json.dump(self.__store[name],f)
            except Exception as e:
                self.__err_database.add(name,
                    'EncoderDatabase  failed to format json\
                        for {}...\nerror -->{}'.format(filename,str(e)))