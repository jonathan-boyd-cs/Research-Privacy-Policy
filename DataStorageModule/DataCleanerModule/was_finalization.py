#!/usr/bin/env python3
"""
    Class serves as the end of the WAS cleaning pipeline, acting by merging the results of
    statistical transformations on RS files with the remaining text processor file. This class formats 
    data in a structure ready to be delivered the the CSV creator class in the graphics storage module.
    (WASToCSVConverter)
"""

import json
import sys
sys.path.append('../../')
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from FileManager.file_manager import FileManager


class WASFinalizer:
    """
        This class formats data passed from the WASTP and WASTT in a structure ready 
        to be delivered the the CSV creator class in the graphics storage module.
    """
    def __init__(self, name : str, outputDirectory : str, errLogDirectory : str, verbose=True) -> str :
        self.__outputDirectory = outputDirectory
        self.__name = name
        self.__verbose = verbose
        self.__file_manager = FileManager(name,errLogDirectory, verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
        m = time_stamped_msg("was-finalizer-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))
        
    def WASTT_WASTP_merger(self, WASTT_file : str, WASTP_file : str, tag : str) -> str:
        WASTT=None
        WASTP=None
        maybe_print(self.__verbose, "(WASFinalizer) Attempting a merger...")
        try:
            with open(WASTT_file, 'r') as f:
                WASTT = json.load(f)
                maybe_print(self.__verbose, "(WASFinalizer) WASTT data loaded successfully.")
                
            with open(WASTP_file, 'r') as f:
                WASTP = json.load(f)
                maybe_print(self.__verbose, "(WASFinalizer) WASTP data loaded successfully.")

            maybe_print(self.__verbose, "(WASFinalizer) Beginning merge operation...")

            data_key = list(WASTP.keys())[0]
            for website in WASTP[data_key].keys():
                maybe_print(self.__verbose, "(WASFinalizer) merging ({})...".format(website))

                d = WASTT[website]
                statistics = d[list(d.keys())[0]]
                WASTP[data_key][website]['statistics'] = statistics
            
            maybe_print(self.__verbose, "(WASFinalizer) Finished merge operation...")
            
            m = time_stamped_msg('Finalized-{}-{}'.format(self.__name,tag))
            file = "{}{}.json".format(self.__outputDirectory,m)
            
            with open(file,'w') as f:
                json.dump(WASTP,f)
            maybe_print(self.__verbose, "(WASFinalizer) Results for ({}) dumped to json.".format(
                tag
            ))
            return file
        
        except KeyboardInterrupt:
            sys.exit()

        except Exception as e:
            m = "(WASFinalizer) Failure in merge routine... error --> {}".format(str(e))
            self.__err_database.add("{}-{}".format(self.__name,tag),m)
            raise(e)
# Example
#outputDirectory = '../../OutputFiles/WAS/COMPLETE/'
#errLogDirectory = '../../OutputFiles/Errors/WAS/'
#verbose =True
#name = 'testing'

#WASTP_file = '../../OutputFiles/WAS/CLEANING/testing-WASTextProcessor-04_44PM-on-November-30.jon'
#WASTT_file = '../../OutputFiles/WAS/CLEANING/WASTT-testing-test-05_35PM-on-November-30.json'#
####
#WASF = WASFinalizer(name,outputDirectory,errLogDirectory,verbose)
#WASF.WASTT_WASTP_merger(WASTT_file, WASTP_file, name)