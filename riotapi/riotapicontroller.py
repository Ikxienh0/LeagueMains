import urllib.request
import urllib.error
import json

from riotapi_static.staticdto import ChampionListDto
from riotapi_static.staticdto import RealmDto

class RiotApiController:

    def __init__(self, apikey):
        self.apikey = apikey


    """TODO: Rate limitations"""
    def requestbyurl(self, url):
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        content = response.read()
        return content


    def get_realms(self, region="euw"):
        url = "https://global.api.pvp.net/api/lol/static-data/" + region + "/v1.2/realm?api_key=" + self.apikey
        response = self.requestbyurl(url)
        realms = RealmDto(json.loads(response.decode('utf-8')))
        return realms


    def get_championlist(self, region="euw", locale="en_GB", version=None):
        if version:
            url = "https://global.api.pvp.net/api/lol/static-data/" + region + "/v1.2/champion?locale=" + locale + "&version=" + version + "&champData=all&api_key=" + self.apikey
        else:
            url = "https://global.api.pvp.net/api/lol/static-data/" + region + "/v1.2/champion?locale=" + locale + "&champData=all&api_key=" + self.apikey
        response = self.requestbyurl(url)
        champlist = ChampionListDto(json.loads(response.decode('utf-8')))
        return champlist