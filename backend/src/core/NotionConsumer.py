#Consumer using Generic Consumer
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from client.requestNotion import Notion
from server.models import secretKeys
from utils.encryption import decrypt_token


class AsyncNotionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "fetch_tasks":
            await self.send_notion_request(data)

    async def send_notion_request(self, data):
        token = await self.get_decryted_token()

        if token:
            notion_client = Notion(token)
            db_list = notion_client.db_list()
            await self.send(text_data=json.dumps({
                "type": "db_list",
                "data": db_list
            }))
        else:
            await self.send(text_data=json.dumps({
                'status': 'error',
                'message': 'Impossible de récupérer la clé secrète.'
            }))

    @database_sync_to_async
    def get_decryted_token(self):
        try:
            key_object = secretKeys.objects.first()
            if key_object:
                encrypted_key = key_object.secretKey
                return decrypt_token(encrypted_key)
            return None
        except Exception:
            # Gérer les erreurs potentielles (ex: table vide)
            return None
