import { useContext } from "react";
import { WebSocketContext } from "./webSocketContext";
import type { IwebSocketContext } from "./webSocketContext";

export const useWebSocket = (): IwebSocketContext => {
    const context = useContext(WebSocketContext);
    if (!context) {
        throw new Error('useWebSocket must be used within a WebSocketProvider');
    }
    return context;
};