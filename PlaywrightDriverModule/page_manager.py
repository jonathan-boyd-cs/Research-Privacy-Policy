#!/usr/bin/env python3
"""
    Class handles the management of Playwright browser Page objects.

"""
import sys
from typing import KeysView
sys.path.append('../')
from DataStorageModule.WebScraperStorageModule.page_database import PageDatabase
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from PlaywrightDriverModule.url_manager import UrlManager
from playwright.sync_api import Browser
class Page:
    """
        Class serves as a container for playwright Page objects, tagging
        them with a provided ID.
    """
    def __init__(self,id,page):
        self.__id = id
        self.__page = page
    
    def id(self):
        return self.__id
    
    def page(self):
        return self.__page

class PageManager:
    """
        Class manages playwright Page objects, facilitating page 
        navigation, history management, and rememberance.
    """
    def __init__(self, name : str, errLogDirectory : str, browser : Browser, verbose=True) -> None:
        self.__browser = browser
        self.__pages = PageDatabase()
        m = time_stamped_msg("page-manager-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))
        self.__url_manager = UrlManager()
        self.__verbose = verbose

    def new_page(self, id : str) -> None:
        """
            Generates a new Playwright page and stores it in the
            PageManager database under the provided id.
        """
        page = self.__browser.new_page()
        page.set_default_timeout(90000)
        self.__pages.add(id.strip() ,Page(id.strip(),page))

    def has(self, id : str) -> bool:
        return self.__pages.has(id.strip())

    def get_page(self,page_id : str) -> Page:
        if self.__pages.has(page_id.strip()):
            return self.__pages.get(page_id.strip())

    def remove_page(self, page_id : str) -> None:
        if self.__pages.has(page_id.strip()):
            self.__pages.remove(page_id.strip())

    def goto(self, page_id : str, url : str) -> None:
        """
            Executes the goto Playwright browser chromium Page command for
            the page associated with the given id.
        """
        page = None
   
        if self.__pages.has(page_id.strip()):
            page = self.__pages.get(page_id.strip())
            
        if page != None:
            try:
                page.page().set_default_navigation_timeout(120000)
                self.__url_manager.set("previous-{}".format(page_id.strip()) ,page.page().url)
                page.page().goto(url, wait_until='domcontentloaded')
                self.__url_manager.set("current-{}".format(page_id.strip()) , page.page().url)
            except Exception as e:
                m = "(PageManager) failed to go to page {}...\nerror --> {}".format(url,str(e))
                self.__err_database.add(page_id,m)
                
                
                maybe_print(self.__verbose, m)
                raise Exception(e)

    def set_browser(self, browser : Browser) -> None:
        self.__browser = browser

    def get_browser(self) -> Browser:
        return self.__browser

    def flush(self) -> None:
        """
            Closes and unremembers all Page objects in its database.
        """
        for page in self.__pages:
            try:
                page.page().close()
            except:
                continue
        self.__pages.flush()
        self.__browser = None

    def get_pages(self) -> KeysView:
        """
            Returns a key list of all pages stored in the database
        """
        return self.__pages.keys()
    
    def remember(self, page_id : str, tag : str) -> None:
        """
            Stores the specified Page object's current url under the
            tag name provided.
        """
        page = None
        if self.__pages.has(page_id.strip()):
            page = self.__pages.get(page_id.strip())
        
        if page != None:
            try:
                self.__url_manager.set("{}-{}".format(tag,page_id.strip()), page.page().url)
            except Exception as e:
                m = "(PageManager) unknown error remembering...\nerror --> {}".format(str(e))
                self.__err_database.add(page_id,m)
                
                maybe_print(self.__verbose, m)
                raise Exception(e)
    
    def has_visited(self,page_id : str,url : str) -> bool:
        """
            Utilizies the PageManager UrlDatabase to confirm whether the
            page under a given ID has visited a particular URL
        """
        page = None
        if self.__pages.has(page_id.strip()):
            page = self.__pages.get(page_id.strip())
        
        if page != None:
            try:
                key = "{}-{}".format(url,page_id.strip())
                return self.__url_manager.has(key)
            except Exception as e:
                m = "(PageManager) unknown error in has visited...\nerror --> {}".format(str(e))
                self.__err_database.add(page_id,m)
                
                maybe_print(self.__verbose, m)
                raise Exception(e)
    
    def restore(self, page_id : str, tag : str) -> None:
        """
            Restores a Page to a prior url as saved by the specified tag.
        """
        page = None
        
        if self.__pages.has(page_id.strip()):
            page = self.__pages.get(page_id.strip())
            try:
                key = "{}-{}".format(tag,page_id.strip())
                url = self.__url_manager.get(key)
                if url != None:
                    page.page().goto(url)
            except Exception as e:
                m = "(PageManager) unknown error restoring...\nerror --> {}".format(str(e))
                self.__err_database.add(page_id,m)
                
                maybe_print(self.__verbose, m)
                raise Exception(e)

    def back(self, page_id : str) -> None:
        """
            Returns a page to it's previous url location.
        """
        page = None
        
        if self.__pages.has(page_id.strip()):
            page = self.__pages.get(page_id.strip())
            try:
                key = "{}-{}".format("previous",page_id.strip())
                if not self.__url_manager.has(key):
                    return
                url = self.__url_manager.get(key)
                if url != None:
                    page.page().goto(url)
            except Exception as e:
                m = "(PageManager) unknown error moving to previous page...\nerror --> {}".format(str(e))
                self.__err_database.add(page_id,m)
                
                maybe_print(self.__verbose, m)
                raise Exception(e)
