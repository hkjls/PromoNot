#!/usr/bin/env python3
"""
Simple verification script for StopConsumer integration
This script verifies the enhanced Closing Consumers implementation with StopConsumer
"""
import sys
import os
import django
from unittest.mock import Mock

# Setup Django environment
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.src.settings')
django.setup()

from core.EchoConsumer import EchoConsumer, AsyncEchoConsumer
from channels.exceptions import StopConsumer

def test_sync_consumer_stopconsumer():
    """Test that sync consumer properly raises StopConsumer"""
    print("Testing Sync EchoConsumer StopConsumer integration...")
    
    consumer = EchoConsumer()
    mock_send = Mock()
    consumer.send = mock_send
    
    disconnect_event = {
        'code': 1000,
        'reason': 'Normal closure'
    }
    
    try:
        consumer.websocket_disconnect(disconnect_event)
        print("✗ Sync EchoConsumer should have raised StopConsumer")
        return False
    except StopConsumer as e:
        # Verify StopConsumer details
        print(f"✓ Sync EchoConsumer raised StopConsumer with code={e.code}, reason='{e.reason}'")
        
        # Verify close message was sent before StopConsumer was raised
        close_calls = [call for call in mock_send.call_args_list 
                       if call[0][0].get('type') == 'websocket.close']
        if close_calls:
            close_message = close_calls[0][0][0]
            print(f"✓ Sync EchoConsumer sent close message: {close_message}")
            return True
        else:
            print("✗ Sync EchoConsumer failed to send close message")
            return False

def test_async_consumer_stopconsumer():
    """Test that async consumer properly raises StopConsumer"""
    print("Testing Async EchoConsumer StopConsumer integration...")
    
    consumer = AsyncEchoConsumer()
    mock_send = Mock()
    consumer.send = mock_send
    
    disconnect_event = {
        'code': 1000,
        'reason': 'Normal closure'
    }
    
    try:
        import asyncio
        async def run_test():
            await consumer.websocket_disconnect(disconnect_event)
            return False
        result = asyncio.run(run_test())
        print("✗ Async EchoConsumer should have raised StopConsumer")
        return False
    except StopConsumer as e:
        print(f"✓ Async EchoConsumer raised StopConsumer with code={e.code}, reason='{e.reason}'")
        
        # Verify close message was sent before StopConsumer was raised
        close_calls = [call for call in mock_send.call_args_list 
                       if call[0][0].get('type') == 'websocket.close']
        if close_calls:
            close_message = close_calls[0][0][0]
            print(f"✓ Async EchoConsumer sent close message: {close_message}")
            return True
        else:
            print("✗ Async EchoConsumer failed to send close message")
            return False

def main():
    """Run all tests"""
    print("Verifying enhanced Closing Consumers with StopConsumer integration...\n")
    
    # Run sync consumer test
    sync_success = test_sync_consumer_stopconsumer()
    
    # Run async consumer test
    async_success = test_async_consumer_stopconsumer()
    
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
        print("• StopConsumer ensures proper consumer termination")
    else:
        print("❌ Some tests failed. Check the output above.")
    
    return all([sync_success, async_success])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
