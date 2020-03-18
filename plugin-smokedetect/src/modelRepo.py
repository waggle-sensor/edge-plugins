import requests
import os
import json
from requests.exceptions import HTTPError

class modelRepo:
    #baseURL = 'https://sage-restapi.nautilus.optiputer.net/api/v1/'
    TOKEN = os.getenv('TOKEN')
    if TOKEN is None:
        raise EnvironmentError("Failed because {} is not set.".format('TOKEN'))
    headers = {'Authorization': 'Bearer {}'.format(TOKEN)}
    def __init__(self, baseURL):
        self.baseURL = baseURL
    
    def getModel(self,bucket,object, directory):
        url = self.baseURL +'buckets' +'/{}/{}'.format(bucket,object)
        payload = {'filePathDest': directory}
        try:
            r = requests.request('GET',url, headers=modelRepo.headers,params=payload)
            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Complete:')
            print(r.text)

    def postModel(self,bucket,filePath):
        url = self.baseURL +'bucket'
        payload = {'bucket':bucket}
        f = open(filePath,'rb')
        files = [('file', f)]
        try:
            r = requests.request('POST',url,headers=modelRepo.headers,params=payload,files=files)
            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            print('Complete:')
            print(r.text)

