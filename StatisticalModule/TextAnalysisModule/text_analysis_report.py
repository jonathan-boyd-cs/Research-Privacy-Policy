import sys
sys.path.append('../../')
from StatisticalModule.TextAnalysisModule.text_analysis_suite import TextAnalysisSuite
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from FileManager.file_manager import FileManager


class AnalysisData:
    
    def __init__(self,method, data):
        self.__method = method
        self.__data = data
    
    def get_method(self):
        return self.__method

    def get_data(self):
        return self.__data
        


class TextAnalysisReport(TextAnalysisSuite):
    def __init__(self, id, text, errLogDirectory, verbose=True):
        super().__init__(id, errLogDirectory, verbose)
        self.__data = {}
        self.analyze(text)
        self.__id = id
        
        m = time_stamped_msg('text-analysis-suite-{}'.format(id))
        file = '{}{}.txt'.format(errLogDirectory,m)
        self.__err_database = ErrorDatabase(file)
        self.__file_manager = FileManager(id, errLogDirectory,verbose)
        self.__file_manager.assure_directory(errLogDirectory)
        self.__methods = [ 
                          'flesch_kincaid','automated_readability', 'coleman_liau', 
                    'flesch_reading_ease', 'gunning_fog','smog',
                    'word_count','sentence_count','long_word_count',
                    'reading_time','standard','dale_chall','avg_sentence_length']
        
    def analyze(self,text):
        self.__add('flesch_kincaid', text, self.flesch_kincaid)
        
        self.__add('automated_readability', text, self.automated_readability)
        self.__add('coleman_liau',text,self.coleman_liau)
        self.__add('flesch_reading_ease',text,self.flesch_reading_ease)
        self.__add('gunning_fog',text,self.gunning_fog)
        self.__add('smog',text,self.smog)
        self.__add('word_count',text,self.word_count)
        self.__add('sentence_count',text,self.sentence_count)
        self.__add('long_word_count',text,self.long_word_count)
        self.__add('reading_time',text,self.reading_time)
        self.__add('standard',text,self.standard)
        self.__add('dale_chall',text,self.dale_chall)
        self.__add('avg_sentence_length',text,self.avg_sentence_length)
        
    def get_methods(self):
        return self.__methods

    def __add(self, id, text, func):
        try:
            self.__data[id] = AnalysisData(func,func(text.strip()))
        except Exception as e:
            m = "(TextAnalysisSuite) unexpected error while running mathematical process on text...({})...\nerror --> {}".format(str(func),str(e))
            self.__err_database.add(self.__name,m)
            maybe_print(self.__verbose, m)
            raise Exception(e)

    def has(self,id):
        return id in self.__data
    

    def get_all(self):
        return {
                    x:self.__data[x].get_data() for x in self.__methods
                }
    
    def get_data_from(self, id):
        if self.has(id):
            return self.__data[id].get_data()
        
    def get_method_from(self,id):
        if self.has(id):
            return self.__data[id].get_method()
    
    def __str__(self):
        s = "Analysis for: {}\n".format(self.__id)
        for data in self.__data.keys():
            d = self.__data[data].get_data()
            method = " ".join(data.split("-"))
            s += "--------------------------\n"
            s += method + ":\n" + str(d) + "\n"
        s += "--------------------------\n"
        return s