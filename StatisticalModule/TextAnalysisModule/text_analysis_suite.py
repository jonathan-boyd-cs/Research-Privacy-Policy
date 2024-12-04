import textstat
import sys
sys.path.append('../../')
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from FileManager.file_manager import FileManager


class TextAnalysisSuite:
    def __init__(self, name : str, errLogDirectory : str, verbose : str=True):
        self.__name = name
        self.__verbose = verbose
        self.__file_manager = FileManager(name,errLogDirectory, verbose)
        self.__file_manager.assure_directory(errLogDirectory)
        m = time_stamped_msg("text-analysis-suit-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))


    def flesch_kincaid(self,text : str):
        try:
            return textstat.flesch_kincaid_grade(text)
        except Exception as e:
            m = "(TextAnalysisSuite) failure in flesch_kincaid_grade... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)
            
            
    def automated_readability(self,text : str):
        try:
            return textstat.automated_readability_index(text)
        except Exception as e:
            m = "(TextAnalysisSuite) failure in automated_readability_index... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)
            
    def coleman_liau(self,text : str):
        try:
            return textstat.coleman_liau_index(text )
        except Exception as e:
            m = "(TextAnalysisSuite) failure in coleman_liau_index... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)
            
            
    def flesch_reading_ease(self,text : str):
        try:
            return textstat.flesch_reading_ease(text )
        except Exception as e:
            m = "(TextAnalysisSuite) failure in flesch_reading_ease... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)
            
            
    def gunning_fog(self,text : str):
        try:
            return textstat.gunning_fog(text )
        except Exception as e:
            m = "(TextAnalysisSuite) failure in gunning_fog... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)
            
            
    def smog(self,text : str):
        try:
            return textstat.smog_index(text )
        except Exception as e:
            m = "(TextAnalysisSuite) failure in smog_index... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)
            
    def word_count(self,text : str):
        try:
            return textstat.lexicon_count(text ,removepunct=True)
        except Exception as e:
            m = "(TextAnalysisSuite) failure in lexicon_count... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)
            
    def sentence_count(self,text : str):
        try:
            return textstat.sentence_count(text)
        except Exception as e:
            m = "(TextAnalysisSuite) failure in sentence_count... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)
            
    def long_word_count(self,text : str):
        try:
            return textstat.polysyllabcount(text)
        except Exception as e:
            m = "(TextAnalysisSuite) failure in polysyllabcount... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)
    
    def reading_time(self,text : str):
        try:
            return textstat.reading_time(text, ms_per_char=14.69)
        except Exception as e:
            m = "(TextAnalysisSuite) failure in reading_time... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)
            
    def standard(self, text : str):
        try:
            return textstat.text_standard(text, float_output=True)
        except Exception as e:
            m = "(TextAnalysisSuite) failure in text_standard... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)
            
    def dale_chall(self, text : str):
        try:
            return textstat.dale_chall_readability_score(text)
        except Exception as e:
            m = "(TextAnalysisSuite) failure in dale_chall_readability_score... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)

    def avg_sentence_length(self, text : str):
        try:
            sentences = text.split('.')
            lengths = [len(s.split()) for s in sentences]
            mean = (sum(lengths)) / len(lengths)
            return mean
        except Exception as e:
            m = "(TextAnalysisSuite) failure in avg_sentence_length... error --> {}".format(str(e))
            self.__err_database.add((self.__name),m)
            maybe_print(self.__verbose,m)
            raise (e)
            