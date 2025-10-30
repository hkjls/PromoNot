import {useState, useEffect, useCallback} from "react";
import type { ReactNode } from "react";
import type { IwebSocketContext } from './webSocketContext';
import { webSocketContext } from './webSocketContext';

export const WebSocketProvider = ({children}: {children: ReactNode})=>{
    const [socket, setSocket] = useState<WebSocket | null>(null);
    const [connectionStatus, setConnectionStatus] = useState<IwebSocketContext['connectionStatus']>('connecting');
    const [lastMessage, setLastMessage] = useState<MessageEvent | null>(null);
    const [url, setURL] = useState<string | null>(null);

    useEffect(()=>{
        if(url){
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
        }

    }, [url])
    const sendMessage = useCallback((message: string) => {
        if (socket && connectionStatus === 'open') {
            socket.send(message);
        } else {
            console.error('WebSocket is not open. Unable to send message.');
        }
    }, [socket, connectionStatus]);
    
    const add_url = (ws_url:string)=>{
        setURL(ws_url)
    }

    const contextValue: IwebSocketContext = {
        connectionStatus,
        lastMessage,
        sendMessage,
        add_url
    }


    return (
        <webSocketContext.Provider value={contextValue}>
            {children}
        </webSocketContext.Provider>
    )
}