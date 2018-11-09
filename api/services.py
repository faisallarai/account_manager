import json
import requests

def get_items(request):
    url = 'http://localhost:9000/authorize' 
    params = json.loads(request.body)
    r = requests.get('http://localhost:9200/_search', params=params)
    items = r.json()
    return items['results'] # handle exceptions for fail proof design