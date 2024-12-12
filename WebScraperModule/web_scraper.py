#!/usr/bin/env python3

"""
    Primary web scraper of the codebase, responsible for all playwright queries.

"""

import sys
sys.path.append('../')
from FileManager.file_manager import FileManager
from ErrorHandleModule.errors import err_msg_tagged_details
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from PlaywrightDriverModule.playwright_driver import PlaywrightManager
from TranslationModule.translation_unit import WebTranslationUnit
from DataStorageModule.WebScraperStorageModule.page_database import PageDatabase
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from WebScraperModule.scrape_location import ScrapeLocation
from playwright.sync_api import expect
from PlaywrightDriverModule.page_manager import Page

import re
from typing import List , Callable

class WebScraper(PlaywrightManager):
    """
        Scraper and playwright manager, handling all complications of creating a playwright environment and
        performing specified queries on webpages.
    """
    def __init__(self, name : str, errLogDirectory : str, headless : bool, slow_mo : int, verbose=True) -> None:
        super().__init__(name, errLogDirectory, headless,slow_mo, verbose)
        self.__translation_unit = WebTranslationUnit(self,'web-scrape-translator',errLogDirectory,verbose)
        self.__database = PageDatabase()
        m  = time_stamped_msg("web-scraper-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))        
        self.__subjects = 0        
        self.__queries = 0
        self.__verbose = verbose
        self.__file_manager = FileManager(name,verbose)
        self.__file_manager.assure_directory(errLogDirectory)  
          
    
    
    def get_num_subjects(self) -> int:
        return self.__subjects
    
    def get_num_queries(self) -> int:
        return self.__queries
    
    def translate(self,text,to) -> List[str]:
        text_ = self.__translation_unit.translate(text,to)
        return text_
            
    def get_language(self, page : Page) -> str:
        """ 
            Works to retrieve the language associated with a given page url.
        """
        maybe_print(self.__verbose,"(WebScraper) getting page language...")
        url = page.page().url
        self.check(url)
        location = self.__database.get(url)
        lang = location.get_language()
        return lang
        
    def check(self, url : str) -> None:
        """
            Ensures that the provided url is accounted for in the database, storing its 
            associated language.
        
        """
        try:
            maybe_print(self.__verbose,"(WebScraper) check point reached for page...")

            if not self.__database.has(url):
                self.__database.add(url,
                        ScrapeLocation(url))
                self.__subjects += 1
                
            location = self.__database.get(url)
            if location.get_language() == None:
                lang = self.__translation_unit.detect_lang_webpage(url)
                location.set_language(lang)
        except Exception as e:
            m = "(WebScraper) unknown error in check protocol...\nerror --> {}".format(str(e))
            self.__err_database.add(self.__queries,m)

            maybe_print(self.__verbose, m)
            raise Exception(e)
      
    def chart_data(self, page_id : str, data : object, tag : str) -> None:
        """
            Stores information about a url associated with the provided page id and
            charts data under the tag name at that url's metadata storage point
        """
        page = self.get_page(page_id)
        location = self.__database.get(page.page().url)
        if location != None: 
            location.set_data(tag,data)
    
    def locate(self, page_id : str, html_tag : str, class_list= None, 
               id_list = None, attributes_list = None) -> object:
        """
            Implementation of the locator method of playwright sync api for python
        """
        
        try:
            page = self.get_page(page_id)
            if page == None: 
                return None
            

                
            self.check(page.page().url)
            
            #build the query per playwright specifications
            query = html_tag.strip()
            if class_list != None:
                classes = ".".join([x.strip() for x in class_list])
                query += ".{}".format(classes)
            
            if id_list != None:
                ids = "#".join([x.strip() for x in id_list])
                query += "#{}".format(ids)

            if attributes_list != None:
                query += "{}".str(attributes_list)
                
        except Exception as e:
            err = err_msg_tagged_details("locate--> {}".format(str(e)),
                                page_id,
                                [html_tag,class_list,id_list,attributes_list])
            m = "(WebScraper) unknown error during initial preparations in locate...\n{}...\nerror -> {}".format(err,str(e))
            self.__err_database.add(self.__queries,m)
                
            maybe_print(self.__verbose, m)
            raise Exception(e)
        try:
            self.__queries += 1
            result = page.page().locator(query)
            
            self.chart_data(page.id(),
                            result, self.__queries)
            return result
        except Exception as e:
            err = err_msg_tagged_details("(WebScraper) locate error...\nerror --> {}".format(str(e)),
                                  page_id,
                                  [html_tag,class_list,id_list,attributes_list])
            self.__err_database.add(self.__queries,err)
            raise Exception(e)
        
    
    
    def grab(self, page : Page, role : str, text : str) -> object:
        """
            Implements the playwright get by role functionality
            on the specified Page object. That is... the page_manager.py Page
        """
        if page == None:
            return None
        

        try:
            
            self.__queries += 1
            maybe_print(self.__verbose,"(WebScraper) attempting to grab {} via {}".format(role,text))
            result = None
            if text == None:
                result = page.page().get_by_role(role)
            else:
                lang = self.get_language(page)
                if lang != 'en':
                    text = self.translate(text,lang)
                    maybe_print(self.__verbose,"(WebScraper) translated text to {}".format(lang))

                else:
                    # enveloped in a list structure for congruence with the transate output
                    text = [text]
                for var in (text):  
                    maybe_print(self.__verbose,"(WebScraper) attempting to get {} via {}".format(role,var))
                    result = page.page().get_by_role(role,name=str(var))
                    if not self.is_null(result):
                        maybe_print(self.__verbose,"(WebScraper) attempt successful")
                        break
        
        except KeyboardInterrupt:
            sys.exit()
        
        except Exception as e:
            err = err_msg_tagged_details("grab-->{}".format(str(e)),page.id(), [role, text])
            self.__err_database.add(self.__queries, err)
            raise Exception(e)
        
        self.chart_data(page.id(),
                            result, self.__queries)
        return result
        
    
    def is_null(self, result_obj : object) -> bool:
        """
            Method is utilized to determine if a playwright query resultant object is empty
        """
        try:
            expect(result_obj).not_to_have_count(count=0, timeout=3000)
            return False
        except:
            return True
    
    def num_elements(self, result_obj : object) -> int:
        """
            Report the number of items in a playwright locator return structure.
        """
        try:
            return result_obj.count()
        except:
            return 0
        
    def get_text(self, result_obj : object, lang='en') -> List[dict]:
        """
            Extracts the text contents from a locator query result.
            Ensures return values are in English
        """
        text = []
        try:
            if self.is_null(result_obj):
                return {}
            i = 0
            for var in result_obj.all():
                t = var.text_content()
                if lang != 'en':
                    t = self.translate(t,'en')
                text.append({i:t})
                i += 1
            return text
        
        except KeyboardInterrupt:
            sys.exit()
        
        except Exception as e:
            err = err_msg_tagged_details("(WebScraper) get_text error...\nerror -->{}".format(str(e)),self.__queries, [lang,text])
            self.__err_database.add(self.__queries, err)
            raise Exception(e)
    
   
    
    def find_text(self, page_id : str, text : str) -> dict:
        """
            Seeks occurance of key phrases or text on a page associated with the provided ID.
            Returns the entire text associated with the discovered key as well as a count of the number
            of occurances.
        """
        try:
            page = self.get_page(page_id)
        except Exception as e:
            m = "(WebScraper) unknown error in retrieving page...\nerror --> {}".format(str(e))
            self.__err_database.add(self.__queries,m)

            maybe_print(self.__verbose, m)
            raise Exception(e)
        
        if page == None:
            return None
        
        text_results = {'text':{},'count':0}
        
        try:
            
            lang = self.get_language(page)
            if lang != 'en':
                text_ = self.translate(text,lang)
                maybe_print(self.__verbose, "(WebScraper) translated to {}".format(lang))

            else:
                # convert to list for conformity with translate output.
                text_ = [text]
            for var in text_:
                query = page.page().get_by_text(re.compile("{}[^a-zA-Z1-9]".format(var), re.IGNORECASE))
                    
                if not self.is_null(query):
                    text_results["count"] += query.count()  
                    maybe_print(self.__verbose, "(WebScraper) RESULT DISCOVERED as {}".format(var))

                                  
                t = self.get_text(query,lang)
                if bool(t) == True:
                    text_results['text'][var] = t

            tag = "find_text-{}".format(self.__queries)
            self.chart_data(page.id(),
                            text_results,tag)
            return text_results
        
        except KeyboardInterrupt:
            sys.exit()
        
        except Exception as e:
            m = "(WebScraper) error in find_text id: ({}) on...{}...\nerror --> {}".format(page_id,text,str(e))
            self.__err_database.add(self.__queries,m)

            maybe_print(self.__verbose, m)
            raise Exception(e)
            

    def multi_link_iteration(self,object : object, page : Page, routine : Callable, _args : list =None) -> dict:
        """
            Function takes (object) a locator result on links and traverses each link, running the provided (routine)
            action at the destination of each link before returning the results to the caller.
        """
        if page == None or object == None:
            return None
        results = {}
        
        i = 0
        page_id = page.id()
        for var in object.all():
            try:
                self.click(page.id(),var)
                tag = "multi-{}".format(page.page().url)
                if self.has_visited(page.id(),tag):
                    self.return_to_previous_url(page.id())
                    continue
                
                self.remember_current_url(page_id,tag)
            
            except KeyboardInterrupt:
                sys.exit()    
            
            except:
                continue
            try:
                r = None
                if _args != None:
                    r = routine(*_args)
                else:
                    r = routine(page)
                results['link-{}'.format(i)] = r
                i += 1

                self.return_to_previous_url(page.id())
            except:
                self.return_to_previous_url(page.id())
        try:
            tag = "multi-link-{}".format(self.__queries)
            self.chart_data(page.id(),
                            results,tag)
            return results
        except Exception as e:
            m = "(WebScraper) error in return from multi link iteration procedure...\nerror --> {}".format(str(e))
            self.__err_database.add(self.__queries,m)

            maybe_print(self.__verbose, m)
            raise Exception(e)
    
#Example
#ws = WebScraper('scraper','./',False,5000,True)
#ws.visit("origin","https://games.yahoo.co.jp/")
#r = ws.find_text("origin","Privacy")
#ws.save_err_state("test")
# page = ws.get_page("origin")
# r = ws.grab(page,"link","Privacy")
# ws.save_err_state("test")
# s = ws.multi_link_iteration(r,page,ws.find_text,["origin","Privacy"])    
# print(s)
# ws.save_err_state("test")