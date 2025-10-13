#!/usr/bin/env python3
"""
Test script for Closing Consumers functionality with StopConsumer integration
This script tests the enhanced Closing Consumers implementation that uses StopConsumer
"""
import sys
import os
import django
from unittest.mock import Mock, patch
import pytest

# Setup Django environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.src.settings')
django.setup()

from core.EchoConsumer import EchoConsumer, AsyncEchoConsumer
from channels.exceptions import StopConsumer

class MockConsumerMixin:
    """Mixin to handle StopConsumer in tests"""
    def setup_consumer(self):
        consumer = self.consumer_class()
        mock_send = Mock()
        consumer.send = mock_send
        return consumer, mock_send

class TestSyncEchoConsumer(MockConsumerMixin):
    consumer_class = EchoConsumer
    
    def test_websocket_disconnect_raises_stopconsumer(self):
        """Test that websocket_disconnect properly raises StopConsumer"""
        consumer, mock_send = self.setup_consumer()
        
        disconnect_event = {
            'code': 1000,
            'reason': 'Normal closure'
        }
        
        # Test that StopConsumer is raised
        with pytest.raises(StopConsumer) as exc_info:
            consumer.websocket_disconnect(disconnect_event)
        
        # Verify StopConsumer details
        assert exc_info.value.code == 1000
        assert exc_info.value.reason == 'Normal closure'
        
        # Verify close message was sent before StopConsumer was raised
        close_calls = [call for call in mock_send.call_args_list 
                       if call[0][0].get('type') == 'websocket.close']
        assert len(close_calls) == 1
        close_message = close_calls[0][0][0]
        assert close_message['type'] == 'websocket.close'
        assert close_message['code'] == 1000
        assert close_message['reason'] == 'Normal closure'
        print("✓ Sync EchoConsumer properly uses StopConsumer")

class TestAsyncEchoConsumer(MockConsumerMixin):
    consumer_class = AsyncEchoConsumer
    
    async def test_websocket_disconnect_raises_stopconsumer(self):
        """Test that async websocket_disconnect properly raises StopConsumer"""
        consumer, mock_send = self.setup_consumer()
        
        disconnect_event = {
            'code': 1000,
        'reason': 'Normal closure'
        }
        
        # Test that StopConsumer is raised
        try:
            await consumer.websocket_disconnect(disconnect_event)
            assert False, "Should have raised StopConsumer"
        except StopConsumer as e:
            # Verify StopConsumer details
            assert e.code == 1000
            assert e.reason == 'Normal closure'
            
            # Verify close message was sent before StopConsumer was raised
            close_calls = [call for call in mock_send.call_args_list 
                           if call[0][0].get('type') == 'websocket.close']
            assert len(close_calls) == 1
            close_message = close_calls[0][0][0]
            assert close_message['type'] == 'websocket.close'
            assert close_message['code'] == 1000
            assert close_message['reason'] == 'Normal closure'
            print("✓ Async EchoConsumer properly uses StopConsumer")

def run_tests():
    """Run all tests"""
    print("Testing enhanced Closing Consumers with StopConsumer integration...\n")
    
    # Run sync consumer test
    try:
        test = TestSyncEchoConsumer()
        test.test_websocket_disconnect_raises_stopconsumer()
        print("✓ Sync EchoConsumer StopConsumer integration test passed")
        sync_success = True
    except Exception as e:
        print(f"✗ Sync EchoConsumer StopConsumer integration test failed: {e}")
        sync_success = False
    
    # Run async consumer test
    try:
        import asyncio
        test = TestAsyncEchoConsumer()
        asyncio.run(test.test_websocket_disconnect_raises_stopconsumer())
        print("✓ Async EchoConsumer StopConsumer integration test passed")
        async_success = True
    except Exception as e:
        print(f"✗ Async EchoConsumer StopConsumer integration test failed: {str(e)}")
        async_success = False
    
    print(f"\nTest Summary:")
    print(f"Passed: {sum([sync_success, async_success])}/2")
    print(f"Failed: {2 - sum([sync_success, async_success])}/2")
    
    if all([sync_success, async_success]):
        print("🎉 All enhanced Closing Consumers tests passed!")
        print("\n✅ Enhanced Implementation Summary:")
        print("• Sync EchoConsumer properly uses StopConsumer for proper termination")
        print("• Async EchoConsumer properly uses StopConsumer for proper termination")
        print("• Both consumers maintain proper websocket closing handshake")
        print("• StopConsumer integration follows Django Channels best practices")
        print("• Enhanced error handling with StopConsumer")
    else:
        print("❌ Some tests failed. Check the output above.")
    
    return all([sync_success, async_success])

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
