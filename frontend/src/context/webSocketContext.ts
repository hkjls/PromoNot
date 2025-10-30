import { createContext } from 'react';

export interface IwebSocketContext {
    connectionStatus:'connecting' | 'open' | 'closed';
    lastMessage: MessageEvent | null;
    sendMessage: (message: string) => void;
    add_url:(ws_url:string)=>void;
}

export const webSocketContext = createContext<IwebSocketContext | null>(null)