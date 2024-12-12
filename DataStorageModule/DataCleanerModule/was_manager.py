#!/usr/bin/env python3
"""
    Class serves to hide the complexity behind the WebAnalysisSuite's output and file generation.
    This class is meant to serve as an extension to the WAS, following a successful scrape routie.
    The clean() method of this class converts the WAS output to csv for visualizations.

"""
from typing import List, Callable
import json
import sys
sys.path.append('../../')
from DataStorageModule.DataCleanerModule.was_post_scrape_cleaner import WASDataCleaner
from DataStorageModule.DataCleanerModule.was_data_merger import WASDataMerger
from DataStorageModule.DataCleanerModule.was_text_processor import WASTextProcessor
from DataStorageModule.DataCleanerModule.was_finalization import WASFinalizer
from DataStorageModule.DataCleanerModule.was_text_numeric_transformer import WASTextTransformer
from FileManager.file_manager import FileManager
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from DataStorageModule.GraphicalStorageModule.was_csv_converter import WASToCSVConverter


class WASManager:
    """
    This class is meant to serve as an extension to the WAS, following a successful scrape routie.
    The clean() method of this class converts the WAS output to csv for visualizations.
    """
    def __init__(self, name : str, outputDirectory :str, errLogDirectory :str, phrase_legend : dict, subj_idx : int, columns : List[str] , web_src : dict, key_levels=1, verbose=True) -> None:
        self.__name = name
        self.__WASDC = WASDataCleaner(name, phrase_legend, outputDirectory, errLogDirectory, verbose)
        self.__WASDM = WASDataMerger(name, outputDirectory,errLogDirectory,verbose)
        self.__WASTP = WASTextProcessor(name, phrase_legend, outputDirectory, errLogDirectory, verbose)
        self.__WASTT = WASTextTransformer(name, outputDirectory, errLogDirectory, verbose)
        self.__WASF  = WASFinalizer(name, outputDirectory, errLogDirectory, verbose)
        self.__WASTCSV = None
        self.__file_manager = FileManager(name, errLogDirectory, verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
        m = time_stamped_msg(self.__name)
        m += ".txt"
        self.__err_database = ErrorDatabase(m)
        self.__outputDirectory = outputDirectory
        self.__errLogDirectory = errLogDirectory
        self.__verbose = verbose
        self.__columns = columns
        self.__subj_idx = subj_idx
        self.__web_src = web_src
        self.__key_levels = key_levels
        self.__exclusion_list = {}
        
    def is_url(self,s : str) -> bool:
        if type(s) == str:
            return (s[:5] == 'https')
        else:
            return False

    def url_to_file_safe(self, url : str) -> str:
        web_name = str(url)
        web_name = web_name.replace('.','_')
        web_name = web_name.replace('/','_')
        web_name = web_name.replace(':','_')   
        return web_name.strip()

    def __dfs_helper(self, current : dict, key : str, container : dict, condition_func : Callable) -> List[any]:
        """
            Serves as a diver, traversing until a condition is met. 
            In this implementation, the class seeks urls in the dictionary key heirarchy...
        """
        if condition_func(key):
            container += [key]
            return container
        else:
            assert(type(current) == dict)
            for k in current:
                c = self.__dfs_helper(
                                current         = current[k], 
                                key             =  k,
                                container       = [], 
                                condition_func  = condition_func
                )
                container.extend(c)
            return container

    def pull_urls(self, top_level_keys : List[str]) -> List[str]:
        """
            Retrieves url's from the stored class web_src, given the provided top level keys
        """
        websites = []
        for key in top_level_keys:
            if key in self.__web_src.keys():
                TARGET = self.__web_src[key]
                for sub_level in TARGET.keys():
                    websites += self.__dfs_helper(
                                    current   = TARGET[sub_level], 
                                    key       = sub_level, 
                                    container = [], 
                                    condition_func = self.is_url
                    )
        return [x for x in websites if x not in self.__exclusion_list]
                

    def merge_results(self, web_list_keys : List[str], directory : str, was_name : str,preexisting_results_files=[]) -> str:
        """
            Function loads results from the WAS default scrape routine in their intermediate state (url safe file names),
            while merging in any data from prexisting total WAS scrape output files. Serves as a failsafe in case the
            WAS doesn't complete its routine, or accessory data from a routine is lost due to a crash, causing incongruent data.
            (non aligned/mising data will be marked as N/A if not found in the preexisting result files)
            
            - The directory specifies the location of the preexisting partial (safe url) result files
            - The was_name parameter specifies the name of the WAS that produced the partial files... this is used 
                alongside the web_list_keys to reproduce the filenames in the specified directory
            - The preexisting result files object is meant to be a list of file names of fully complete WAS files.
        """
        websites = self.pull_urls(web_list_keys)
        return self.__manual_WAS_scrape_result_loader(
                        web_list  = websites, 
                        directory = directory, 
                        was_name  =  was_name, 
                        preexisting_results_files = preexisting_results_files
        )

    def __manual_WAS_scrape_result_loader(self, web_list : List[str], directory : str, was_name :str, preexisting_results_files=[]) -> str:
        save = {
            'successful': { 'results':{}},
            'unsuccessful': {}
            } # mimics structure of default WAS final output...
        i = 0
        for website in web_list:
            loaded = False
            web_name = self.url_to_file_safe(website)
            try:
                filename = "{}intermediate/{}-intermediate.json".format(directory, web_name)
                with open(filename, 'r') as f:
                    data = json.load(f)
                save['successful']['results'][website] = data    
                loaded = True
                i += 1
            
            except KeyboardInterrupt:
                sys.exit()
                        
            except Exception as e:
            
                if loaded:
                    continue
                
                try:
                    filename = "{}WAS-{}-{}.json".format(directory, was_name,web_name)
                    with open(filename, 'r') as f:
                        data = json.load(f)
                    
                    # further mimicing WAS final output structure...
                    d = {'main':data, 'accessory':{}}
                    save['successful']['results'][website] = d    
                
                
                except KeyboardInterrupt:
                    sys.exit()
                            
                except Exception as e:
                    m = "(WASManager)  error while loading file ({})...\nerror --> {}".format(filename,str(e))
                    self.__err_database.add(self.__name,m)    
                    maybe_print(self.__verbose,m)
                    continue
        
        # used to track which accesories may be missing from any given website scrape...
        accessories_store = {}
        for result_file in preexisting_results_files:
        
            try:
                with open(result_file, 'r') as f:
                    data = json.load(f)
                
                for result in data['unsuccessful']:
                    
                    if not result in save['unsuccessful']:
                        save['unsuccessful'][result] =  data['unsuccessful'][result]
                
                scrape_data = data['successful']['results']
                
                # Where save holds the data from the latest scrape, search for missing accessory data
                # in the provided preexisting files.
                for website in save['successful']['results']:
                    site = save['successful']['results'][website]
                    try:
                        assert(website in scrape_data)
                    
                    
                    except KeyboardInterrupt:
                        sys.exit()
                                    
                    except Exception as e:
                        continue
                    try:
                        assert('accessory' in scrape_data[website])
                    
                    except KeyboardInterrupt:
                        sys.exit()
                    
                    except Exception as e:
                        m = "(WASManager) {} does not posses accessories in the preexisting file ({})...\nerror --> {}".format(website,result_file,str(e))
                        self.__err_database.add(self.__name,m)    
                        maybe_print(self.__verbose,m)
                        continue
                    try:
                        if not 'accessory' in site:
                            site['accessory'] = {}

                        for accessory in scrape_data[website]['accessory']:
                            if not accessory in accessories_store:
                                accessories_store[accessory] = 'N/A'
                                
                            val = scrape_data[website]['accessory'][accessory]
                            site['accessory'][accessory] = val
                    
                    except KeyboardInterrupt:
                        sys.exit()
                    
                    except Exception as e:
                        m = "(WASManager) error acessing accessories ({})...\nerror --> {}".format(website,str(e))
                        self.__err_database.add(self.__name,m)    
                        maybe_print(self.__verbose,m)
                        raise (e)
            
                        
            except Exception as e:
                m = "(WASManager) error in handling a preexisting file ({})...\nerror --> {}".format(result_file,str(e))
                self.__err_database.add(self.__name,m)    
                maybe_print(self.__verbose,m)
                raise (e)
        
        # Check for accessories not found (N/A)
        for website in save['successful']['results']:
            site = save['successful']['results'][website]
            if not 'accessory' in site:
                site['accessory'] = {}
            for accessory in accessories_store:
                if not accessory in site['accessory']:
                    site['accessory'][accessory] = 'N/A'
    
        # saving results
        m = time_stamped_msg("{}-WAS-MERGED-results".format(was_name))
        out = "{}{}.json".format(self.__outputDirectory,m)
        with open(out,'w') as f:
            json.dump(save,f)
        return out

        
    def clean(self, post_scrape_WAS_datafile, out_tag):

        try:
            file = self.__WASDC.load_success(post_scrape_WAS_datafile,out_tag)
        except Exception as e:
            m = "(WASManager) unexpected error while running WASDataCleaner to process ({})...\nerror --> {}".format(
                out_tag,str(e))
            self.__err_database.add(self.__name,m)
            
            maybe_print(self.__verbose, m)
            raise Exception(e)
        
        try:
            file2 = self.__WASDM.merge(file,out_tag)
        except Exception as e:
            m = "(WASManager) unexpected error while running WASDataMerger to process ({})...\nerror --> {}".format(
                out_tag,str(e))
            self.__err_database.add(self.__name,m)
            
            maybe_print(self.__verbose, m)
            raise Exception(e)
            
        try:
            file3, file4 = self.__WASTP.process_merge_data(file2, out_tag)

        except Exception as e:
            m = "(WASManager) unexpected error while running WASTextProcessor to process ({})...\nerror --> {}".format(
                out_tag,str(e))
            self.__err_database.add(self.__name,m)
            
            maybe_print(self.__verbose, m)
            raise Exception(e)
        try:
            file5 = self.__WASTT.transform_WASTP_RS_file(file3, out_tag)
        except Exception as e:
            m = "(WASManager) unexpected error while running WATextTransformer to process ({})...\nerror --> {}".format(
                out_tag,str(e))
            self.__err_database.add(self.__name,m)
            
            maybe_print(self.__verbose, m)
            raise Exception(e)
        try:
            file6 = self.__WASF.WASTT_WASTP_merger(file5, file4, out_tag )
        except Exception as e:
            m = "(WASManager) unexpected error while running finalization process on ({})...\nerror --> {}".format(
                out_tag,str(e))
            self.__err_database.add(self.__name,m)
            
            maybe_print(self.__verbose, m)
            raise Exception(e)
        try:
            self.__WASTCSV = WASToCSVConverter(
                self.__name, file6, self.__columns, self.__web_src, self.__outputDirectory,
                self.__errLogDirectory, self.__verbose
            )
            self.__WASTCSV.run(self.__subj_idx,self.__key_levels)
            self.__WASTCSV.to_file(out_tag)
        except Exception as e:    
            m = "(WASManager) unexpected error while running WASToCSVConverter to process ({})...\nerror --> {}".format(
                out_tag,str(e))
            self.__err_database.add(self.__name,m)
            
            maybe_print(self.__verbose, m)
            raise Exception(e)

# Example
#import sys
#sys.path.append('../../')
#from PolicyQueryModule.privacy_policy_keywords import PRIVACY_POLICY_KEY_PHRASES
#from WebsiteGathering.Run1 import data
#from WebScraperModule.web_analysis_suite import WebAnalysisSuite
#from PolicyQueryModule.privacy_link_key_phrases import PRIVACY_LINK_KEYWORDS as PLK
#name = 'tester'
#out = './Testing/'
#log = './Testing/Log/'
#phrases = PRIVACY_POLICY_KEY_PHRASES

#subj_idx = 3
#columns = ['Industry', 'Country', 'State', 'URL']
#WASM = WASManager(name, out, log, phrases, subj_idx, columns, data)
#file = '../../crawler/saved_dnsmi_links/save1.json'
#WASM.clean(file,'testing')
