class TextDataUnit :
    
    def __init__(self,id, text):
        self.__id = id
        self.__data = text
    
    def get_text(self):
        return self.__data
    
    def get_id(self):
        return self.__id
    
    def __str__(self):
        s = ("ID: {}\nDATA: {}\n".format(self.__id,self.__data))
        return s

class TextDataContainer:
    
    def __init__(self,id):
        self.__database = {}
        self.__entry_count = 0
        self.__id = id
        
    def add_text(self, text):
        text = text.strip()
        text = text.lower()
        if text not in self.__database:
            self.__database[text] = TextDataUnit(self.__entry_count, text)
            self.__entry_count += 1
            
    def remove_text(self, text):
        text = text.strip()
        text = text.lower()
        if text in self.__database:
            del self.__database[text]
            self.__entry_count -= 1
            
    def get_count(self):
        return self.__entry_count
    
    def get_text(self):
        return [self.__database[x].get_text() for x in self.__database.keys()]
    
    def has_text(self, text) :
        text = text.strip()
        text = text.lower()
        return text in self.__database
    
    def clear(self):
        self.__database.clear()
    
    
    def __str__(self):
        s= ("CONTAINER ID: {}\n".format(self.__id))
        for key in self.__database.keys():
            data = self.__database[key]
            print(type(data))
            s += "Entry ({}):\n{}".format(data.get_id(),data)
        return s