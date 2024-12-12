#!/usr/bin/env python3
"""
    Storage point for website urls
"""
import sys
sys.path.append('../')
from DataStorageModule.WebScraperStorageModule.url_database import UrlDatabase

class UrlManager:
    def __init__(self):
        self.__history = UrlDatabase()
        
        
    def set(self, id, url):
        self.__history.add(id,url)
    
    def get(self, id):
        if self.__history.has(id):
            return self.__history.get(id)
        return None
        
    def has(self, id):
        return self.__history.has(id)
          