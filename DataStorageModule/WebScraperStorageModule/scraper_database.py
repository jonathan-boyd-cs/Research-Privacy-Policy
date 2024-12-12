#!/usr/bin/env python3
import json

"""
Basic database module separated from other files for ease of extension in the future.
"""
from ErrorHandleModule.general import time_stamped_msg
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
import random

class ScraperDatabase:
    def __init__(self):
        self.__store = {}
        self.__count = 0
        m = time_stamped_msg('scraper-database-{}'.format(random.randint(2,600)))
        self.__err_database = ErrorDatabase(m)
        
    def add(self,id,data):
        if not str(id).strip() in self.__store:
            self.__count += 1
            self.__store[str(id).strip()] = {"data":{},
                                     "entry":0}
        
        entry = self.__store[str(id).strip()]["entry"]
        self.__store[str(id).strip()]["data"][entry] = data
        entry += 1
        self.__store[str(id).strip()]["entry"] = entry
       
    
    def remove(self, id):
        if str(id).strip() in self.__store:
            del self.__store[str(id).strip()]
            self.__count -= 1
            
    def get(self,id):
        if str(id).strip() in self.__store:
            return self.__store[str(id).strip()]
    
    def keys(self):
        return list(self.__store.keys())    
    
    def dump(self):
        return self.__store
    
    def has(self,id):
        return (str(id).strip() in self.__store)
    
    def flush(self):
        self.__store.clear()
        self.__count =0

    def get_count(self):
        return self.__count
  
    def to_json(self, filename):
        try:
            with open(filename,'w') as f:
                json.dump(self.__store,f)
        except Exception as e:
            self.__err_database.add(self.__name,
                'scraper database failed to format json\
                     for {}...\nerror -->{}'.format(filename,str(e)))
            
    def to_json_id(self, id, filename):
        if self.has(str(id).strip()):
            try:
                with open(filename,'w') as f:
                    json.dump({str(id):self.__store[str(id).strip()]},f)
            except Exception as e:
                self.__err_database.add(self.__name,
                    'scraper database failed to format json\
                        for {}...\nerror -->{}'.format(filename,str(e)))
                