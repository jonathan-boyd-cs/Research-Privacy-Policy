import json
#!/usr/bin/env python3

"""
Basic database module separated from other files for ease of extension in the future.
"""
import sys
sys.path.append('../../')
from FileManager.file_manager import FileManager
class ErrorDatabase:
    def __init__(self, file=None):
        self.__store = {}
        self.__count = 0
        self.__file = file
        self.__file_manager = FileManager('e','./FileManager/',False)
        self.__file_manager.assure_directory('./FileManager/')
        
    def add(self,id,data):
        if not str(id) in self.__store:
            self.__count += 1
            self.__store[str(id)] = []
        self.__store[str(id)].append( data )
        
        if self.__file != None:
            with open(self.__file,'a') as f:
                f.write("\n{}\n{}\n".format(id,data))
       
    
    
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
  
    def to_json(self, filename):
        try:
            self.__file_manager.assure_directory(filename)
            with open(filename,'w') as f:
                json.dump(self.__store,f)
        except Exception as e:
            raise (e)