#Basic Layout
from channels.consumer import AsyncConsumer, SyncConsumer
from channels.exceptions import StopConsumer


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
        self.close_consumer(event)

    def close_consumer(self, event):
        """
        Properly close the consumer connection.
        This method handles the closing handshake and cleanup.
        """
        close_code = event.get('code', 1000)  # Default normal closure
        close_reason = event.get('reason', '')

        # Log the closure for debugging
        print(f"Consumer closing: code={close_code}, reason={close_reason}")

        # Perform any cleanup operations here
        self.cleanup_resources()

        # Send close message if not already sent
        try:
            self.send({
                "type": "websocket.close",
                "code": close_code,
                "reason": close_reason
            })
            # Use StopConsumer to properly terminate the consumer
            raise StopConsumer(close_code, close_reason)
        except Exception as e:
            # Connection might already be closed
            print(f"Error sending close message: {e}")
            # Still raise StopConsumer for proper termination
            raise StopConsumer(close_code, close_reason)

    def cleanup_resources(self):
        """
        Clean up any resources associated with this consumer.
        Override this method in subclasses for specific cleanup needs.
        """
        # Example: Remove from groups, close database connections, etc.
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
        # Handle consumer closure - clean up resources
        await self.close_consumer(event)

    async def close_consumer(self, event):
        """
        Properly close the async consumer connection.
        This method handles the closing handshake and cleanup.
        """
        close_code = event.get('code', 1000)  # Default normal closure
        close_reason = event.get('reason', '')

        # Log the closure for debugging
        print(f"Async Consumer closing: code={close_code}, reason={close_reason}")

        # Perform any cleanup operations here
        await self.cleanup_resources()

        # Send close message if not already sent
        try:
            await self.send({
                "type": "websocket.close",
                "code": close_code,
                "reason": close_reason
            })
            # Use StopConsumer to properly terminate the consumer
            raise StopConsumer(close_code, close_reason)
        except Exception as e:
            # Connection might already be closed
            print(f"Error sending close message: {e}")
            # Still raise StopConsumer for proper termination
            raise StopConsumer(close_code, close_reason)

    async def cleanup_resources(self):
        """
        Clean up any resources associated with this async consumer.
        Override this method in subclasses for specific cleanup needs.
        """
        # Example: Remove from groups, close database connections, etc.
        pass
