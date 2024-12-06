from ...client import ApiClient
from ..connection import PlayerWebSocketHandler

class PlayerConfiguration:
    id: str
    name: str
    unique_name: str
    description: str

class Player:
    def __init__(self, api_client: ApiClient) -> None:
        self.api_client = api_client
        self.websocket_handler = None

    def init_websocket(self, ws_url: str, player_id: str):
        """Initialize WebSocket connection for receiving commands"""
        self.websocket_handler = PlayerWebSocketHandler(
            ws_url=ws_url,
            player_id=player_id,
            api_key=self.api_client.api_key
        )
        return self.websocket_handler

    def get_configuration(self, unique_name: str) -> PlayerConfiguration:
        __response = self.api_client.request("GET", f"players?unique_name={unique_name}")
        return PlayerConfiguration(**__response)
    
    def get_tags(self, player_id: str) -> list[str]:
        __response = self.api_client.request("GET", f"players/{player_id}/tags")
        return __response