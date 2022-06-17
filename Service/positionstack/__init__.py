import requests
import json
from backend.settings import PS_ACCESS_TOKEN
import http.client, urllib.parse


def forward(address:str):
    
    conn = http.client.HTTPConnection('api.positionstack.com')
    params = urllib.parse.urlencode({
    'access_key':PS_ACCESS_TOKEN ,
    'query': address,
    'limit': 1,
    })
    conn.request('GET', '/v1/forward?{}'.format(params))
    res = conn.getresponse()
    data = res.read()
    
    return json.loads(data.decode('utf-8'))
    # url = 'http://api.positionstack.com/v1/forward?access_key ={}&query={}'.format(PS_ACCESS_TOKEN, address)
    # data = requests.get(url)

    # return data

def reverse(lat,lng):
    conn = http.client.HTTPConnection('api.positionstack.com')

    params = urllib.parse.urlencode({
        'access_key': PS_ACCESS_TOKEN,
        'query': '51.507822,-0.076702',
        })

    conn.request('GET', '/v1/reverse?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    return json.loads(data.decode('utf-8'))
    # url = 'http://api.positionstack.com/v1/reverse?access_key={}& query={},{}'.format(PS_ACCESS_TOKEN,lat,lng)
    # data = requests.get(url)
    # return data