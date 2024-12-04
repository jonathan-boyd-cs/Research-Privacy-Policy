#!/usr/bin/env python3
"""_summary_
        The WebAnalysisSuite TextTransformer is a subclass of the TextAnalyzer.
        This class functions to transform RS files from the WASTP into statistical 
        data, which presently revolves around text complexity.
        The TextAnalyzer and remaining pipeline is accepting of variance in the provided
        analysis. Modulating the TextAnalyzer file would generate subsequent changes down the pipeline
        hypothetically without error.
"""

import json
import sys
sys.path.append('../../')
from StatisticalModule.TextAnalysisModule.text_analyzer import TextAnalyzer
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from FileManager.file_manager import FileManager


class WASTextTransformer(TextAnalyzer):
    """_summary_
        The WebAnalysisSuite TextTransformer is a subclass of the TextAnalyzer.
        This class functions to transform RS files from the WASTP into statistical 
        data, which presently revolves around text complexity.
    A
    """
    def __init__(self, name, outputDirectory, errLogDirectory, verbose=True):
        super().__init__(name,errLogDirectory,verbose)
        self.__outputDirectory = outputDirectory
        self.__name = name
        self.__verbose = verbose
        self.__file_manager = FileManager(name,errLogDirectory, verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
        m = time_stamped_msg("was-text-transformer-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))
        
    
    def transform_WASTP_RS_file(self, filename : str, tag : str) -> str:
        """_summary_
            Carries out the main functionality of the class...
        Args:
            filename (str): the name of the RS file to process
            tag (str): used to store the result

        Returns:
            str: filename of file  produced by operation
        """
        data = None
        try:
            with open(filename, 'r') as f:
                data = json.load(f)    
                
            # Will analyze the complexity of the generated 'stories'
            data  = data['stories']
     
            maybe_print(self.__verbose, 
            "(WASTextTransformer) successfully loaded data for {}...".format(
                tag
            ))
            
            
            for website in data.keys():
                maybe_print(self.__verbose, 
                    "(WASTextTransformer) running transformation analysis for {}...".format(
                website
                ))
                self.process_text(website, data[website])
            m = time_stamped_msg("WASTT-{}-{}".format(
                 self.__name, tag
            ))
            file = "{}{}.json".format(self.__outputDirectory,m)
            self.to_json(file)
            maybe_print(self.__verbose, 
            "(WASTextTransformer) finished job for {}...".format(
                tag
            ))
            return file
        
        except KeyboardInterrupt:
            sys.exit()
        
        except Exception as e:
            m = "(WASTextTransformer) error in transformation routine... error --> {}".format(str(e))
            self.__err_database.add("{}-{}".format(self.__name,tag),m)
            raise(e)

## Example
#name = 'testing'
#outputDirectory = '../../OutputFiles/WAS/CLEANING/'
#errLogDirectory = '../../OutputFiles/Errors/WAS/'
#verbose = True
#file = '../../OutputFiles/WAS/CLEANING/testing-WASTextProcessor-04_44PM-on-November-30-RS.json'

#WASTT = WASTextTransformer(name,outputDirectory,errLogDirectory,verbose)
#WASTT.transform_WASTP_RS_file(file,'test')