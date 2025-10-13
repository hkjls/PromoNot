#Basic Layout
from channels.consumer import AsyncConsumer, SyncConsumer


class EchoConsumer(SyncConsumer):
    def websocket_connect(self, event): # websocket.connect
        self.send({
            "type": "websocket.accept"
        })

    def websocket_receive(self, event): # websocket.receive
        message = event.get('text', '')
        self.send({
            "type": "websocket.send",
            "text": message
        })

    def websocket_disconnect(self, event):
        pass


class AsyncEchoConsumer(AsyncConsumer):
    async def websocket_connect(self, event): # websocket.connect
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event): # websocket.receive
        message = event.get('text', '')
        await self.send({
            "type": "websocket.send",
            "text": message
        })

    async def websocket_disconnect(self, event):
        pass
