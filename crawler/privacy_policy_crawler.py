#!/usr/bin/env python3

"""
    file: privacy_policy_crawler.py
    
    function: A specific implementation of the WebAnalysisSuite...queries websites for privacy policy text  and link data as specified by the
    provided parameters

"""
import sys
sys.path.append('../')
from WebScraperModule.web_analysis_suite import WebAnalysisSuite
from WebsiteGathering.websites import WEBSITE_DATASET as WebsiteDictionary
from PolicyQueryModule.privacy_link_key_phrases import PRIVACY_DNSMI_LINK_KEY_PHRASES
from PolicyQueryModule.privacy_link_key_phrases import PRIVACY_LINK_KEYWORDS
from PolicyQueryModule.privacy_policy_keywords import PRIVACY_POLICY_KEY_PHRASES

from DataStorageModule.DataCleanerModule.was_manager import WASManager
import random

# privacy policy scraper
name                    = 'pps'
output_directory        = '../OutputFiles/Run/SCRAPE/'
error_log_directory     = '../OutputFiles/Run/ERROR/'
headless                = False
slow_mo                 = 0
policy_link_keywords    = PRIVACY_LINK_KEYWORDS
policy_text_phrases     = PRIVACY_POLICY_KEY_PHRASES
keys                    = list(WebsiteDictionary.keys())
web_url_index_in_key_heirarchy = 3
columns                 = ['Industry', 'Country','State','URL']
verbose                 = True

# Utilizing the Web Analysis Suite Manager to handle the aquisition of website urls... will be used later 
# in a different file for result cleansing...
WASM = WASManager(
    name=name, 
    outputDirectory         =   output_directory, 
    errLogDirectory         =   error_log_directory,
    phrase_legend           =   policy_text_phrases, 
    subj_idx                =   web_url_index_in_key_heirarchy,
    columns                 =   columns,
    web_src                 =   WebsiteDictionary,
    verbose                 =   verbose)


websites = WASM.pull_urls(keys) 
# OutputFiles/Run
for website in websites:
    try:
        site = WASM.url_to_file_safe(website)
        file = "{}{}-{}-{}.json".format(output_directory,'WAS',name,site)

        with open(file,'r') as f:
            a = 1

        websites.remove(website)

    except KeyboardInterrupt:
        sys.exit()
    except:
        try:
            file = "{}intermediate/{}-intermediate.json".format(output_directory,site)
            with open(file,'r') as f:
                a = 1
            websites.remove(website)

        except:
            continue
    
random.shuffle(websites)

# Web Analysis Suite expects its additional text search parameters in a list-of-dictionaries format
# with these exact keys...

accessory_pulls = [
    {
        'name':'DNSMI',
        'values':PRIVACY_DNSMI_LINK_KEY_PHRASES
    }
]

# Utilizing Web Analysis Suite to handle the difficulties of the scraping...
WAS = WebAnalysisSuite(
    name                = name,
    outputDirectory     = output_directory,
    errLogDirectory     = error_log_directory,
    headless            = headless,
    slow_mo             = slow_mo,
    web_link_keywords   = policy_link_keywords,
    web_text_key_phrases= policy_text_phrases,
    websites            = websites,
    verbose             = verbose
)
# Running the default routine... seeks [web_link_keywords] -> navigate through each link and...
# search for [web_text_key_phrases]
# ** first will seek presence of text as necessary given [accessory_pulls]
try:
    WAS.run_default_routine(
        accessory_has_text=accessory_pulls
    )
except:
    del WAS
    sys.exit()
    