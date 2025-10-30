import {render, screen} from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'

import {WebSocketProvider} from './webSocketProvider'
import {useWebSocket} from './useWebSocket';

describe('useWebSocket hook', ()=>{
    it('should create an error when it is used outside of a WebSocketProvider', ()=>{
        const errorSpy = vi.spyOn(console, 'error').mockImplementation(()=>{});
        const TestComponent = () =>{
            useWebSocket();
            return <div>Test</div>
        }

        expect(()=>render(<TestComponent/>)).toThrow('useWebSocket must be used within a WebSocketProvider');
        errorSpy.mockRestore();
    });
})

describe('WebSocketProvider', ()=>{
    it('should provide the WebSocket instance to its children', ()=>{
        const TestComponent = () => {
            const ws = useWebSocket();
            return (
                <div>
                    <span>WebSocket Status: {ws.connectionStatus}</span>
                    <span>WebSocket Message: {ws.lastMessage ? 'last Message' : 'Vide'}</span>
                    <button onClick={()=>ws.sendMessage('Provider Test')}></button>
                </div>
            );
        };

        render(
            <WebSocketProvider>
                <TestComponent />
            </WebSocketProvider>
        );

    screen.debug();

    const wsStatus = screen.getByText(/WebSocket Status:/);
    expect(wsStatus).toBeInTheDocument();
    expect(wsStatus).toHaveTextContent('WebSocket Status: connecting');

    const wsMessage = screen.getByText(/WebSocket Message:/);
    expect(wsMessage).toBeInTheDocument();
    expect(wsMessage).toHaveTextContent('WebSocket Message: Vide');
    });
})