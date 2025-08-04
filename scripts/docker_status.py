#!/bin/python3
import requests
import json

### Google 
url = "http://localhost:8191/v1"
headers = {"Content-Type": "application/json"}
data = {
    "cmd": "request.get",
    "url": "http://www.google.com/",
    "maxTimeout": 60000
}
response = requests.post(url, headers=headers, json=data)
#print(response.text)

### List Sessions
url = "http://localhost:8191/v1"
headers = {"Content-Type": "application/json"}
data = {
    "cmd": "sessions.list",
    "url": url,
    "maxTimeout": 60000
}
response = requests.post(url, headers=headers, json=data)
response_data    = json.loads(response.content)
print(json.dumps(response_data,indent=4))