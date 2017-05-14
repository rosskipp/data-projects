import requests
import json
from twilio.rest import Client

"""
helper function to open json files
"""
def readJson(fileName):
    with open(fileName) as f:
        return json.loads(f.read())
        
"""
helper to save a json file
"""
def saveJson(filename, jsonData):
    with open(fileName, 'w') as f:
        json.dump(jsonData, f)

"""
SUNSET WX
The output of the /login endpoint is saved to a file called "suburst-token-credentials.json"
and gitignored.
My login credentials are in a file called sunburst-credentials.json
"""
loginCreds = readJson('sunburst-credentials.json')
loginUrl = "https://sunburst.sunsetwx.com/v1/login"
resp = requests.post(url=loginUrl, data={'email': loginCreds['email'], 'password':loginCreds['password']})
saveJson('sunburst-token-credentials.json', resp.json())

# load the token
tokenJson = readJson("./sunburst-token-credentials.json")
token = tokenJson['token']

# Set the coordinates for our sunset data: Brooklyn (DUMBO), NY
# I got these coordinates from google maps
lat = -73.995573
long = 40.7024259

# Assemble the request
url = 'https://sunburst.sunsetwx.com/v1/quality?type=sunset&coords=' + str(lat) + '%2C' + str(long)
headers = {'Authorization': 'Bearer ' + token}
resp = requests.get(url=url, headers=headers)
data = resp.json()['features']
quality = data[0]['properties']['quality']
quality_percent = data[0]['properties']['quality_percent']

"""
TWILIO
The twilio credentials are saved in a file called "twilio-credentials.json"
and gitignored. And my phone numbers are in phone-credentials.json
"""
twilioCreds = readJson("./twilio-credentials.json")
phoneNumbers = readJson("./phone-credentials.json")
account_sid = twilioCreds['sid']
auth_token = twilioCreds['token']
myPhone = phoneNumbers['my_number']
twilioPhone = phoneNumbers['twilio_number']
client = Client(account_sid, auth_token)

messageText = "Sky quality: " + str(quality) + ". Percent: " + str(quality_percent)

message = client.api.account.messages.create(
    to=myPhone,
    from_=twilioPhone,
    body=messageText)
