import pytest
from channels.testing import WebsocketCommunicator
from django.test import TestCase

from core.notionConsumer import AsyncNotionConsumer


class NotionConsumerTests(TestCase):

    async def test_notion_consumer_flow(self):
        communicator = WebsocketCommunicator(AsyncNotionConsumer.as_asgi(), "/ws/notion/")  # noqa: E501
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        await communicator.send_json_to({"action": "test_action", "data": "test_data"})
        response = await communicator.receive_json_from()
        self.assertEqual(response, {"status": "received", "data": "test_data"})

        await communicator.disconnect()
