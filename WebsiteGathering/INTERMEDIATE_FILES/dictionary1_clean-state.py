import json

country_us = ["US","us","Us","USA","UnitedStates","United States", "united states"]

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

data = None
with open("websites-json.json","r") as f:
    data = json.load(f)
    
    for industry in data.keys():
        for site in data[industry].keys():
            if data[industry][site]["Country"] not in country_us:
                if 'State' in data[industry][site]:
                    del data[industry][site]["State"]
            
            else:
                state = data[industry][site]["State"]
                if state in us_state_to_abbrev:
                    data[industry][site]["State"] = us_state_to_abbrev[state]
    
            if data[industry][site]["Country"] == None:
                del data[industry][site]["Country"]
            
            if "State" in data[industry][site]:    
                if data[industry][site]["State"] == None:
                    del data[industry][site]["State"]
    
    
with open("website-json2.json","w") as f:
    json.dump(data,f)