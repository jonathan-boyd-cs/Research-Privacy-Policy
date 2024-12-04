#!/usr/bin/env python3
"""
    Class serves as a gate keeper for the codebase's TextAnalysisDatabase.
    The TextAnalyzer receives text input and passes it to the database for statistical analysis
    and storage.

"""

import sys
from typing import KeysView
sys.path.append('../../')
from DataStorageModule.PreprocessorStorageModule.text_analysis_database import TextAnalysisDatabase
from FileManager.file_manager import FileManager
from ErrorHandleModule.general import time_stamped_msg


class TextAnalyzer(TextAnalysisDatabase):
    
    def __init__(self, name : str, errLogDirectory : str, verbose : str =True) -> None:
        super().__init__(name, errLogDirectory, verbose)
        m = time_stamped_msg("text-analyzer-{}".format(name))
        self.__file_manager = FileManager(name,verbose)
        self.__file_manager.assure_directory(errLogDirectory)
    
    def process_text(self, subject : str, text : str) -> None:
        self.add(subject,text)
    
    def get_subject_results(self, subject : str) -> dict:
        return self.get_data(subject)
    
            
    def get_subjects(self) -> KeysView:
        return self.get_keys()
    

    def get_data(self, id : str) -> dict:
        return super().get_data(id)
# Example

#name = 'testing'
#errLog = '../../OutputFiles/Errors/TA/'

#TA = TextAnalyzer(name, errLog)
#TA.process_text("Dog","Where there was one there was more. Where there was more there were few. I never knew.")
#TA.process_text("Dog","He was a boy and I was a man. So I ate his plate and it was great..")
#TA.process_text("Dog","Many places to be yet I am here. I would rather be elsewhere but I am no where")
#TA.process_text("Cat","Where there was one there was more. Where there was more there were few. I never knew.")
#s = TA.get_subjects()
#v = TA.get_subject_results('Dog')
#v2 = TA.get_subject_results('Cat')
#print(s)
#print(v)
#print(v2)
#TA.to_json('./testing-text-analyzer.json')