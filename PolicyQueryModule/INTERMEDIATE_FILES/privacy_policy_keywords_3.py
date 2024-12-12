import json

ASSERTIVE = 1
PASSIVE = 2
OTHER = 3
MODIFICATION = 4
LAW = 5
CALIFORNIA = 6
YOUTH = 7
ASSERTION = 8


category_d = {
  1:"ASSERTIVE",
  2:"PASSIVE",
  3:"OTHER",
  4:"MODIFICATION",
  5:"LAW",
  6:"CALIFORNIA",
  7:"YOUTH",
  8:"ASSERTION",
  0:"OTHER",
}

d= {
  "SPOTLIGHT": {
    "COMMITMENT": { "we": 0, "promise": 0, "only": 0 },
    "OTHER": { "information": 0, "use": 0, "why": 0, "privacy": 0 },
    "SUGGESTIVE": { "other": 0 },
    "CONDITIONAL": { "if": 0, "when": 0 },
    "BENEFIT": { "help you": 0, "help us": 0 },
    "ACCESS": { "can access": 0, "can't access": 0 }
  },
  "CAPABILITY": {
    "COMPANY": {
      "we will not": ASSERTIVE,
      "we only": ASSERTIVE,
      "we collect certain": PASSIVE,
      "we collect": ASSERTIVE,
      "we may collect": PASSIVE,
      "we may collect certain": PASSIVE,
      "we collect information": ASSERTIVE,
      "we collect details": ASSERTIVE,
      "we gather data": PASSIVE,
      "we may disclose": PASSIVE,
      "we don't share information that": ASSERTIVE,
      "information we gather": ASSERTIVE
    },
    "USER": {
      "you may": 0,
      "you can": 0,
      "right to request": 0,
      "your choice": 0,
      "request access": 0,
      "deletion of your personal information": MODIFICATION,
      "deletion of": MODIFICATION,
      "delete": MODIFICATION,
      "remove": MODIFICATION,
      "right to delete": MODIFICATION,
      "right to remove": MODIFICATION,
      "removal": MODIFICATION,
      "erase": MODIFICATION,
      "erase your": MODIFICATION,
      "right to erase": MODIFICATION
    }
  },
  "LEGAL": {
    "BINDING": {
      "contract": 0,
      "contractual": 0,
      "agreement": 0,
      "obligation": 0
    },
    "NOTICE": {
      "we have the right": 0,
      "you control": 0,
      "we control": 0,
      "rights": 0,
      "right to know": 0,
      "information may be disclosed": 0
    },
    "LEGISLATIVE": {
      "legal": LAW,
      "authority": LAW,
      "comply with": LAW,
      "compliant with": LAW,
      "law": LAW,
      "enforce": LAW,
      "govern": LAW,
      "regulators": LAW,
      "privacy law": LAW,
      "policy": LAW,
      "state laws": LAW,
      "international laws": LAW,
      "in accordane with": LAW,
      "california": CALIFORNIA,
      "other than california": CALIFORNIA,
      "outside of california": CALIFORNIA,
      "children": YOUTH,
      "kid": YOUTH,
      "child": YOUTH,
      "youth": YOUTH,
      "young": YOUTH,
      "minor": YOUTH,
      "under the age": YOUTH,
      "under-the-age": YOUTH,
      "under age": YOUTH,
      "under-age": YOUTH
    },
    "PREPPING": {
      "consent": 0,
      "dispute": 0,
      "with your consent": 0,
      "does not cover": 0,
      "you consented": ASSERTION,
      "you consent": ASSERTION,
      "you agree": ASSERTION,
      "your agreement": ASSERTION,
      "you acknowledge": ASSERTION,
      "you acknowledged": ASSERTION,
      "you signed": ASSERTION,
      "you approve": ASSERTION,
      "you approved": ASSERTION,
      "with your permission": ASSERTION,
      "you made it public": ASSERTION,
      "you oblige": ASSERTION,
      "you obliged": ASSERTION,
      "you chose": ASSERTION,
      "you choose": ASSERTION,
      "when you signed": ASSERTION,
      "when you accepted": ASSERTION,
      "when you read": ASSERTION,
      "when you approved": ASSERTION,
      "when you consent": ASSERTION,
      "when you acknowledge": ASSERTION
    }
  },
  "BUSINESS_FOCUS": {
    "EXTERNAL": {
      "third parties": 0,
      "third-party": 0,
      "third party": 0,
      "we send to third": ASSERTIVE,
      "we sell to third": ASSERTIVE,
      "we share with third": ASSERTIVE,
      "we exchange with third": ASSERTIVE,
      "may send to third": PASSIVE,
      "may lead to third": PASSIVE,
      "may sell to third": PASSIVE,
      "may share with third": PASSIVE,
      "may exchange with third": PASSIVE,
      "advertising partners": 0
    },
    "SELF": {
      "may share information": PASSIVE,
      "may share": PASSIVE,
      "we share": ASSERTIVE,
      "we sell": ASSERTIVE,
      "business goals": 0,
      "business purposes": 0,
      "enterprise": 0
    },
    "AMBITION": {
      "to improve the service": 0,
      "to improve": 0,
      "to optimize": 0,
      "to increase": 0,
      "to benefit our": 0,
      "to enhance our": 0,
      "to enhance": 0,
      "to innovate": 0,
      "technologial innovation": 0
    }
  },
  "ATTRIBUTING": {
    "USER": {
      "information you": 0,
      "we create a user profile": ASSERTIVE,
      "create a user profile": ASSERTIVE,
      "we profile": ASSERTIVE,
      "a profile": 0,
      "your activity": 0,
      "user behavior": 0,
      "owns my data": ASSERTIVE,
      "owns your data": ASSERTIVE,
      "personl records": 0,
      "personal records": 0
    },
    "LOCATION": {
      "location information": 0,
      "location": 0,
      "location data": 0
    },
    "DATA": {
      "usage information": 0,
      "usage": 0,
      "usage data": 0,
      "records": 0
    }
  },
  "UTILIZATION": {
    "USE": {
      "to gather data": 0,
      "we process personal data": ASSERTIVE,
      "we process": ASSERTIVE,
      "data controller": 0,
      "we use information": ASSERTIVE,
      "may use information": PASSIVE
    },
    "NON_EXCLUSIVE": {
      "we sell information": ASSERTIVE,
      "sharing of": 0,
      "sharing of personal": 0,
      "sharing of user": 0,
      "external processing": 0
    },
    "PERSISTENCE": {
      "data collected": 0,
      "collected": 0,
      "stored": 0,
      "retention": 0,
      "collected by": 0,
      "collected with": 0
    }
  },
  "INNOVATION": {
    "DEPTH": { "analyze": 0, "analysis": 0, "analytics": 0 },
    "AUTOMTATION": {
      "automate": 0,
      "automatic": 0,
      "AI": 0,
      "information collected automatically": 0,
      "collected automatically": 0
    },
    "AI": {
      "artificial intelligence": 0,
      "algorithm": 0,
      "language processing": 0
    }
  },
  "SECURITY": {
    "CHOICE": {
      "control options": 0,
      "settings": 0,
      "privacy controls": 0,
      "privacy settings": 0
    },
    "INTENTION": {
      "fraud": 0,
      "to detect": 0,
      "malicious": 0,
      "against malicious": 0,
      "against fraud": 0,
      "illegal activity": 0
    },
    "COMMITMENT": { "to protect": 0, "protect personal information": 0 },
    "ACCESS": {
      "encryption": 0,
      "security": 0,
      "unauthorized": 0,
      "auditing": 0
    }
  },
  "EDUCATION": {
    "HOW": {
      "how we use": 0,
      "how": 0,
      "how you": 0,
      "how we use your": 0,
      "how cookies": 0,
      "how are": 0,
      "how we collect": 0,
      "how can i": 0,
      "how you can": 0,
      "how to": 0,
      "how we disclose": 0
    },
    "OTHER": {
      "explain": 0,
      "understand": 0,
      "type of cookies": 0,
      "what are cookies": 0,
      "what are": 0,
      "learn": 0,
      "purpose for collection": 0
    }
  },
  "SUGGESTIVE": {
    "SUSPICIOUS": {
      "for various reasons": 0,
      "possibility": 0,
      "intention": 0,
      "certain": 0,
      "certain information": 0,
      "other data": 0,
      "other purposes": 0,
      "other reasons": 0,
      "other objectives": 0,
      "various purposes": 0,
      "various objectives": 0,
      "if necessary": 0,
      "for business purpose": 0
    },
    "CONDITIONAL": {
      "we may share": 0,
      "for legal reasons": 0,
      "may not cover": 0,
      "only when": 0,
      "only for": 0,
      "only under": 0
    }
  },
  "TECHNOLOGY": {
    "cookies": 0,
    "mobile identifiers": 0,
    "pixel tags": 0,
    "web beacons": 0,
    "session monitoring": 0
  },
  "DNSMI": {
    "do not share my personal information": 0,
    "dnsmi": 0,
    "do not sell my personal information": 0,
    "do not share or sell my personal information": 0,
    "do not share my data": 0,
    "do not sell my data": 0,
    "do not sell or share my data": 0,
    "do not share or sell my data": 0,
    "do not sell or share my personal information": 0,
    "do not sell my info":0,
    "do not sell or share my info":0,
    "do not share or sell my info":0,
    "do not share my info":0
  }
}


res = {x:{} for x in d.keys()}
for category in d.keys():
  
   
  
    for subcat in d[category].keys():
        if subcat == "OTHER":
          res[category][subcat] = {x:0 for x in d[category][subcat]} 
          continue
        if type(d[category][subcat]) == dict:
          if not subcat in res[category]:
            res[category][subcat] = {}
        
          for phrase in d[category][subcat].keys():
            subject = category_d[d[category][subcat][phrase]]    
            if subject not in res[category][subcat]:
                res[category][subcat][subject] = {}
            res[category][subcat][subject][phrase] = 0
        else:

          res[category]["OTHER"] = {x:0 for x in d[category]}        

        
with open("privacy-policy-clean3-key-phrases.json",'w') as f:
    json.dump(res,f)