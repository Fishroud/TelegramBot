import requests
import json
import urllib.parse
import configparser

class ApiCaller:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self, endpoint):
        url = f'{self.base_url}/{endpoint}'
        headers = {}        
        response = response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            return response.text
        else:
            return None

class Api:
    def __init__(self, fpath, config_path='./config.ini'):
        if type(config_path) == str:
            self.config = configparser.ConfigParser()
            self.config.read(config_path)
        elif type(self.config) == configparser.ConfigParser:
            self.config = config_path
        

        self.base_url = self.config['MYSQL']['servername']
        self.path = self.config['MYSQL'][fpath]
        self.api_caller = ApiCaller(self.base_url + self.path)


    def bind_user_info(self, userid, nickname, steamid):
        params = {
            'qq': userid,
            'steamid': steamid,
            'nickname': nickname
        }
        url_params = urllib.parse.urlencode(params)
        return self.api_caller.get_data(f'{self.base_url}?{url_params}')
    
    def GetsteamRecentlyPlayedGames(self, nickname):
        params = {
            'nickname': nickname
        }
        url_params = urllib.parse.urlencode(params)
        return json.loads(self.api_caller.get_data(f'{self.base_url}?{url_params}'))
    
if __name__ == "__main__":
    api = Api('GetsteamRecentlyPlayedGames_path')
    response = api.GetsteamRecentlyPlayedGames('鱼仙')
    print(response)
    print(type(response))



