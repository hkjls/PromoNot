#!/usr/bin/env python3
"""
Test script for verifying Closing Consumers functionality in EchoConsumer
"""
import asyncio
import websockets
import json
import threading
import time
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import Django settings to configure the environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

import django
django.setup()

from channels.routing import URLRouter
from django.urls import path
from core.EchoConsumer import EchoConsumer, AsyncEchoConsumer

# Create a simple routing configuration for testing
application = URLRouter([
    path('ws/echo/', EchoConsumer.as_asgi()),
    path('ws/async_echo/', AsyncEchoConsumer.as_asgi()),
])

def run_server():
    """Run the ASGI server for testing"""
    import uvicorn
    uvicorn.run(application, host="127.0.0.1", port=8000, log_level="info")

async def test_sync_consumer_closure():
    """Test the synchronous EchoConsumer closure"""
    print("Testing Sync EchoConsumer closure...")
    
    try:
        # Connect to the server
        async with websockets.connect('ws://127.0.0.1:8000/ws/echo/') as websocket:
            # Send a test message
            await websocket.send("Hello, Sync Consumer!")
            response = await websocket.recv()
            print(f"Received: {response}")
            
            # Test normal closure
            await websocket.close(code=1000, reason="Normal closure")
            
            # Wait a bit to see the closure logs
            await asyncio.sleep(1)
            
        print("✓ Sync EchoConsumer closure test passed")
        return True
        
    except Exception as e:
        print(f"✗ Sync EchoConsumer closure test failed: {e}")
        return False

async def test_async_consumer_closure():
    """Test the asynchronous EchoConsumer closure"""
    print("Testing Async EchoConsumer closure...")
    
    try:
        # Connect to the server
        async with websockets.connect('ws://127.0.0.1:8000/ws/async_echo/') as websocket:
            # Send a test message
            await websocket.send("Hello, Async Consumer!")
            response = await websocket.recv()
            print(f"Received: {response}")
            
            # Test normal closure
            await websocket.close(code=1000, reason="Normal closure")
            
            # Wait a bit to see the closure logs
            await asyncio.sleep(1)
            
        print("✓ Async EchoConsumer closure test passed")
        return True
        
    except Exception as e:
        print(f"✗ Async EchoConsumer closure test failed: {e}")
        return False

async def test_abnormal_closure():
    """Test abnormal closure scenarios"""
    print("Testing abnormal closure scenarios...")
    
    try:
        # Test with abnormal closure code
        async with websockets.connect('ws://127.0.0.1:8000/ws/echo/') as websocket:
            await websocket.send("Testing abnormal closure")
            await websocket.recv()
            
            # Close with abnormal code
            await websocket.close(code=1006, reason="Abnormal closure")
            await asyncio.sleep(1)
            
        print("✓ Abnormal closure test passed")
        return True
        
    except Exception as e:
        print(f"✗ Abnormal closure test failed: {e}")
        return False

async def main():
    """Main test function"""
    print("Starting Closing Consumers tests...\n")
    
    # Start the server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    await asyncio.sleep(2)
    
    # Run tests
    results = []
    results.append(await test_sync_consumer_closure())
    results.append(await test_async_consumer_closure())
    results.append(await test_abnormal_closure())
    
    # Print summary
    print(f"\nTest Summary:")
    print(f"Passed: {sum(results)}/{len(results)}")
    print(f"Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All Closing Consumers tests passed!")
    else:
        print("❌ Some tests failed. Check the output above.")

if __name__ == "__main__":
    # Install websockets if not available
    try:
        import websockets
    except ImportError:
        print("Installing websockets package...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets"])
        import websockets
    
    # Install uvicorn if not available
    try:
        import uvicorn
    except ImportError:
        print("Installing uvicorn package...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "uvicorn"])
        import uvicorn
    
    asyncio.run(main())
