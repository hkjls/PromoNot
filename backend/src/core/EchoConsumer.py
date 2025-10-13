#Basic Layout
from channels.consumer import SyncConsumer


class EchoConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({
            "type": "websocket.accept"
        })

    def websocket_receive(self, event):
        message = event.get('text', '')
        self.send({
            "type": "websocket.send",
            "text": message
        })

    def websocket_disconnect(self, event):
        pass
