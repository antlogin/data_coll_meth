import requests
import json
from pprint import pprint
service = 'https://api.github.com/users/antlogin/repos'
params = '-H "Accept: application/vnd.github.v3+json'
req = requests.get(service, params=params)
data = req.json()
for i in range(0, len(data)):
    pprint(data[i].get('name'))


