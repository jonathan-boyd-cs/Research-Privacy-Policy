import json
import sys
sys.path.append('../')

from FileManager.file_manager import FileManager
from ErrorHandleModule.general import time_stamped_msg, maybe_print
from DataStorageModule.DataCleanerModule.was_manager import WASManager
from PolicyQueryModule.privacy_policy_keywords import PRIVACY_POLICY_KEY_PHRASES as PPKP
from WebsiteGathering.Runs_Cumulative import data as web_src

name = 'was_manager'
output = './PostScrapeClean/'
log = './PostScrapeClean/Logs/'
columns = ['Industry', 'Country', 'State', 'URL']
web_src_keys = [ industry for industry in web_src.keys()]
was_name = 'pps' #privacy policy scraper
existing = [
    "../OutputFiles/Run/SCRAPE/pps-WAS-results-10_22PM-on-December-01.json",
    "../OutputFiles/Run/SCRAPE/pps-WAS-results-12_20PM-on-December-02.json",
    
]


WASM = WASManager(name, output, log, PPKP, 3, columns, web_src, True)

file = WASM.merge_results( web_src_keys, '../OutputFiles/Run/SCRAPE/',was_name, existing)

WASM.clean(file, 'post-scrape-results-2')



