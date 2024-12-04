#!/usr/bin/env python3

"""
    Main driver of the scraper codebase... a simplification of the scraper
    functionality, providing a template to perform web analysis through search
    queries for links and text. The output of the run_default_routine command can be 
    fed through the WASManager pipeline to produce a CSV file.
    
    The web_link_keywords will inform the WAS what links to seek for traversal to the primary sites of analysis.
    That is, the WAS expects to be placed on a particular page, followed by navigating through links to otehr pages and performing its
    analysis.
    
    The web_text_key_phrases dictionary is expected to be a heirarchical python dictionary tree. The WAS will traverse this structure, producing
    statistical details on the number of successful queries at each level, which can be viewed after the output is fed through the pipeline.
    
    The pipeline allows for specification of the desired depth associated with total calculations. Passing the lowest heirarchical index+1 will lead the
    WAS cleaners to provide information on the count of successful queries at each heirarchical level.
    
    The websites list expects websites to be pulled from the website dictionary associated with the scrape run. This can be done through the
    WASManager, which will pull the websites by provided top level keys. A lower level pull has not yet been implemented. The dictionary structure of the
    websites still much remain in tact for the WAS cleaning pipeline to CSV.
    
    Be sure to write down and save the name you prescribe to your WAS run. See WASManager for details on why this is important.

"""


import sys
sys.path.append('../')
from FileManager.file_manager import FileManager
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from DataStorageModule.WebScraperStorageModule.analysis_suite_database import AnalysisSuiteDatabase
from WebScraperModule.web_analyzer import WebAnalyzer
from typing import List
import json

class WebAnalysisSuite(WebAnalyzer):
    def __init__(self, name : str, outputDirectory : str, errLogDirectory : str, headless : bool, slow_mo : bool,  
                 web_link_keywords : dict, web_text_key_phrases : dict, websites : List[str] =None, verbose : bool =True) -> None:
        super().__init__(name,outputDirectory, errLogDirectory, headless,slow_mo,
                         web_link_keywords,
                         web_text_key_phrases, None,verbose)
        self.__name = name
        self.__websites = websites 
        m = time_stamped_msg("web-analysis-suite-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))
        self.__verbose = verbose
        self.__result_bank = AnalysisSuiteDatabase(name,errLogDirectory)
        self.__outputDirectory = outputDirectory
        self.__file_manager = FileManager(self.__name,verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
        
        
        
    def url_to_file_safe(self, url : str) -> str:
        web_name = str(url)
        web_name = web_name.replace('.','_')
        web_name = web_name.replace('/','_')
        web_name = web_name.replace(':','_')   
        return web_name.strip()
        
    def set_websites(self, websites_list) -> None:
        """
            Dynamically change the WAS's website dictionary
        """
        self.__websites = websites_list
        
    def get_websites(self):
        return self.__websites
        
    def run_default_routine(self, accessory_has_text : List[dict] = None):
        """
            See class summary
            accessory_has_text expects a list of dictionaries. The required format is...
            [{
                'name': <name you prescribe to query>,
                'values': <the iterable list of phrases to search for>
            }]
        """
        for website in self.__websites:
            # format to be passed down the cleaning pipeline.
            result = {'main':{},
                    'accessory':{}}
            self.set_url(website)
            try:
                if accessory_has_text != None:
                    for job in accessory_has_text:
                        text_keywords = job['values']
                        out = self.is_present(text_keywords)
                        result['accessory'][job['name']] = out
            except KeyboardInterrupt:
                        sys.exit()
            
            except Exception as e:
                m = "(WebAnalysisSuite) unexpected error in processing accessory has_text parameters ({})...\nerror --> {}".format(website,str(e))
                self.__err_database.add(website,m)
            
                maybe_print(self.__verbose, m)
                
                
            try:
                # main analysis
                out_file_name = self.run_web_analysis()
            
            except KeyboardInterrupt:
                        sys.exit()
            
            except Exception as e:
                m = "(WebAnalysisSuite) unexpected error in main web analysis ({})...\nerror --> {}".format(website,str(e))
                self.__err_database.add(website,m)
            
                maybe_print(self.__verbose, m)
                self.__result_bank.add(website,{'error':str(e)},'unsuccessful')
                continue
            try:
                # loads results and stores them in a common structure for later cleaning.
                with open(out_file_name, 'r') as f:
                    data = json.load(f)
                    result['main'] = data
                    
                web_name = self.url_to_file_safe(website)
                filename = "{}WAS-{}-{}.json".format(self.__outputDirectory, self.__name,web_name)
                self.__file_manager.copy_rename(out_file_name, filename)
            
            except KeyboardInterrupt:
                        sys.exit()
            
            except Exception as e:
                m = "(WebAnalysisSuite) unexpected error in file management post web analysis ({})...\nerror --> {}".format(website,str(e))
                self.__err_database.add(website,m)
            
                maybe_print(self.__verbose, m)
                continue            
            try:
                # place this result in the 'successful bin'
                self.__result_bank.add(website,result,'successful')
                m = time_stamped_msg("save-state")
                filename = "{}intermediate/{}-intermediate.json".format(self.__outputDirectory,
                                                              web_name,m)
                self.__file_manager.assure_directory(filename)
                with open(filename, 'w') as f:
                    json.dump(result,f)
            
            except KeyboardInterrupt:
                        sys.exit()
            except Exception as e:
                m = "(WebAnalysisSuite) unexpected error storing web analysis results in database ({})...\nerror --> {}".format(website,str(e))
                self.__err_database.add(website,m)
            
                maybe_print(self.__verbose, m)
                continue
                
        try:
            m = time_stamped_msg("{}-WAS-results".format(self.__name))
            out = "{}{}.json".format(self.__outputDirectory,m)
            self.__result_bank.save(out)
            
        except Exception as e:
                m = "(WebAnalysisSuite) unexpected error while saving final results ({})...\nerror --> {}".format(website,str(e))
                self.__err_database.add(self.__name,m)
            
                maybe_print(self.__verbose, m)
                raise Exception(e)
            
    


# Example
#from PolicyQueryModule.privacy_link_key_phrases import PRIVACY_LINK_KEYWORDS, PRIVACY_DNSMI_LINK_KEY_PHRASES
#from PolicyQueryModule.testing import PRIVACY_POLICY_KEY_PHRASES#
#
#pas = WebAnalysisSuite('PAS','../OutputFiles/WAS/ROUTINE/', '../OutputFiles/Errors/WAS/',
#                          False, 0, PRIVACY_LINK_KEYWORDS,PRIVACY_POLICY_KEY_PHRASES,
#                          [
#                           'https://games.yahoo.co.jp/',
#                            'https://yahoo.com',
#                            "https://ru.search.yahoo.com/",
#                           #'https://github.com',
#                           ], True)
#print(pas.get_websites())
#pas.run_default_routine(
#    [   
#     {
#            'name': 'dnsmi',
#            'values':PRIVACY_DNSMI_LINK_KEY_PHRASES
#        }
#    ]
#)
