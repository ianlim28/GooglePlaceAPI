import pandas as pd 
import requests 
import os
import json
import time 

API_KEY = 'your_api_token'

url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=Museum%20of%20Contemporary%20Art%20Australia&inputtype=textquery&fields=formatted_address,name,rating,opening_hours,geometry&key={}'.format(API_KEY)

currentRequest = requests.get(url = url)

currentRequest.json()


"""
Basic data SKU
address_component, adr_address, formatted_address, geometry, icon, name, permanently_closed, photo, place_id, plus_code, type, url, utc_offset, vicinity
"""

endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
params = {
    'location':'3.146973, 101.615702',
    'radius':'1000',
    'types':'restaurant',
    'key':API_KEY
}

res = requests.get(endpoint_url, params = params)
print('SENT REQUEST:', res.url)
print('REQUEST SUCCESSFUL:', res.ok)
print('REQUEST STATUS:', res.json().get('status'))

results = json.loads(res.content)

places = []
places.extend(results['results'])
time.sleep(2)
while "next_page_token" in results:
    params['pagetoken'] = results['next_page_token'],
    res = requests.get(endpoint_url, params = params)
    results = json.loads(res.content)
    places.extend(results['results'])
    time.sleep(2)
#return places

dfObj = pd.DataFrame(columns=['name', 'rating', 'types','vicinity'])

for i,  place in enumerate(places):
    dfObj.loc[i, 'name'] = place['name']
    try:
        dfObj.loc[i, 'rating'] = place['rating']
    except KeyError:
        pass 
    dfObj.loc[i, 'types'] = place['types']
    dfObj.loc[i, 'vicinity'] = place['vicinity']

dfObj.to_csv('google_data.csv')
