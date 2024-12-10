#!/usr/bin/env python3
"""

    Serves as the entry point into the WAS cleaning pipeline...
    Parses scrape results and formats them into an appropriate structure.
"""

import json
import sys
sys.path.append('../../')
from DataStorageModule.DataCleanerModule.cleaner_database import CleanerDatabase
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
import copy
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from FileManager.file_manager import FileManager
from typing import Union, Callable

class WASDataCleaner:
    def __init__(self, name : str, phrase_legend : dict, outputDirectory : str, errLogDirectory : str, verbose= True, strict = False) -> None:
        """_summary_

        Args:
            name (str): _description_
            phrase_legend (dict): _description_
            outputDirectory (str): _description_
            errLogDirectory (str): _description_
            verbose (bool, optional): Determine whether console progression output is desired. Defaults to True.
            strict (bool, optional): Allows for modulation on whether or not incidental translation results are kept if not possessing the exact English text. Defaults to False.
        """
        self.__success = CleanerDatabase()
        self.__failure = CleanerDatabase()
        self.__name = name
        self.__phrase_references = phrase_legend
        self.__strict = strict
        self.__verbose = verbose
        self.__errLogDirectory = errLogDirectory
        m = time_stamped_msg(self.__name)
        self.__err_database = ErrorDatabase("{}{}-WASDC.txt".format(errLogDirectory,m))
        self.__outDirectory = outputDirectory
        self.__file_manager = FileManager(self.__name,verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
        
        
    def set_strict(self, boolean : bool):
        self.__strict = boolean

    def load_success(self,file_name : str, tag : str) -> str:
        """
            Carries out the class's main function of loading successful test results into a structure
            to pass down the pipeline.
        """
        file = file_name
        try:
            data = None
            with open(file , 'r') as f:
                data = json.load(f)
            assert(data != None)
        except Exception as e:
            self.__failure.add(tag,data['unsuccessful'])
            self.__file_manager.assure_directory('{}Failure/'.format(self.__errLogDirectory))
            failure_file = time_stamped_msg('failure')
            self.__failure.to_json("{}{}.json".format(failure_file))
            raise(e)
        data_cleaned = {}
        # accessing the successful scrape data...
        data =  data['successful']['results']
        try: 
            websites = list(data.keys())
            
            for website in websites:
                maybe_print(self.__verbose,
                    "(WASDataCleaner) processing text entries for {}...".format(website))
                data_cleaned[website] = {}
                # process accessory scrape data...
                data_accessory = data[website]['accessory']
                for accessory in data_accessory.keys():
                    data_cleaned[website][accessory] = data_accessory[accessory]
                # process main phrase scrape results...
                try:
                    data_main = data[website]['main'][website]
                
                except KeyboardInterrupt:
                    sys.exit()
                
                except Exception as e:
                    m = "(WebDataCleaner) unexpected error with web data parsing...\n throwing away results for...\
                         ({}--{})...\nerror --> {}".format(website,str(list(data[website]['main'].keys())),str(e))
                    self.__err_database.add(self.__name,m)    
                    del data_cleaned[website]
                    continue
                
                data_cleaned[website]['num-pages-analyzed'] = data_main['entry']
                data_cleaned[website]['pages'] = {}
                page_no = 0
                maybe_print(self.__verbose,
                    "(WASDataCleaner) extracted number of pages for this site... {}...".format(
                        data_cleaned[website]['num-pages-analyzed']))
                data_main = data_main['data']
                
                for link_query in data_main.keys():
                    maybe_print(self.__verbose,
                    "(WASDataCleaner) processing link query {}".format(link_query))
                    for link in data_main[link_query].keys():
                        maybe_print(self.__verbose,
                            "(WASDataCleaner) processing link  {}".format(link))
                        data_cleaned[website]['pages'][page_no] = {}
                        data_container = copy.deepcopy(self.__phrase_references)
                        maybe_print(self.__verbose,
                            "(WASDataCleaner) preparing to extract...")
                        for key in self.__phrase_references:
                            maybe_print(self.__verbose,
                                    "(WASDataCleaner) processing top level:  {}".format(key))
                            self.__dfs_helper(
                                            data_container[key],
                                            key, data_container,
                                            self.__default_clean, 
                                            data_main[link_query][link][key], 
                                            data_main[link_query][link] 
                                            )
                        maybe_print(self.__verbose,
                            "(WASDataCleaner) cleaning complete for link ({})...".format(link))
                        data_cleaned[website]['pages'][page_no] = data_container
                        page_no += 1
            maybe_print(self.__verbose,
                            "(WASDataCleaner) cleaner complete for operation ({})...".format(tag))
        
        except KeyboardInterrupt:
            sys.exit()
                      
        except Exception as e:
            m = "(WebDataCleaner) unexpected error while processing success results...{}\nerror --> {}".format(
                file_name,str(e))
            self.__err_database.add(self.__name,m)  
            raise(e)

        try:
            self.__success.add(tag,data_cleaned)
            name = time_stamped_msg('{}-WASDC'.format(self.__name))
            file = "{}{}.json".format(self.__outDirectory,name)
            self.__success.to_json(file)
            return file
        except Exception as e:
            m = "(WebDataCleaner) unexpected error while storing as json...{}\nerror --> {}".format(
                file_name,str(e))
            self.__err_database.add(self.__name,m)  
            raise(e)
            
    
    def __dfs_helper(self, current : Union[dict, int, float], key : str, previous : dict, act : Callable , data : dict, prev_data : dict) -> None:
        """
            Function acts as a diver, traversing a heirarchical structure until reaching a depth, followed by carrying out some act on data.
            Traverses the heirarchical phrase list in this instance.
        """
        try:
            if current == 0:
                maybe_print(self.__verbose,
                    "(WASDataCleaner) reached leaf for key... ({})".format(key))
                previous[key] = act(prev_data[key], key)
                maybe_print(self.__verbose,
                    "(WASDataCleaner) completed cleaning process for ({})...".format(key))
                return
            for k in current:
                maybe_print(self.__verbose,
                    "(WASDataCleaner) traversing sublebel for ({})...".format(k))
                self.__dfs_helper(current[k],k,current, act, data[k],data)
                maybe_print(self.__verbose,
                    "(WASDataCleaner) returned - sublebel  ({})...".format(k))   
            maybe_print(self.__verbose,
                "(WASDataCleaner) seeking new top level after ({})...".format(key))             
        except Exception as e:
            m = "(WebDataCleaner) unexpected error in dfs...{}\nerror --> {}".format(
                key,str(e))
            self.__err_database.add(self.__name,m)  
            raise(e)
        
    def __default_clean(self, data, key):
        maybe_print(self.__verbose,
                    "(WASDataCleaner) beginning cleaning process for ({})...".format(key))
        work = data['text']
        result_bank ={}
        for phrase in work.keys():
            text = work[phrase]
            # handles web scrapers tendancy to deliver multipke variations on translated text.
            for var in text:
                for translation in var.keys():
                    if type(var[translation]) == list :
                        if var[translation] == []:
                            continue
                        entry = var[translation][0]
                        
                    else:
                        entry = var[translation]
                        
                    if entry == None:
                        continue
                    if self.__strict:
                    # strict
                        if key not in entry.split():
                            continue
                    
                    if not entry in result_bank:
                        maybe_print(self.__verbose,
                            "(WASDataCleaner) storing text result..,")
                        result_bank[entry] = 1
        # returns a list of unique text elements.              
        return list(result_bank.keys())
                
        
        
#from PolicyQueryModule.privacy_policy_keywords import PRIVACY_POLICY_KEY_PHRASES  
#Example
#was = WASDataCleaner('tester',PRIVACY_POLICY_KEY_PHRASES,'./BUG/','./Errors/', False)
#was.load_success("../../DataStorageModule/DataCleanerModule/Testing/pps-WAS-results-08_42PM-on-December-01.json",'test')
        
        
