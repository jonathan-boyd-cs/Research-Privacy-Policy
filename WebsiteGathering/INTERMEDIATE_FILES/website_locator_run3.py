'''
    Webscrapper -> Collecting websites for research study from ahref.com
    Using : playwright (sync)

'''
import pycountry
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}


from playwright.sync_api import sync_playwright, expect
import json
from ipwhois import IPWhois
import dns.message
import dns.query
import dns.rdatatype
import dns.rrset

website_database = {}
with open("website-whois-json3.json", "r") as f:
    website_database = json.load(f)

print(website_database.keys())

target_site = "https://www.whois.com/whois/"
with sync_playwright() as playwright:
    # Launch a browser
    browser = playwright.chromium.launch(headless=False)
    # Create a new page/tab
    page = browser.new_page()
    page.set_default_timeout(10000)
   
    page.goto(url=target_site)
    
    # invalid_domain = page.get_by_role(role="heading",name="Invalid domain name")
    
    input_field =  page.get_by_placeholder(
        "Enter Domain Name or IP Address")
    
    search_btn = page.locator("button[aria-label='Whois Search']").nth(1)
    
       

    with open("website-whois-scrape-run000.txt",'w') as f:
        for industry in website_database.keys():
            f.write("* {}\n".format(industry))
            industry_data = website_database[industry]
            for website in industry_data.keys():
               
                site_data = industry_data[website]
                if not 'State' in site_data:
                    site_data['State'] = None
                if not 'Country' in site_data:
                    site_data['Country'] = None
                    
                if site_data['Country'] == None:
                    try:
                        s = website.split(':')
                        web = 'www.' + s[1][2:]
                        print(web)
                        query = dns.message.make_query(web,dns.rdatatype.A)
                        response = dns.query.tls(query,'8.8.8.8')
                        for x in response.answer:
                            if not str(str(x[0])[0]).isdigit():
                                continue
                            ip = str(x[0])
                            print(ip)
                            
                            obj = IPWhois(ip)
                            results = obj.lookup_rdap(depth=1)
                            
                            asn_country_code = results['asn_country_code']
                            site_data['Country'] = asn_country_code
                            print(asn_country_code)
                    except:
                        pass     
                    
                if site_data['State'] != None or site_data['Country'] != None:
                    continue
                
                
                input_field.fill(website)
                search_btn.click()        
                
                
                try:
                    
                    expect( page.locator("div.df-row").filter(has_text="Country").nth(0).locator("div.df-value")).not_to_be_empty(timeout=500)
                    country_info = page.locator("div.df-row").filter(has_text="Country").nth(0).locator("div.df-value").text_content()
                    code = pycountry.countries.lookup(country_info).alpha_2
                    site_data['Country'] = code
                    f.write("+ {}\n".format(website))
                    f.write("- Country: {}\n".format(country_info))
                except:
                    pass    
                try:
                    expect( page.locator("div.df-row").filter(has_text="State").nth(0).locator("div.df-value")).not_to_be_empty(timeout=500)
                    state_info =   page.locator("div.df-row").filter(has_text="State").nth(0).locator("div.df-value").text_content()
                    site_data['State'] = state_info
                    
                    f.write("+ {}\n".format(website))
                    f.write("- State: {}\n".format(state_info))
                    
                    page.goto(target_site)
                    continue
                except:
                    try:
                        expect( page.locator("pre.df-raw#registryData")).not_to_be_empty(timeout=500)
                        text = page.locator("pre.df-raw#registryData").text_content()
                        i = -1
                        i = text.find('country')
                        if i == -1:
                            i = text.find('Country')
                        if i > -1:
                            i += 9
                            country = text[i:].split()
                            country = country[0]
                            code = pycountry.countries.lookup(country).alpha_2
                            f.write("+ {}\n".format(website))
                            f.write("- Country: {}\n".format(country))
                            site_data['Country'] = code
                        else:
                            raise Exception('e')
                        page.goto(target_site)
                        continue 
                    except:
                        try:
                            exception_domain = ['com','org','net','io','gov']
               
                            web_split = website.split('.')
                            web_split_c_code = web_split[-1]
                            
                            if web_split_c_code not in exception_domain:
                                
                                if web_split_c_code == 'uk':
                                    site_data['Country'] = 'UK'
                                else:
                                    code = pycountry.countries.lookup(web_split_c_code.upper()).alpha_2
                                    country = code
                                    site_data['Country'] = country
                                    

                                page.goto(target_site)
                                continue
                            else:
                                raise Exception('e')                  
                        except:
                           pass
                            
                        page.goto(target_site)
                        continue
                    
                    
    
    with open('website-whois-json4.json','w') as f:
        json.dump(website_database,f)
                
                
            
    # Close browser
    browser.close()
    
