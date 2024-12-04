import json
#!/usr/bin/env python3

"""
Basic database module separated from other files for ease of extension in the future.
"""

import sys
sys.path.append('../')
from DataStorageModule.WebScraperStorageModule.scraper_database import ScraperDatabase

class ScrapeLocation:
    def __init__(self, id):
        self.__id = id
        self.__language = None
        self.__data = ScraperDatabase()
    
    def get_id(self):
        return self.__id
    
    def get_data(self):
        return self.__data
    
    def set_data(self, id, data):
        self.__data.add(id, data)
        
    def get_language(self):
        return self.__language
    
    def set_language(self, lang):
        self.__language = lang