#!/usr/bin/env python3

"""
Basic database module separated from other files for ease of extension in the future.
"""
import sys
sys.path.append('../../')
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg


class AnalysisSuiteDatabase:
    def __init__(self,name, errLogDirectory):
        self.__name = name
        self.__database =  {
                                'successful':{
                                    'results':{},
                                    'count':0
                                },
                                'unsuccessful':{
                                    'results':{},
                                    'count':0
                                }
                              }
        m = time_stamped_msg("analysis-suite-database-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))
        
    def add(self,id,data, state):
        if not str(id) in self.__database[state]['results']:
            self.__database[state]['count'] += 1
        self.__database[state]['results'][str(id)] = data
       
    
    def remove(self, id, state):
        if str(id) in self.__database[state]['results']:
            del self.__database[state]['results'][id]
            self.__database[state]['count'] -= 1
            
    def get(self,id, state):
        if str(id) in self.__database[state]['results']:
            return self.__database[state]['results'][id]
    
    def keys(self):
        keys = {
                'successful':{x for x in self.__database['successful']['results'].keys()},
                'unsuccessful':{x for x in self.__database['unsuccessful']['results'].keys()}
            }
        return keys  
    
    def dump(self):
        return self.__database
    
    def has(self,id,state):
        return (str(id) in self.__database[state]['results'])
    
    def flush(self):
        self.__database['successful']['results'].clear()
        self.__database['unsuccessful']['results'].clear()
        self.__database['successful']['count'] = 0
        self.__database['successful']['count'] = 0


    def get_count(self, state):
        return self.__database[state]['count']
  
    def save(self, filename):
        try:
            self.to_json(filename)
        except Exception as e:
            self.__err_database.add(self.__name,
                'analysis suite database failed to save...\nerror -->{}'.format(str(e)))
            raise(e)
  
    def to_json(self, filename):
        try:
            with open(filename,'a') as f:
                json.dump(self.__database,f)
        except Exception as e:
            self.__err_database.add(self.__name,
                'analysis suite database failed to format json\
                     for {}...\nerror -->{}'.format(filename,str(e)))
            raise(e)