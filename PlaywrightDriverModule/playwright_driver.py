#!/usr/bin/env python3
"""`
    Class manages all technical details associated with instantiating
    a syncronous playwright browser and handles all
"""

import sys
sys.path.append('../')
from playwright.sync_api import sync_playwright
from PlaywrightDriverModule.page_manager import PageManager
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from PlaywrightDriverModule.page_manager import Page

class PlaywrightManager:
    def __init__(self, name :str, errLogDirectory :str, headless : bool, slow_mo=0, verbose=True) -> None:
        self.__playwright = sync_playwright().start()
        self.__browser = self.__playwright.chromium.launch(
            headless=headless, slow_mo=slow_mo)
        #self.__browser = browser.new_context( user_agent=
        #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        #)
        #self.__browser.set_default_timeout(120000)
        #self.__browser = self.__playwright.chromium.launch(
        #    headless=headless, slow_mo=slow_mo
        #)
        self.__page_manager = PageManager(name, errLogDirectory, self.__browser, verbose)
        m = time_stamped_msg("playwright-manager-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))
        self.__verbose = verbose
        self.__name = name
        
    def __del__(self):
        try:
            self.browser.close()
        except Exception as e:
            pass
        try:
            self.__playwright.stop()
        except Exception as e:
            pass
        
    def new_page(self, id : str) -> None:
        """
            Create a new Chromium browser Page object associated with the provided
            id.
        """
        try:
            self.__page_manager.new_page(id)
        except Exception as e:
            m = "(PlaywrightManager) failed to create page under id {}...\nerror --> {}".format(id,str(e))
            self.__err_database.add(id,m)
                
                
            maybe_print(self.__verbose, m)
            raise Exception(e)
    
    
    def get_page(self,id : str) -> Page:
        """
            Returns an encapsulated Chromium browser Page object.
        """
        try:
            page = self.__page_manager.get_page(id)
            return page
        except Exception as e:
            m = "(PlaywrightManager) failed to get page under id {}...\nerror --> {}".format(id,str(e))
            self.__err_database.add(id,m)
                
                
            maybe_print(self.__verbose, m)
            raise Exception(e)
    
    def has_visited(self, page_id : str, url : str) -> bool:
        """
            Returns true if a page has visited a provided url
        """
        try:
            return self.__page_manager.has_visited(page_id,url)
        except Exception as e:
            m = "(PlaywrightManager) failed to confirm visit history for page under id {} agaisnt {}...\nerror --> {}".\
                format(page_id,url,str(e))
            self.__err_database.add(page_id,m)
                
                
            maybe_print(self.__verbose, m)
            raise Exception(e)
    
    def remember_current_url(self, page_id :str, tag : str) -> None:
        """
            Will store the current url for the specified page id, under
            the alias of the provided tag.
        """
        try:
            self.__page_manager.remember(page_id,tag)
        except Exception as e:
            m = "(PlaywrightManager) failed to store current url for page under {} against {}...\nerror --> {}".\
                format(page_id,tag,str(e))
            self.__err_database.add(page_id,m)
                
                
            maybe_print(self.__verbose, m)
            raise Exception(e)
        
    def return_to_url(self, page_id : str, tag : str) -> None:
        """
            Attempts to restore the page associated with the 
            specified ID to the url stored under the provided tag
            for that page.
        """
        try:
            self.__page_manager.restore(page_id,tag)
        except Exception as e:
            m = "(PlaywrightManager) failed to return to url for page under id {} against {}...\nerror --> {}".\
                format(page_id,tag,str(e))
            self.__err_database.add(page_id,m)
                
                
            maybe_print(self.__verbose, m)
            raise Exception(e)
        
        
    def return_to_previous_url(self, page_id : str) -> None:
        """
            Attempts to restore the specified page to its prior url
        """
        try:
            self.__page_manager.back(page_id)
        except Exception as e:
            m = "(PlaywrightManager) failed to return to previous url for page under id {}...\nerror --> {}".format(page_id,str(e))
            self.__err_database.add(page_id,m)
                
                
            maybe_print(self.__verbose, m)
            raise Exception(e)
    
    def visit(self, page_id : str, url : str) -> None:
        """
            Sends the specified page to the provided url.
        
        """
        try:
            if not self.__page_manager.has(page_id):
                self.__page_manager.new_page(page_id)
            self.__page_manager.goto(page_id,url)
        except Exception as e:
            m = "(PlaywrightManager) failed to visit url for page under id {}, tried : {}...\nerror --> {}".\
                format(page_id,url,e)
            self.__err_database.add(page_id,m)
                
                
            maybe_print(self.__verbose, m)
            raise Exception(e)
    
    def click(self,page_id, button):
        """
            Performs the page click functionality while first
            remembering the pages present url.
        """
        try:
            self.remember_current_url(page_id,"previous")
            button.click()
        except Exception as e:
            m = "(PlaywrightManager) failed to perform button click for page under id {}...\nerror --> {}".format(page_id,str(e))
            self.__err_database.add(page_id,m)
                
                
            maybe_print(self.__verbose, m)
            raise Exception(e)
    
    def  reboot_session(self, headless, slow_mo = 0):
        """
            Attempt to recover a playwright session by reinstantiating a browser
        """
        try:
            self.__page_manager.flush()
            
            if self.__browser != None:
                self.__browser.close()
            
            if self.__playwright != None:
                self.__playwright.stop()
                
            self.__playwright = sync_playwright().start()
            #browser = self.__playwright.chromium.launch(
            #    headless=headless, slow_mo=slow_mo)
            #self.__browser = browser.new_context( user_agent=
            #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            #)
            self.__browser = self.__playwright.chromium.launch(headless = headless, slow_mo=slow_mo)
            self.__page_manager.set_browser(self.__browser)
        except Exception as e:
            m = "(PlaywrightManager) failed to reboot...\nerror --> {}".format(str(e))
            self.__err_database.add(self.__name,m)
                
                
            maybe_print(self.__verbose, m)
            raise Exception(e)

# Example
# pm = PlaywrightManager('pm','./',False,5000,True)
# pm.new_page("HOME")
# pm.visit("HOME","https://google.com")
# pm.reboot_session(False, 3000)
# pm.new_page("DOG")
# pm.visit("DOG","https://youtube.com")
# pm.visit("DOG", "https://google.com")
# pm.return_to_previous_url("DOG")
# pm.remember_current_url("DOG","BAGEL")
# pm.visit("DOG", "https://wikipedia.com")
# pm.return_to_url("DOG","BAGEL")