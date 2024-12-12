#!/usr/bin/env python3
"""

    Class functions to compartmentalize components of the web scraper, allowing focus on the functionality of
    seeking phrases, rather than the details of working with playwright.
"""

import sys
sys.path.append('../')
import copy
from DataStorageModule.WebScraperStorageModule.scraper_database import ScraperDatabase
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from WebScraperModule.web_scraper import WebScraper
from ErrorHandleModule.errors import err_msg_tagged_details
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from FileManager.file_manager import FileManager
from typing import Iterable, Callable, List
import json

class PhraseScraper(WebScraper):
    def __init__(self, name : str, outputDirectory : str, errLogDirectory : str, headless : bool , 
                 slow_mo : int, link_keywords : Iterable[str] =None,phrase_keywords : Iterable[str] =None,
                 verbose=True):
        super().__init__(name, errLogDirectory,headless,slow_mo, verbose)
        self.__name = name
        self.__link_keywords = link_keywords
        self.__queries = phrase_keywords
        self.__query_database = ScraperDatabase()
        m = time_stamped_msg("phrase-scraper-{}".format(name))
        self.__err_database = ErrorDatabase("{}/{}.txt".format(errLogDirectory,m))
        self.__current_url = None
        self.new_page(self.__name)
        self.__verbose = verbose
        self.__outputDirectory = outputDirectory
        self.__file_manager = FileManager(self.__name,verbose)
        self.__file_manager.assure_directory(outputDirectory)
        self.__file_manager.assure_directory(errLogDirectory)
    
    def store_link_keywords(self, keywords):
        self.__link_keywords = keywords
        
    def store_phrase_bank(self, phrases):
        self.__queries = phrases
        
    def get_link_keywords(self):
        return self.__link_keywords
    
    def get_phrase_bank(self):
        return self.__queries
    
    def has_text(self, url : str, text_phrase_list : str) -> bool:
        try:
            if not url == self.__current_url:
                self.visit(self.__name, url)
                self.__current_url = url
            page = self.get_page(self.__name)
            
            # Done to render the lower end of dynamic websites.
            page.page().mouse.wheel(0,500000)
            page.page().mouse.wheel(0,-500000)
            page.page().wait_for_load_state(state='load')
            
        except Exception as e:
            m = "(PhraseScraper) error in initial preparations in has text... error --> {}".format(str(e))
            self.__err_database.add("{}-{}".format(self.__name,url),m)

            maybe_print(self.__verbose, m)
            raise Exception(e)
        
        for var in text_phrase_list:
        
            try:
                maybe_print(self.__verbose, "(PhraseScraper) searching for...{}...on the url page.".format(var))
                result = self.find_text(page.id(),var)
                if result['count'] > 0:
                    maybe_print(self.__verbose, "(PhraseScraper) FOUND")
                    return True
                maybe_print(self.__verbose, "(PhraseScraper) NOT FOUND")
                
            except:
                maybe_print(self.__verbose, '(PhraseScraper) hit a snag... attempting recovery.')
                continue
        return False
        
        
    def get_links(self, url : str, link_keywords : Iterable[str] =None)-> dict:
        
        if link_keywords == None:
            link_keywords = self.__link_keywords
        if link_keywords == None:
            maybe_print(self.__verbose, "(PhraseScraper) no link keywords have been provided...\nStore link keywords or load with constructor.\nurl: {}".format(url))
            return None
        
        try:
            if not url == self.__current_url:
                self.visit(self.__name, url)
                self.__current_url = url
            page = self.get_page(self.__name)
        
        except Exception as e:
            m = "(PhraseScraper) error in initial preparations in get links... error --> {}".format(str(e))
            self.__err_database.add("{}-{}".format(self.__name,url),m)

            maybe_print(self.__verbose, m)
            raise Exception(e)
        
        links = {}
        maybe_print(self.__verbose, "(PhraseScraper) BEGINNING LINK SEARCH ON {}".format(url))
        try:
            page.page().mouse.wheel(0,100000)
            page.page().mouse.wheel(0,-100000)
            page.page().wait_for_load_state(state='load')
        
        except Exception as e:
            m = "(PhraseScraper) error in page scroll... error --> {}".format(str(e))
            self.__err_database.add("{}-{}".format(self.__name,url),m)
            maybe_print(self.__verbose, str(e))
            raise(e)
        
        for i in range(2):
            for key in link_keywords:
                maybe_print(self.__verbose, "(PhraseScraper) trying {}".format(key))
                try:
                    link_s = self.grab(page,"link",key)

                    if not self.is_null(link_s):
                        links[key] = link_s
                        maybe_print(self.__verbose, "(PhraseScraper) a hit!")
                
                except KeyboardInterrupt:
                    sys.exit()
                
                except Exception as e:
                    err = err_msg_tagged_details("(PhraseScraper) links error",self.get_num_queries(),[page.id(),url,str(e)])
                    self.__err_database.add(self.get_num_queries(),err)
                    continue
            
            if bool(links):
                break
                    
        maybe_print(self.__verbose, "(PhraseScraper) END LINK SEARCH")
        return links
    
    def analyze_phrase_information_per_link(self, url : str, playwright_links : Iterable[object], routine : Callable, args_list : List[any]):
        try:
            if not url == self.__current_url:
                self.visit(self.__name, url)
                self.__current_url = url
            page = self.get_page(self.__name)
        except Exception as e:
            m = "(PhraseScraper) error in initial preparations in analyze phrase information per link... error --> {}".format(str(e))
            self.__err_database.add("{}-{}".format(self.__name,url),m)

            maybe_print(self.__verbose, m)
            raise Exception(e)
        
        maybe_print(self.__verbose, "(PhraseScraper) BEGINNING PHRASE ANALYSIS")
        
        i = 0
        for key in playwright_links:
            try:
                result = self.multi_link_iteration(playwright_links[key],page,routine,args_list)
                if bool(result):
                    self.__query_database.add((url),result)
            except Exception as e:
                m = "(PhraseScraper) error in playwright multi link handling on ({})... error --> {}".format(key,str(e))
                self.__err_database.add("{}-{}".format(self.__name,url),m)

                maybe_print(self.__verbose, m)
                continue
            
        maybe_print(self.__verbose, "(PhraseScraper) END PHRASE ANALYSIS")
        m = time_stamped_msg("analysis-{}".format(self.__name))
        outfile = "{}{}.json".format(self.__outputDirectory, m)
        self.__query_database.to_json_id(url, outfile)
        return outfile
        
    def default_routine(self,url, page_id, outDirectory):
        outfile_prefix = "{}{}".format(outDirectory,page_id)
        outfile = time_stamped_msg("phrase_analysis")
        _outfile = '{}-{}.json'.format(outfile_prefix,outfile)
        phrase_data = copy.deepcopy(self.__queries)
        page = self.get_page(page_id)
        maybe_print(self.__verbose, "\n(PhraseScraper) ON A NEW WEBPAGE\n: {}\nFOR ROUTINE...".format(page.page().url))
        
        try:
            for key in phrase_data:
                maybe_print(self.__verbose, "(PhraseScraper) TOP LEVEL AT: {}".format(key))
                
                self.dfs_helper(phrase_data[key],key, phrase_data, self.phrase_analysis)
                # Populates the nodes of the provided phrases queries heirarchical tree with
                # resutls corresponding to the website attended.
            
            # store a personalized copy of the tree with data corresponding to the url.
            with open(_outfile, "w") as f:
                json.dump({url:phrase_data},f)
            
            return phrase_data
        
        except Exception as e:
            m = "(PhraseScraper) error in default routine on ({})... error --> {}".format(url,str(e))
            self.__err_database.add("{}-{}".format(self.__name,url),m)

            maybe_print(self.__verbose, m)
            raise Exception(e)
            
    def dfs_helper(self, current, key, previous, act):
        """
            Diver traverses a heirarchical tree to a node, where it acts on the that segments key.
        """
        try:
            if current == 0:
                maybe_print(self.__verbose, "(PhraseScraper) AT LEAF... SEARCHING FOR {} IN WEBPAGE...".format(key))
                act(previous, key)
                return
            for key in current:
                maybe_print(self.__verbose, "(PhraseScraper) SUB LEVEL AT: {}".format(key))
                self.dfs_helper(current[key],key,current,act)
        except Exception as e:
            m = "(PhraseScraper) error in default routine's dfs helper ({})... error --> {}".format(key,str(e))
            self.__err_database.add("{}-{}".format(self.__name,key),m)

            maybe_print(self.__verbose, m)     
            raise Exception(e)   
           
    def phrase_analysis(self, result_container, phrase):
        try:
            data = self.find_text(self.__name,phrase)
            if data == None:
                result_container[phrase] = {}
                maybe_print(self.__verbose, "(PhraseScraper) miscellaneous error in find text through phrase scraper for...{}".\
                    format(phrase))
                return
            maybe_print(self.__verbose, "{} --> {}".format(data["count"],phrase))

            result_container[phrase] = data
    
        except Exception as e:
            m = "(PhraseScraper) miscellaneous error in phrase phrase analysis through policy scraper for...{}\n \
            error -->{}".format(phrase,str(e) )
            self.__err_database.add("{}-{}".format(self.__name,phrase),m)

            maybe_print(self.__verbose, m)
            raise Exception(e)        
        
        
        
        
        
        
# Example 
#sys.path.append('../PolicyQueryModule')  
#from privacy_link_key_phrases import PRIVACY_LINK_KEYWORDS, PRIVACY_DNSMI_LINK_KEY_PHRASES
#from testing import PRIVACY_POLICY_KEY_PHRASES        
#name = 'scraper'
#ps = PhraseScraper(name, './','./',False, 0, PRIVACY_LINK_KEYWORDS,PRIVACY_POLICY_KEY_PHRASES, False)
#url = "https://ru.search.yahoo.com/"
#links = ps.get_links(url)
#ps.analyze_phrase_information_per_link(url,links,ps.default_routine,[url,name,"../OutputFiles/ScraperResults"])
#ps.save_err_state("testing")