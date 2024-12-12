#!/usr/bin/env python3
"""
    Class serves as a translation module, utilizing googletrans to detect and
    translate languages found on web pages.

"""


import sys
sys.path.append('../')
from googletrans import Translator, LANGUAGES
from DataStorageModule.ErrorStorageModule.error_database import ErrorDatabase
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from playwright.sync_api import expect, sync_playwright

from typing import List

GOOGLETRANS_TRANSLATION_POSSIBLE_SET = 0
GOOGLETRANS_TRANSLATION_POSSIBLE_SET_DATA = 2
GOOGLETRANS_TRANSLATION_POSSIBLE_SET_DATA_TEXT = 0


class TranslationUnit :
    """
        Responsible for translations and the detection of languages
    """
    
    translator  = None
    
    def __init__(self, verbose):
        self.__lang_bank   = LANGUAGES
        self.__translator = Translator()
        self.__verbose = verbose
    def __get_translator__(self):
        return self.__translator
     
    def translate(self,phrase : str, to_lang : str) -> List[str]:
        """
            Translate a phrase to the specified language.
        """
        maybe_print(self.__verbose,"(TranslationUnit) Beginning a translation to {}".format(to_lang))
        translation = self.__translator.translate(phrase,to_lang)
        possible_translations = translation.extra_data['possible-translations']\
                                                        [GOOGLETRANS_TRANSLATION_POSSIBLE_SET]\
                                                        [GOOGLETRANS_TRANSLATION_POSSIBLE_SET_DATA]
        maybe_print(self.__verbose,"(TranslationUnit) Processing the translation result")
        results = []
        for t in possible_translations:
            try:
                v = str(t[GOOGLETRANS_TRANSLATION_POSSIBLE_SET_DATA_TEXT])
                lang = self.detect_lang(v)
                if lang == translation.dest:
                    results.append(v)
            except:
                continue
        maybe_print(self.__verbose,"(TranslationUnit) Returning the translation package")
        return results
    
    def detect_lang(self,phrase : str) -> str:
        """
            Given a phrase, returns the suspected language.
        """
        try:
            maybe_print(self.__verbose,"(TranslationUnit) Detecting language...\n{}".format(phrase))

            translation = self.__translator.detect(phrase)
            return translation.lang
        except:
            return None
        
    def all_translations(self,text : str) -> List[str]:
        """
            Return a text written in all knwon languages.
        """
        result = {}
        for lang in self.__lang_bank.keys():
            result[lang] = self.translate(text,lang)
        return result

class WebTranslationUnit(TranslationUnit):
    """
        Dedicated translation class for web scraping and querying.
    """
    def __init__(self, playwright_manager : sync_playwright ,name : str, errLogDirectory : str, verbose=True) -> None:
        super().__init__(verbose)
        self.__playwright_manager = playwright_manager  
        self.__html_text_search_keys = ['link','paragraph','textbox','caption',
                          'dialog','heading','form','link']
        self.__name = name
        m = time_stamped_msg("web-translation-unit-{}".format(name))
        self.__err_database = ErrorDatabase("{}{}.txt".format(errLogDirectory,m))
        self.__verbose = verbose
    
    def get_name(self) -> str:
        return self.__name
    
    def get_text_search_keys(self) -> List[str]:
        return self.__html_text_search_keys
    
    def detect_lang_webpage(self,url  : str) -> str:
        try:
            maybe_print(self.__verbose, "(WebTranslationUnit) DETECTING LANGUAGE FOR...{}".format(url))
            self.__playwright_manager.visit(self.__name,url)
            page = self.__playwright_manager.get_page(self.__name)
            language = None
            for key in self.get_text_search_keys():
                try:
                    query = page.page().get_by_role(role=key)
                    # ensure a result was found
                    expect(query).not_to_have_count(count=0,timeout=1000)
                    for i in range(query.count()):
                        # extract text
                        result = query.nth(i)
                        text = result.text_content()
                        assert(text != None)
                        for t in text:
                            try:
                                assert(t.strip() != "")
                                assert(len(t.strip()) > 5)
                                language = self.detect_lang(text)
                                assert(language != None)
                                maybe_print(self.__verbose, "(WebTranslationUnit) LANGUAGE DETERMINED AS...{}".format(language))
                                return language 
                            
                            except KeyboardInterrupt:
                                raise (KeyboardInterrupt)
                            
                            except:
                                continue      
                except:
                    continue
            return language
        except Exception as e:
            m = "(WebTranslationUnit) Error fetching URL: {}\nerror-->{}".format(url,str(e))
            self.__err_database.add(self.__name,m)
            
            maybe_print(self.__verbose, m)
            raise Exception(e)    

  
# Example \
# pm = PlaywrightManager(False)
# web_tranlator = WebTranslationUnit(pm,'translator')
# print(web_tranlator.detect_lang_webpage("https://wikipedia.com"))
# print(web_tranlator.detect_lang_webpage("https://steadyhq.com/de/deutschmitrieke/posts"))
# print(web_tranlator.detect_lang_webpage("https://games.yahoo.co.jp/"))
