import requests
import constants as const
import apiKey as apk

url = const.SCAN_URL
API_KEY = apk.getAPIKey()

#Calling the scan URL
payload = { "url": "br-icloud.com.br/" }
headers = {
    "accept": "application/json",
    "x-apikey": API_KEY,
    "content-type": "application/x-www-form-urlencoded"
}
response = requests.post(url, data=payload, headers=headers)

print(response.text)


