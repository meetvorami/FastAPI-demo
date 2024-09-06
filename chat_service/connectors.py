from fastapi import WebSocket

class LobbyconnectionManager:
    def __init__(self) -> None:
        self.activte_connection = {}
    
    async def connect(self,websocket:WebSocket):
        await websocket.accept()
    
   