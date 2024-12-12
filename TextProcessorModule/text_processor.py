from TextProcessorModule.text_data_container import TextDataContainer
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from FileManager.file_manager import FileManager

import json


class TextProcessor :
    
    def __init__(self, name, errLogDirectory, verbose=True):
        self.__database = {
            'raw':{},
            'stories':{}
        }
        self.__unique_count = 0
        m = time_stamped_msg("{}-WAStextProcessor")
        file = "{}{}.txt".format(errLogDirectory, m)
        self.__err_database = ErrorDatabase(file)
        self.__name = name
        self.__verbose = verbose
        self.__file_manager = FileManager(self.__name,verbose)
        self.__file_manager.assure_directory(errLogDirectory)
    
    def set_database(self, raw_data, story_data):
        try:
            self.__database['raw'].clear()
            self.__unique_count = 0
            for key in raw_data:
                self.__database['raw'][key] = TextDataContainer(key)
                self.__unique_count += 1
                for text in raw_data[key]:
                    self.__database['raw'][key].add_text(text)
            self.__database['stories'].clear()
            self.__database['stories'] = story_data
        except Exception as e:
            m = "(TextProcessor) error in setting database...\nerror --> {}".format(str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)


    def process_text(self, id, text):
        try:
            if not id in self.__database['raw']:
                self.__database['raw'][id] = TextDataContainer(id)
                self.__unique_count += 1
            
            
            self.__database['raw'][id].add_text(text)
        except Exception as e:
            m = "(TextProcessor) error in processing text...\nerror --> {}".format(str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)

        
    def __generate_story(self, id):
        try:
            if id in self.__database['raw']:
                container = self.__database['raw'][id]
                text = container.get_text()
                story = ". ".join(text) + "."
                self.__database['stories'][id] = story
                return story
        except Exception as e:
            m = "(TextProcessor) error in internal story generation method...\nerror --> {}".format(str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)

        
    def write_book(self):
        try:
            for id in self.__database['raw'].keys():
                self.__generate_story(id)
        except Exception as e:
            m = "(TextProcessor) error encountered while writing book...\nerror --> {}".format(str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)

        
    def get_raw(self, id):
        if id in self.__database['raw']:
            return self.__database['raw'][id]
        
        else:
            return None
    
    def get_story(self,id):
        try:
            if id in self.__database['stories']:
                return self.__database['stories'][id]
            elif id in self.__database['raw']:
                story = self.__generate_story(id)
                return story
            else:
                return None
        except Exception as e:
            m = "(TextProcessor) error retrieving story from database...\nerror --> {}".format(str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)

        
    def get_database(self):
        return self.__database
    
    def get_count(self):
        return self.__unique_count
    
    def delete_entry(self,id):
        if id in self.__database['raw']:
            del self.__database['raw'][id]
        if id in self.__database['stories']:
            del self.__database['stories'][id]
        self.__unique_count -= 1
    
    def has_entry(self, id):
        return id in self.__database['raw']

    def save_data(self, filename):
        self.__file_manager.assure_directory(filename)
        try:
            data = {'raw': {x : [] for x in self.__database['raw'].keys()} ,
                    'stories': self.__database['stories']}

            for key in data['raw'].keys():
                data['raw'][key] = \
                    self.__database['raw'][key].get_text()
            
            with open(filename, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            m = "(TextProcessor) error in json formatting...\nerror --> {}".format(str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)



# Example
# tp = TextProcessor('test','./',True)
# tp.process_text("https://dogmeat.com", "Welcome to my show")
# tp.process_text("https://dogmeat.com", "It will be great")
# tp.process_text("https://dogmeat.com", "We have biscuits")
# tp.process_text("https://dogmeat.com", "We have balls")

# print(tp.get_count())
# print(tp.has_entry("https://dogmeat.com"))
# print(tp.get_raw("https://dogmeat.com"))
# print(tp.get_story("https://dogmeat.com"))
# d = tp.get_database()
# print(d)