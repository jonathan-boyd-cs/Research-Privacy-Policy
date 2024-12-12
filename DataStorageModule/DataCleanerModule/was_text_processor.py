#!/usr/bin/env python3

"""_summary_
    A component of the WebAnalysisSuite cleaning pipeline...
    This module consists of the WASTextProcessor. a subclass of the TextProcessor.
    The class functions to analyze word counts at various heirarchical levels,
    given a provided dictionary reference. It also strips repetative data and contatenates all recieved
    text into a 'story' returned in an RS file.


"""

import json
import sys
sys.path.append('../../')
from TextProcessorModule.text_processor import TextProcessor
from DataStorageModule.DataCleanerModule.cleaner_database import CleanerDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from FileManager.file_manager import FileManager
from typing import List
from typing import Union

class WASTextProcessor(TextProcessor):
    """_summary_

        - WASTextProcessor (TextProcessor): 
                _The class functions to analyze word counts at various heirarchical levels,
                given a provided dictionary reference._
    """
    def __init__(self, name :str , reference : dict, outputDirectory : str ,errLogDirectory : str, verbose=True) -> None:
        super().__init__(name,errLogDirectory)
        self.__name = name
        # Reference is a heirarchical dictionary of key words to search for in the WASTP's operation
        self.__reference = reference
        self.__verbose = verbose
        self.__outputDirectory = outputDirectory
        self.__database = CleanerDatabase()
        m = time_stamped_msg("{}-WAStextProcessor")
        file = "{}{}.txt".format(errLogDirectory, m)
        self.__err_database = ErrorDatabase(file)
        self.__file_manager = FileManager(self.__name,verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)


    def process_merge_data(self, WASDM_file : str, tag : str) -> List[str] :
        """Carries out class's main functionality of processing text data.

        Args:
            WASDM_file (str): file of the associated results of the WASDataMerger cleaning process...
            tag (str): alias will be used as the key for the WASTP database entry corresponding to the file's data...

        Returns:
            [str,str]: files corresponding to the WASTP raw_stories database and word_count database respectively. 
        """
        _data = None
        with open(WASDM_file, 'r') as f:
            _data = json.load(f)

        # accessing the stored website results
        data = _data[list(_data.keys())[0]]
        
        websites_word_count = {}
        for website in data.keys():
            
            maybe_print(self.__verbose,
                    "(WASTextProcessor) processing text entries for {}...".format(website))
            
            
            site = {'primary':{},
                    'secondary':data[website]['secondary']}
            
            try:
                # analyze text data given word keys utilizing a dfs on the key heirarchy
                for key in self.__reference:
                    site['primary'][key] = {'count':0,
                                'lower':{}}
                    site['primary'][key]['count'] = self.__dfs_helper(
                                                name    = website, 
                                                key     = key, 
                                                current = self.__reference[key], 
                                                data    = data[website]['primary'][key], 
                                                prev_data = data[website]['primary'], 
                                                journal   = site['primary'][key]['lower'])
                    
                    maybe_print(self.__verbose,
                        "(WASTextProcessor) in total {} entries under category {}".format(
                            site['primary'][key]['count'], key))
                
                # Store text analysis results
                websites_word_count[website] = site
            
            except KeyboardInterrupt:
                sys.exit()    
            
            except Exception as e:
                m = "(WASTextProcessor) unexpected unexpected error while analyzing text...\
                        ({}--{})...\nerror --> {}".format(website,str(e))
                self.__err_database.add(self.__name,m)  
                raise(e)

                
        try:
            
            maybe_print(self.__verbose,"(WASTextProcessor) saving results...")
            
            self.__database.add(tag,websites_word_count)
            file = "{}{}.json".format(self.__outputDirectory,tag)
            self.__database.to_json(file)
            
            # generate Raw -> Stories data
            self.write_book()
            m = time_stamped_msg("{}-WASTextProcessor".format(tag))
            rs_file = '{}{}-RS.json'.format(self.__outputDirectory, m)
            # save data to json
            self.save_data(rs_file)
            
            return rs_file,file
        
        except Exception as e:
            m = "(WASTextProcessor) unexpected unexpected error while saving results...\
                        ({})...\nerror --> {}".format(WASDM_file,str(e))
            self.__err_database.add(self.__name,m)  
            maybe_print(self.__verbose,m)
            raise (e)

    def __dfs_helper(self, name :str, key :str, 
                   current : dict , 
                   data : Union[dict , List[str]], 
                   prev_data : Union[dict , List[str]], 
                   journal : dict) -> int:
        """_summary_

        Args:
            name (str): will be used as a key to store results
            key (str): utilized purely for verbose output
            current (dict): present location in the word tree heirarchy
            data (Union[dict , List[str]]): present location in data as aligned with the reference (current)
            prev_data (Union[dict , List[str]]): prior position before key traversal
            journal (dict): ledger to store intermediate calculations

        Returns:
            _type_: word count for the calling's heirarchical position
        """
        
        if type(data) == list:
            # location of text data by definition of the WAS pipeline.
            for entry in data:
                # Clean text data and store
                self.process_text(name, entry)
            maybe_print(self.__verbose,
                "(WASTextProcessor) charted {} entries for {}.".format(len(data), key))
            # Refers to number of entries discovered given a particular keyword
            return len(data)
        else: 
            count = 0
            # Begin calculating the entry counts for sublevel keywords in the tree.
            for k in current:
                journal[k] = {
                                'count':0,
                                'lower':{}
                            }
                
                journal[k]['count'] = self.__dfs_helper(
                                    name = name, 
                                    key  = k , 
                                    current = current[k],  
                                    data    = data[k],
                                    prev_data = prev_data,
                                    journal   = journal[k]['lower']
                )
                # Toss the lower dictioanry at the bottom of the keyword heirarchy
                if not bool(journal[k]['lower']):
                    del journal[k]['lower']
                    
                count += journal[k]['count']
            return count


    def load(self, file: str) -> None:
        maybe_print(self.__verbose,"(WASTextProcessor) attempting to load processor state from {}.".format(file))
        with open(file, 'r') as f:
            data = json.load(f)
            self.set_database(data['raw'], data['stories'])
            maybe_print(self.__verbose,"(WASTextProcessor) Attempt successful...")


        
# Example
#outputDirectory = '../../OutputFiles/WAS/CLEANING/'
#tag = 'testing'
#from PolicyQueryModule.testing import PRIVACY_POLICY_KEY_PHRASES  
#WASTP = WASTextProcessor('testing',PRIVACY_POLICY_KEY_PHRASES,outputDirectory,"../../OutputFiles/Errors/WAS/")
#WASTP.process_merge_data('../../OutputFiles/WAS/CLEANING/testing-09_35PM-on-November-29-merge.json',tag)
#m = time_stamped_msg("{}-WASTextProcessor".format(tag))
#WASTP.write_book()
#WASTP.save_data("{}{}-RS.json".format(outputDirectory,m))
