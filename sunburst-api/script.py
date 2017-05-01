import requests
import json

# helper to open json files
def readJson(fileName):
    with open(fileName) as f:
        return json.loads(f.read())

# load the token
tokenJson = readJson("./suburst-token-credentials.json")
token = tokenJson['token']


# Set the coordinates for our sunset data: Brooklyn (DUMBO), NY
lat = -73.995573
long = 40.7024259

# Assemblu the request
url = 'https://sunburst.sunsetwx.com/v1/quality?type=sunset&coords=' + str(lat) + '%2C' + str(long)
headers = {'Authorization': 'Bearer ' + token}
resp = requests.get(url=url, headers=headers)
data = resp.json()['features']

