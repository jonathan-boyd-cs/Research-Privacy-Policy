import pycountry
import json


website_data = None
with open('website-json-country-clean.json','r') as f:
    website_data=json.load(f)
    
i = 0
for industry in website_data:
    industry_data = website_data[industry]
    for website in industry_data:
        site_meta = industry_data[website]

        if 'traffic-count' in site_meta:
            if not type(site_meta['traffic-count']) == float:
                print(website,i,site_meta['traffic-count'])
        if 'traffic-value' in site_meta:
            if not type(site_meta['traffic-value']) == float:
                print(website,i)
        if 'domain-rating' in site_meta:
            if not type(site_meta['domain-rating']) == float:
                print(website,i)
        i += 1

                
#with open('website-json-country-clean.json','w') as f:
#    json.dump(website_data,f)
            


