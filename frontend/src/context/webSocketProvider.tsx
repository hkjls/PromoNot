import {useState, useEffect, useCallback} from "react";
import type { ReactNode } from "react";
import type { IwebSocketContext } from './webSocketContext';
import { webSocketContext } from './webSocketContext';

interface WebSocketProviderProps {
    url: string;
    children: ReactNode;
}

export const WebSocketProvider = ({url, children}: WebSocketProviderProps)=>{
    const [socket, setSocket] = useState<WebSocket | null>(null);
    const [connectionStatus, setConnectionStatus] = useState<IwebSocketContext['connectionStatus']>('connecting');
    const [lastMessage, setLastMessage] = useState<MessageEvent | null>(null);

    useEffect(()=>{
        const newSocket = new WebSocket(url);
        setConnectionStatus('connecting')

        newSocket.onopen = () =>{
            setConnectionStatus('open')
        }

        newSocket.onmessage = (event) =>{
            setLastMessage(event);

        }

        newSocket.onclose = ()=>{
            setConnectionStatus('closed');
        }

        newSocket.onerror = () =>{
            setConnectionStatus('closed')
        }

        setSocket(newSocket)

        return () => {
            newSocket.close();
        }

    }, [url])
    const sendMessage = useCallback((message: string) => {
        if (socket && connectionStatus === 'open') {
            socket.send(message);
        } else {
            console.error('WebSocket is not open. Unable to send message.');
        }
    }, [socket, connectionStatus]);
    
    const contextValue: IwebSocketContext = {
        connectionStatus,
        lastMessage,
        sendMessage
    }

    return (
        <webSocketContext.Provider value={contextValue}>
            {children}
        </webSocketContext.Provider>
    )
}