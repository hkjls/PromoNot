import { useContext } from "react"
import { webSocketContext } from "./webSocketContext"

export const useWebSocket = () =>{
    const context = useContext(webSocketContext);
    if (!context){
        throw new Error('useWebSocket must be used within a WebSocketProvider');
    }
    return context;
}