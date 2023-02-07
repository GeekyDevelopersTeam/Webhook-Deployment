import requests
import json

url = "your url/webhook"
data = { 'name': 'Vaibhav Ji', 
         'Just Testing': 'Hello World' }
r = requests.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})