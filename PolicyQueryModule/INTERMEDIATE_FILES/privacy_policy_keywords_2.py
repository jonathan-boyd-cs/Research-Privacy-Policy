import json

# SPOTLIGHT
COMMITMENT = 0
SUGGESTIVE = 1
CONDITIONAL = 2
BENEFIT = 3
ACCESS = 4

# CAPABILITY
COMPANY = 5
USER = 6

# LEGAL
BINDING = 7
NOTICE = 8
LEGISLATIVE = 9
PREPPING = 10

# BUSINESS_FOCUS
EXTERNAL = 11
SELF = 12
AMBITION = 13

# ATTRIBUTING
USER = 14
LOCATION = 15
DATA = 16

# UTILIZATION
NON_EXCLUSIVE = 17
PERSISTENCE = 18
USE = 19

# INNOVATION
DEPTH = 20
AUTOMATION = 21
AI = 22

# SECURITY
CHOICE = 23
INTENTION = 24
ACCESS = 25

# EDUCATION
OTHER = 26
HOW = 27

# SUGGESTIVE
SUSPICIOUS = 28



category_d = {
    
    0:"COMMITMENT",
    1:"SUGGESTIVE",
    2:"CONDITIONAL",
    3:"BENEFIT",
    4:"ACCESS",
    5:"COMPANY",
    6:"USER",
    7:"BINDING",
    8:"NOTICE",
    9:"LEGISLATIVE",
    10:"PREPPING",
    11:"EXTERNAL",
    12:"SELF",
    13:"AMBITION",
    14:"USER",
    15:"LOCATION",
    16:"DATA",
    17:"NON_EXCLUSIVE",
    18:"PERSISTENCE",
    19:"USE",
    20:"DEPTH",
    21:"AUTOMTATION",
    22:"AI",
    23:"CHOICE",
    24:"INTENTION",
    25:"ACCESS",
    26:"OTHER",
    27:"HOW",
    28:"SUSPICIOUS",

}


