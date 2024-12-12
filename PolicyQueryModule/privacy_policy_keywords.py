import json

PRIVACY_POLICY_KEY_PHRASES = {
  "SPOTLIGHT": {
    "COMMITMENT": { "OTHER": { "we": 0, "promise": 0, "only": 0 } },
    "SUGGESTIVE": { "OTHER": { "other": 0 } },
    "CONDITIONAL": { "OTHER": { "if": 0, "when": 0 } },
    "BENEFIT": { "OTHER": { "help you": 0, "help us": 0 } },
    "ACCESS": { "OTHER": { "can access": 0, "can't access": 0 } }
  },
  "CAPABILITY": {
    "COMPANY": {
      "ASSERTIVE": {
        "we will not": 0,
        "we only": 0,
        "we collect": 0,
        "we collect information": 0,
        "we collect details": 0,
        "we don't share information that": 0,
      },
      "PASSIVE": {
        "we collect certain": 0,
        "we may collect": 0,
        "we may collect certain": 0,
        "we gather data": 0,
        "we may disclose": 0
      }
    },
    "USER": {
      "OTHER": {
        "you may": 0,
        "you can": 0,
        "right to request": 0,
        "your choice": 0,
        "request access": 0
      },
      "MODIFICATION": {
        "deletion of": 0,
        "delete": 0,
        "remove": 0,
        "removal": 0,
        "erase": 0,
      }
    }
  },
  "LEGAL": {
    "BINDING": {
      "OTHER": {
        "contract": 0,
        "contractual": 0,
        "agreement": 0,
        "obligation": 0
      }
    },
    "NOTICE": {
      "OTHER": {
        "we have the right": 0,
        "you control": 0,
        "we control": 0,
        "rights": 0,
        "right to know": 0,
        "information may be disclosed": 0
      }
    },
    "LEGISLATIVE": {
      "LAW": {
        "legal": 0,
        "authority": 0,
        "comply with": 0,
        "compliant with": 0,
        "law": 0,
        "enforce": 0,
        "govern": 0,
        "regulators": 0,
        "privacy law": 0,
        "policy": 0,
        "state laws": 0,
        "international laws": 0,
        "in accordane with": 0
      },
      "CALIFORNIA": {
        "california": 0,
        "other than california": 0,
        "outside of california": 0
      },
      "YOUTH": {
        "children": 0,
        "kid": 0,
        "child": 0,
        "youth": 0,
        "young": 0,
        "minor": 0,
        "under the age": 0,
        "under age": 0,
      }
    },
    "PREPPING": {
      "OTHER": {
        "consent": 0,
        "dispute": 0,
        "with your consent": 0,
        "does not cover": 0
      },
      "ASSERTION": {
        "you consented": 0,
        "you consent": 0,
        "you agree": 0,
        "your agreement": 0,
        "you acknowledge": 0,
        "you acknowledged": 0,
        "you signed": 0,
        "you approve": 0,
        "you approved": 0,
        "with your permission": 0,
        "you made it public": 0,
        "you oblige": 0,
        "you obliged": 0,
        "you chose": 0,
        "you choose": 0,
        "when you signed": 0,
        "when you accepted": 0,
        "when you read": 0,
        "when you approved": 0,
        "when you consent": 0,
        "when you acknowledge": 0
      }
    }
  },
  "BUSINESS_FOCUS": {
    "EXTERNAL": {
      "OTHER": {
        "third parties": 0,
        "third-party": 0,
        "third party": 0,
        "advertising partners": 0
      },
      "ASSERTIVE": {
        "we send to third": 0,
        "we sell to third": 0,
        "we share with third": 0,
        "we exchange with third": 0
      },
      "PASSIVE": {
        "may send to third": 0,
        "may sell to third": 0,
        "may share with third": 0,
        "may exchange with third": 0
      }
    },
    "SELF": {
      "PASSIVE": { "may share information": 0, "may share": 0 },
      "ASSERTIVE": { "we share": 0, "we sell": 0 },
      "OTHER": { "business goals": 0, "business purposes": 0, "enterprise": 0 }
    },
    "AMBITION": {
      "OTHER": {
        "to improve": 0,
        "to optimize": 0,
        "to increase": 0,
        "to benefit our": 0,
        "to enhance our": 0,
        "to enhance": 0,
        "to innovate": 0,
        "technologial innovation": 0
      }
    }
  },
  "ATTRIBUTING": {
    "USER": {
      "OTHER": {
        "information you": 0,
        "a profile": 0,
        "your activity": 0,
        "user behavior": 0,
        "personl records": 0,
        "personal records": 0
      },
      "ASSERTIVE": {
        "we create a user profile": 0,
        "create a user profile": 0,
        "we profile": 0,
        "owns your data": 0
      }
    },
    "LOCATION": {
      "OTHER": { "location information": 0, "location": 0, "location data": 0 }
    },
    "DATA": {
      "OTHER": {
        "usage": 0,
        "usage": 0,
        "records": 0
      }
    }
  },
  "UTILIZATION": {
    "USE": {
      "OTHER": { "to gather data": 0, "data controller": 0 },
      "ASSERTIVE": {
        "we process": 0,
        "we use": 0
      },
      "PASSIVE": { "may use information": 0 }
    },
    "NON_EXCLUSIVE": {
      "ASSERTIVE": { "we sell information": 0 },
      "OTHER": {
        "sharing of": 0,
        "sharing of personal": 0,
        "sharing of user": 0,
        "external processing": 0
      }
    },
    "PERSISTENCE": {
      "OTHER": {
        "data collected": 0,
        "collected": 0,
        "stored": 0,
        "retention": 0,
        "collected": 0,
        "collected": 0
      }
    }
  },
  "INNOVATION": {
    "DEPTH": { "OTHER": { "analyze": 0, "analysis": 0, "analytics": 0 } },
    "AUTOMTATION": {
      "OTHER": {
        "automate": 0,
        "automatic": 0,
        "AI": 0,
        "information collected automatically": 0,
        "collected automatically": 0
      }
    },
    "AI": {
      "OTHER": {
        "artificial intelligence": 0,
        "algorithm": 0,
        "language processing": 0
      }
    }
  },
  "SECURITY": {
    "CHOICE": {
      "OTHER": {
        "control options": 0,
        "settings": 0,
        "privacy controls": 0,
        "privacy settings": 0
      }
    },
    "INTENTION": {
      "OTHER": {
        "fraud": 0,
        "detect": 0,
        "malicious": 0,
        "illegal activity": 0
      }
    },
    "COMMITMENT": {
      "OTHER": { "to protect": 0, "protect personal information": 0 }
    },
    "ACCESS": {
      "OTHER": {
        "encryption": 0,
        "security": 0,
        "unauthorized": 0,
        "auditing": 0
      }
    }
  },
  "EDUCATION": {
    "HOW": {
      "OTHER": {
        "how": 0,
        "how you": 0,
        "how we": 0,
        "how are": 0,
        "how can": 0,
      }
    },
    "OTHER": {
      "explain": 0,
      "understand": 0,
      "type of cookies": 0,
      "what are": 0,
      "learn": 0,
      "purpose for collection": 0,
      "if you have questions": 0,
      "if you have any questions": 0,
      "related information": 0,
      "educate": 0,
      "education":0
    }
  },
  "SUGGESTIVE": {
    "SUSPICIOUS": {
      "OTHER": {
        "for various reasons": 0,
        "possibility": 0,
        "intention": 0,
        "certain": 0,
        "other data": 0,
        "other purposes": 0,
        "other reasons": 0,
        "other objectives": 0,
        "various purposes": 0,
        "various objectives": 0,
        "if necessary": 0,
        "for business purpose": 0
      }
    },
    "CONDITIONAL": {
      "OTHER": {
        "we may share": 0,
        "for legal reasons": 0,
        "may not cover": 0,
        "only when": 0,
        "only for": 0,
        "only under": 0
      }
    }
  },
  "TECHNOLOGY": {
    "OTHER": {
      "cookies": 0,
      "mobile identifiers": 0,
      "pixel tags": 0,
      "web beacons": 0,
      "session monitoring": 0
    }
  }
}
