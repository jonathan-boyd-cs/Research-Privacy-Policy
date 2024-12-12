import json

files = ["website-whois-scrape-run1.txt"]

website_data_by_industry = {}
with open("website-whois-json4.json",'r') as f:
    website_data_by_industry = json.load(f)


    for file in files:
        with open(file, 'r') as file:
            industry = None
            website = None
            value = None
            tag = None
    
            line_number = 0
            
            for line in file:
                line_number += 1
                if line[0] == "*":
                    industry = str(line[1:].strip())
                    
                if line[0] == "+":
                    website = str(line[1:].strip())
                    
                if line[0] == "-":
                    metadata = str(line[1:].strip())
                    metadata = metadata.split(":")
                    tag = metadata[0]
                    
                    if tag == "State":
                        if website_data_by_industry[industry][website]['State'] == None:
                            website_data_by_industry[industry][website]['State'] = metadata[1]
                    else:
                        if website_data_by_industry[industry][website]['Country'] == None:
                            website_data_by_industry[industry][website]['Country'] = metadata[1]
                        
                        
with open("websites-json.json","w") as f:
    json.dump(website_data_by_industry,f)