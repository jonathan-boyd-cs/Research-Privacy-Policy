import json

PRIVACY_POLICY_KEY_PHRASES = {
  "WORDS": {
    "we": 0, "promise": 0, "only": 0 ,
    "information": 0, "use": 0, "why": 0, "priv": 0 ,
    "other": 0, "if": 0, "when": 0,
    "help": 0, "access": 0, "can't access": 0 
  },
  "CAPABILITY": {
    
        "we will not": 0,
        "we only": 0,
        "we collect": 0,
        "we may collect": 0,
        "we gather data": 0,
      
   
        "you may": 0,
        "you can": 0,
        "right": 0,
        "choice": 0,
        "request": 0,
        "delete":0,
        "deletion": 0,
        "delete": 0,
        "remove": 0,
        "removal": 0,
        "erase": 0,
      
    
  },
  "LEGAL": {
    
        "contract": 0,
        "agreement": 0,
        "obligation": 0,
        "you control": 0,
        "we control": 0,
       
   
        "legal": 0,
        "authority": 0,
        "comply": 0,
        "compliant": 0,
        "law": 0,
        "enforce": 0,
        "govern": 0,
        "regulators": 0,
        "regulatory": 0,
        "policy": 0,
        "international": 0,
        "in accordane with": 0,
    
        "california": 0,
        
        "children": 0,
        "kid": 0,
        "child": 0,
        "youth": 0,
        "young": 0,
        "minor": 0,
    
        "you consented": 0,
        "you consent": 0,
        "you agree": 0,
        "your agreement": 0,
        "you acknowledge": 0,
        "you acknowledged": 0,
        "you signed": 0,
        "you approve": 0,
        "you approved": 0,
        "your permission": 0,
        "you signed": 0,
        "you accepted": 0,
        "you read": 0,
        "you approved": 0,
        "you acknowledge": 0
      
    
  },
  "BUSINESS_FOCUS": {
   
        "third parties": 0,
        "third-party": 0,
        "third party": 0,
        "advertising": 0,
        "sends to": 0,
        "sell to": 0,
        "share with": 0,
        "exchange": 0,
        "improve": 0,
        "optimize": 0,
        "increase": 0,
        "benefit": 0,
        "enhance": 0,
        "enhance": 0,
        "innovate": 0,
        "technologial innovation": 0
      
  },
  "UTILIZATION": {
    "data": 0,
        "we process": 0,
        
        "collected": 0,
        "stored": 0,
        "retention": 0,
  },
  "INNOVATION": {
   "analyze": 0, "analysis": 0, "analytics": 0 ,
    
        "automate": 0,
        "automatic": 0,
        "AI": 0,
       
        "automatically": 0,
     

        "artificial intelligence": 0,
        "algorithm": 0,
        "language processing": 0
   
  },
  "SECURITY": {
   
        "control": 0,
        "settings": 0,
        "controls": 0,
    
        "fraud": 0,
        "to detect": 0,
        "malicious": 0,
       
        "illegal activity": 0,
 
   "to protect": 0,
        "encryption": 0,
        "security": 0,
        "unauthorized": 0,
        "auditing": 0
    
  },
  "EDUCATION": {
   
        "how": 0,
        "what":0,
        "how you": 0,
        
        "how we ": 0,
      
   
      "explain": 0,
      "understand": 0,
      "learn": 0,
      "more information": 0,
      "educational resource": 0,
      "educate": 0
    
  },
  "TECHNOLOGY": {
   
      "cookies": 0,
      "mobile identifiers": 0,
      "pixel tags": 0,
      "web beacons": 0,
      "session monitoring": 0
  
  }
}
