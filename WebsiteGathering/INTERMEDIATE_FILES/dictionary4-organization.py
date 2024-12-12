import pycountry
import json


website_data = None
with open('website-json-country-clean.json','r') as f:
    website_data=json.load(f)
  
  
organized_data = {}

for industry in website_data:
    
    organized_data[industry] = {
        'unknown':{}, 
        'US':{
            'unknown' :{}
            }
        }
    industry_data = website_data[industry]
    for website in industry_data:
        
        if not 'Country' in industry_data[website]:
            industry_data[website]['Country'] = None
        country = industry_data[website]['Country']
        
        try:
            pycountry.countries.lookup(country)
        except:
            country = 'unknown'
        
        try:
            web_split = website.split('.')
            web_split_c_code = web_split[-1]
            if not code in ['com','org','net']:
                code = pycountry.countries.lookup(web_split_c_code).alpha_2
                if code != 'ME' and code != 'me':
                    country = code
                industry_data[website]['Country'] = country
        except:
            pass
        
        
        
        if country == 'US':
            if 'State' in industry_data[website]:
                state = industry_data[website]['State']
                if not state in organized_data[industry]['US']:
                    organized_data[industry]['US'][state] = {}
                
                organized_data[industry]['US'][state][website] = industry_data[website]
            else:
                organized_data[industry]['US']['unknown'][website] = industry_data[website]
        else:
            if 'State' in industry_data[website]:
                del industry_data[website]['State']
            
            if industry_data[website]['Country'] == None:
                del industry_data[website]['Country']
            if 'State' in industry_data[website] and industry_data[website]['State'] == None:
                del industry_data[website]['State']
                    
                
            if not country in organized_data[industry]:
                organized_data[industry][country] = {}
            organized_data[industry][country][website] = industry_data[website]

        

                
with open('website-clean-organized-by-industry-by-country.json','w') as f:
    json.dump(organized_data,f)
            


