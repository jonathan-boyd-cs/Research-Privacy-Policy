import pycountry
import json



print(pycountry.countries.lookup("km"))

website_data = None
with open('website-json2.json','r') as f:
    website_data=json.load(f)
    

for industry in website_data:
    industry_data = website_data[industry]
    for website in industry_data:
        site_meta = industry_data[website]
        
        
        website_split = website.split('.')
        try:
            code = website_split[-1]
            if not code in ['com','org','net']:
                country_code = pycountry.countries.lookup(code).alpha_2
                if not 'Country' in site_meta:
                    site_meta['Country'] = ""
                site_meta['Country'] = country_code
        except:
            pass
        
        
        if 'Country' in site_meta:
            try:
                country = site_meta['Country']
                country_code = pycountry.countries.lookup(country).alpha_2
                site_meta['Country'] = country_code
                
            except:
                del site_meta['Country']
                if 'State' in site_meta:
                    del site_meta['State']
        else:
            if 'State' in site_meta:
                del site_meta['State']
                
        if 'Country' in site_meta and site_meta['Country'] != 'US':
            if 'State' in site_meta:
                    del site_meta['State']
        
with open('website-json-country-clean.json','w') as f:
    json.dump(website_data,f)
            