d = {
  "SPOTLIGHT": {
    "we": COMMITMENT,
    "promise": COMMITMENT,
    "information": OTHER,
    "use": OTHER,
    "other": SUGGESTIVE,
    "if": CONDITIONAL,
    "when": CONDITIONAL,
    "only": COMMITMENT,
    "why": OTHER,
    "privacy": OTHER,
    "help you": BENEFIT,
    "help us": BENEFIT,
    "can access": ACCESS,
    "can't access": ACCESS
  },
  "CAPABILITY": {
    "we will not": COMPANY,
    "we only": COMPANY,
    "you may": USER,
    "we collect certain": COMPANY,
    "we collect": COMPANY,
    "we may collect": COMPANY,
    "we may collect certain": COMPANY,
    "you can": USER,
    "we collect information": COMPANY,
    "we collect details": COMPANY,
    "we gather data": COMPANY,
    "we may disclose": COMPANY,
    "right to request": USER,
    "your choice": USER,
    "request access": USER,
    "deletion of your personal information": USER,
    "deletion of": USER,
    "delete": USER,
    "remove": USER,
    "right to delete": USER,
    "right to remove": USER,
    "removal": USER,
    "erase": USER,
    "erase your": USER,
    "right to erase": USER,
    "we don't share information that": COMPANY,
    "information we gather": COMPANY
  },
  "LEGAL": {
    "contract": BINDING,
    "contractual": BINDING,
    "agreement": BINDING,
    "we have the right": NOTICE,
    "you control": NOTICE,
    "we control": NOTICE,
    "legal": LEGISLATIVE,
    "obligation": BINDING,
    "authority": LEGISLATIVE,
    "comply with": LEGISLATIVE,
    "compliant with": LEGISLATIVE,
    "law": LEGISLATIVE,
    "enforce": LEGISLATIVE,
    "govern": LEGISLATIVE,
    "regulators": LEGISLATIVE,
    "rights": NOTICE,
    "consent": PREPPING,
    "dispute": PREPPING,
    "privacy law": LEGISLATIVE,
    "policy": LEGISLATIVE,
    "state laws": LEGISLATIVE,
    "international laws": LEGISLATIVE,
    "with your consent": PREPPING,
    "in accordane with": LEGISLATIVE,
    "does not cover": PREPPING,
    "california": LEGISLATIVE,
    "other than california": LEGISLATIVE,
    "outside of california": LEGISLATIVE,
    "right to know": NOTICE,
    "information may be disclosed": NOTICE,
    "children": LEGISLATIVE,
    "kid": LEGISLATIVE,
    "child": LEGISLATIVE,
    "youth": LEGISLATIVE,
    "young": LEGISLATIVE,
    "minor": LEGISLATIVE,
    "under the age": LEGISLATIVE,
    "under-the-age": LEGISLATIVE,
    "under age": LEGISLATIVE,
    "under-age": LEGISLATIVE,
    "you consented": PREPPING,
    "you consent": PREPPING,
    "you agree": PREPPING,
    "your agreement": PREPPING,
    "you acknowledge": PREPPING,
    "you acknowledged": PREPPING,
    "you signed": PREPPING,
    "you approve": PREPPING,
    "you approved": PREPPING,
    "with your permission": PREPPING,
    "you made it public": PREPPING,
    "you oblige": PREPPING,
    "you obliged": PREPPING,
    "you chose": PREPPING,
    "you choose": PREPPING,
    "when you signed": PREPPING,
    "when you accepted": PREPPING,
    "when you read": PREPPING,
    "when you approved": PREPPING,
    "when you consent": PREPPING,
    "when you acknowledge": PREPPING
  },
  "BUSINESS_FOCUS": {
    "third parties": EXTERNAL,
    "third-party": EXTERNAL,
    "third party": EXTERNAL,
    "we send to third": EXTERNAL,
    "we sell to third": EXTERNAL,
    "we share with third": EXTERNAL,
    "we exchange with third": EXTERNAL,
    "may send to third": EXTERNAL,
    "may lead to third": EXTERNAL,
    "may sell to third": EXTERNAL,
    "may share with third": EXTERNAL,
    "may exchange with third": EXTERNAL,
    "may share information": SELF,
    "may share": SELF,
    "we share": SELF,
    "we sell": SELF,
    "business goals": SELF,
    "business purposes": SELF,
    "advertising partners": EXTERNAL,
    "enterprise": SELF,
    "to improve the service": AMBITION,
    "to improve": AMBITION,
    "to optimize": AMBITION,
    "to increase": AMBITION,
    "to benefit our": AMBITION,
    "to enhance our": AMBITION,
    "to enhance": AMBITION,
    "to innovate": AMBITION,
    "technologial innovation": AMBITION
  },
  "ATTRIBUTING": {
    "information you": USER,
    "we create a user profile": USER,
    "create a user profile": USER,
    "we profile": USER,
    "a profile": USER,
    "location information": LOCATION,
    "location": LOCATION,
    "usage information": DATA,
    "usage": DATA,
    "usage data": DATA,
    "location data": LOCATION,
    "your activity": USER,
    "user behavior": USER,
    "owns my data": USER,
    "owns your data": USER,
    "personl records": USER,
    "personal records": USER,
    "records": DATA
  },
  "UTILIZATION": {
    "to gather data": USE,
    "we sell information": NON_EXCLUSIVE,
    "we process personal data": USE,
    "we process": USE,
    "sharing of": NON_EXCLUSIVE,
    "sharing of personal": NON_EXCLUSIVE,
    "sharing of user": NON_EXCLUSIVE,
    "data controller": USE,
    "data collected": PERSISTENCE,
    "collected": PERSISTENCE,
    "stored": PERSISTENCE,
    "retention": PERSISTENCE,
    "collected by": PERSISTENCE,
    "collected with": PERSISTENCE,
    "we use information": USE,
    "may use information": USE,
    "external processing": NON_EXCLUSIVE
  },
  "INNOVATION": {
    "analyze": DEPTH,
    "analysis": DEPTH,
    "analytics": DEPTH,
    "automate": AUTOMATION,
    "automatic": AUTOMATION,
    "AI": AUTOMATION,
    "artificial intelligence": AI,
    "algorithm": AI,
    "language processing": AI,
    "information collected automatically": AUTOMATION,
    "collected automatically": AUTOMATION
  },
  "SECURITY": {
    "control options": CHOICE,
    "fraud": INTENTION,
    "to protect": COMMITMENT,
    "settings": CHOICE,
    "protect personal information": COMMITMENT,
    "to detect": INTENTION,
    "malicious": INTENTION,
    "against malicious": INTENTION,
    "against fraud": INTENTION,
    "illegal activity": INTENTION,
    "encryption": ACCESS,
    "security": ACCESS,
    "unauthorized": ACCESS,
    "privacy controls": CHOICE,
    "privacy settings": CHOICE,
    "auditing": ACCESS
  },
  "EDUCATION": {
    "how we use": HOW,
    "how": HOW,
    "how you": HOW,
    "explain": OTHER,
    "understand": OTHER,
    "how we use your": HOW,
    "type of cookies": OTHER,
    "what are cookies": OTHER,
    "how cookies": HOW,
    "what are": OTHER,
    "how are": HOW,
    "learn": OTHER,
    "how we collect": HOW,
    "how can i": HOW,
    "how you can": HOW,
    "how to": HOW,
    "how we disclose": HOW,
    "purpose for collection": OTHER
  },
  "SUGGESTIVE": {
    "for various reasons": SUSPICIOUS,
    "possibility": SUSPICIOUS,
    "intention": SUSPICIOUS,
    "certain": SUSPICIOUS,
    "certain information": SUSPICIOUS,
    "other data": SUSPICIOUS,
    "other purposes": SUSPICIOUS,
    "other reasons": SUSPICIOUS,
    "other objectives": SUSPICIOUS,
    "we may share": CONDITIONAL,
    "for legal reasons": CONDITIONAL,
    "may not cover": CONDITIONAL,
    "only when": CONDITIONAL,
    "only for": CONDITIONAL,
    "only under": CONDITIONAL,
    "various purposes": SUSPICIOUS,
    "various objectives": SUSPICIOUS,
    "if necessary": SUSPICIOUS,
    "for business purpose": SUSPICIOUS
  },
  "TECHNOLOGY": {
    "cookies": -1,
    "mobile identifiers": -1,
    "pixel tags": -1,
    "web beacons": -1,
    "session monitoring": -1
  },
  "DNSMI": {
    "do not share my personal information": -1,
    "dnsmi": -1,
    "do not sell my personal information": -1,
    "do not share or sell my personal information": -1,
    "do not share my data": -1,
    "do not sell my data": -1,
    "do not sell or share my data": -1,
    "do not share or sell my data": -1,
    "do not sell or share my personal information": -1
  }
}

res = {x:{} for x in d.keys()}
for category in d.keys():
    for phrase in d[category]:
        
        if d[category][phrase] == -1:
            res[category][phrase] = 0
            continue
        
        
        subject = category_d[d[category][phrase]]    
        if subject not in res[category]:
            res[category][subject] = {}
        res[category][subject][phrase] = 0        

        
with open("privacy-policy-clean2-key-phrases.json",'w') as f:
    json.dump(res,f)