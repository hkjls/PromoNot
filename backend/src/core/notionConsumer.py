import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from client.requestNotion import Notion
from server.models import secretKeys
from utils.encrypt import decrypt_token


class AsyncNotionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'notion_updates_{self.user_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_data):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "fetch_tasks":
            await self.notion_requestf(data)

    async def notion_update_event(self, event):
        message_data = event['data']

        await self.send(text_data=json.dumps({
            'type':'notion_update',
            'payload':message_data
        }))

    async def notion_requestf(self, data):

        token = await self.get_decrypted_token(data.get("user_id"))

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
    def get_decrypted_token(self, primary_key = ""):
        try:
            key_object = secretKeys.objects.get(id=primary_key)
            if key_object:
                encrypted_key = key_object.secretKey
                return decrypt_token(encrypted_token=encrypted_key)
            return None
        except Exception:
            return None
