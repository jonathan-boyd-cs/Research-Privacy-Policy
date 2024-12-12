#!/usr/bin/env python3

"""
Basic database module separated from other files for ease of extension in the future.
"""

import json
from FileManager.file_manager import FileManager
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
import random
from ErrorHandleModule.general import time_stamped_msg

class CleanerDatabase:
    def __init__(self):
        self.__store = {}
        self.__count = 0
        self.__file_manager = FileManager('cleaner',False)
        m = time_stamped_msg('cleaner-database-{}'.format(random.randint(2,500)))
        self.__err_database = ErrorDatabase('{}.txt'.format(m))
        
    def add(self,id,data):
        if not str(id) in self.__store:
            self.__count += 1
        self.__store[str(id)] = data
       
    
    def remove(self, id):
        if str(id) in self.__store:
            del self.__store[str(id)]
            self.__count -= 1
            
    def get(self,id):
        if str(id) in self.__store:
            return self.__store[str(id)]
    
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
  
    def to_json(self, filename):
        try:
            
            self.__file_manager.assure_directory(filename)
            with open(filename,'w') as f:
                json.dump(self.__store,f)
        except Exception as e:
            self.__err_database.add(self.__name,
                'cleaner database failed to format json\
                     for {}...\nerror -->{}'.format(filename,str(e)))