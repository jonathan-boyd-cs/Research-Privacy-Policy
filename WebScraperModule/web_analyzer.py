#!/usr/bin/env python3
"""
    Class works to further conceal the complexities of the WebScraper and PhraseScraper, functioning
    by allowing queries for the presencs of text on a page, and providing a default dynamic
    analysis of a web url provided accessory information.

"""

import sys
sys.path.append('../')
from WebScraperModule.phrase_scraper import PhraseScraper
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from FileManager.file_manager import FileManager
from typing import Iterable, List

class WebAnalyzer(PhraseScraper):
    def __init__(self, name : str, outputDirectory : str, errLogDirectory : str, headless : bool , slow_mo : int ,  
                 policy_link_keywords : dict, policy_key_phrases : dict, url : str =None, verbose : bool =True) -> None:
        super().__init__(name,outputDirectory, errLogDirectory, headless,slow_mo,
                         policy_link_keywords,
                         policy_key_phrases, verbose)
        self.__name = name
        self.__url = url
        m = time_stamped_msg("web-analyzer-{}".format(name))
        self.__outputDirectory = outputDirectory
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))
        self.__verbose = verbose
        self.__file_manager = FileManager(self.__name,verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
        
    def set_url(self,url : str) -> None:
        """
            Required prior to functionality
        """
        self.__url = url
        maybe_print(self.__verbose, '(WebAnalyzer) url set to...{}'.format(url))
    
    def get_url(self) -> str:
        return self.__url
    
    
    def is_present(self, keywords : Iterable[str]) -> bool:
        """
            Method checks if the provided keywords are present at the url set for the WebAnalyzer instance.
        """
        if self.__url == None:
            maybe_print(self.__verbose, "(WebAnalyzer) must set url first...exiting with None...")
            return None
        try:
            
            maybe_print(self.__verbose, "(WebAnalyzer) checking for text presence at url...{}".format(self.__url))
            present = self.has_text(self.__url,keywords)
            maybe_print(self.__verbose, "(WebAnalyzer) url {} the text content on its page.".format(
                'has' if present else 'does not have'
            ))
            return present
        except Exception as e:
            m = "(WebAnalyzer) unexpected error accessing url in text presence analysis...\nerror --> {}".format(str(e))
            self.__err_database.add(self.__url,m)
            
            maybe_print(self.__verbose, m)
            raise Exception(e)

    def run_web_analysis(self):
        if self.__url == None:
            maybe_print(self.__verbose, "(WebAnalyzer) must set url first...exiting with None...")
            return None
        try:
            links = self.get_links(self.__url,self.get_link_keywords())
            if not bool(links):
                maybe_print(self.__verbose, "(WebAnalyzer) failed to capture web links for  url...{}...aborting.".format(self.__url))
                raise Exception("(WebAnalyzer) Failed to capture links")
            result_location = self.analyze_phrase_information_per_link(
                self.__url, links, self.default_routine, 
                [self.__url,self.__name,self.__outputDirectory]
            )
            maybe_print(self.__verbose, "(WebAnalyzer) results of web analysis located at... {}".format(result_location))
            
            return result_location
        except Exception as e:
            m = "(WebAnalyzer) unexpected error in web analysis...\nerror --> {}".format(str(e))
            self.__err_database.add(self.__url,m)
            
            maybe_print(self.__verbose, m)
            raise Exception(e)

#from privacy_link_key_phrases import PRIVACY_LINK_KEYWORDS, PRIVACY_DNSMI_LINK_KEY_PHRASES
#from testing import PRIVACY_POLICY_KEY_PHRASES 
# Example
#url = 'https://google.com'
#pa = WebAnalyzer('policy-analyzer',"../OutputFiles/ScraperResults/",'../OutputFiles/Errors/',False,0,
#                            PRIVACY_LINK_KEYWORDS, PRIVACY_POLICY_KEY_PHRASES, url, True)
#print(pa.is_present(PRIVACY_DNSMI_LINK_KEY_PHRASES))
#file = pa.run_web_analysis()
#print(file)