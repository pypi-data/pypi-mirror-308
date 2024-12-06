from .client import ApiClient
from .api.player import Player

class ShifIQ:
    def __init__(self, api_key: str, base_url: str = "https://api.shifiq.com", api_version: str = "v1"):
        self.__api_client = ApiClient(api_key=api_key, base_url=base_url, api_version=api_version)
        self.player = Player(self.__api_client) 