#!/usr/bin/env python3
import json

"""
Basic database module separated from other files for ease of extension in the future.
"""

class PageDatabase:
    def __init__(self):
        self.__store = {}
        self.__count = 0
        
    def add(self,id,data):
        if not str(id) in self.__store:
            self.__count += 1
        self.__store[str(id)] = data
       
    
    def remove(self, id):
        if str(id) in self.__store:
            del self.__store[id]
            self.__count -= 1
            
    def get(self,id):
        if str(id) in self.__store:
            return self.__store[id]
    
    def keys(self):
        return list(self.__store.keys())    
    
    def dump(self):
        return self.__store
    
    def has(self,id):
        return (str(id) in self.__store)
    
    def flush(self):
        self.__store.clear()
        self.__count = 0

    def get_count(self):
        return self.__count
  