import json
def number_magnitude(symbol):
    if symbol == "K":
        return 1000
    if symbol == "M":
        return 1_000_000
    if symbol == "B":
        return 1_000_000_000
    if symbol == "T":
        return 1_000_000_000_000
    return None
mags = ["K","M","B","T"]
files = ["website-scrape.txt", "website-scrape-run2.txt", "website-scrape-run3.txt","website-scrape-run4.txt"]

website_data_by_industry = {}


for file in files:
    with open(file, 'r') as file:
        industry = None
        website = None
        value = None
        tag = None
        mag = None
        line_number = 0
        
        try:
            
            for line in file:
                line_number += 1
                if line[0] == "*":
                    industry = str(line[1:].strip())
                    if industry not in website_data_by_industry:
                        website_data_by_industry[industry] = {}
                
                if line[0] == "+":
                    website = str(line[1:].strip())
                    website_data_by_industry[industry][website] = {}
                    
                if line[0] == "-":
                    metadata = str(line[1:].strip())
                    metadata = metadata.split("_")
                    tag = metadata[0]
                    
                    if tag == "traffic-count":
                        if metadata[1] != 'None':
                            value = float(metadata[1])
                        else:
                            value = None
                        if metadata[2] != 'None' and metadata[2] in mags:
                            mag = number_magnitude(metadata[2])
                        else:
                            mag = None
                        
                        if value and mag:
                            value = value * mag
                        else:
                            value = None
                        
                        website_data_by_industry[industry][website][tag] = value 
                    
                    if tag == "traffic-value":
                        
                        if metadata[1] != 'None' and metadata[1][-1] in mags:
                            val = metadata[1]
                            val = val[1:]
                            magnitude = val[-1]
                            val = float(val[:-1])
                            mag = number_magnitude(magnitude)
                            if val and mag:
                                value = val * mag
                            else:
                                value = None
                        else:
                            value = None
                        website_data_by_industry[industry][website][tag] = value 
                        
                    
                    
                    if tag == "domain-rating":
                        if metadata[1] != 'None' and len(metadata) == 2:
                            value = float(metadata[1])
                        else:
                            value = None
                        website_data_by_industry[industry][website][tag] = value 
        except:
            print("err {}".format(line_number))

with open("websites-json.json","w") as f:
    json.dump(website_data_by_industry,f)