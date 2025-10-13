#Consumer using Generic Consumer

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer


class NotionConsumer(WebsocketConsumer):
    groups = ["notion"]
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.send(text_data=text_data)


class AsyncNotionConsumer(AsyncWebsocketConsumer):
    groups = ["notion"]
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=text_data)  # noqa: W292
