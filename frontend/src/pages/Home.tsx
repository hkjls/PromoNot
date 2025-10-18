import type { ReactElement } from 'react';
import { useWebSocket } from '../context/useWebSocket';

const Home=():ReactElement=>{
  const { connectionStatus, lastMessage, sendMessage } = useWebSocket();

  const handleSendMessage = ()=>{
    sendMessage(JSON.stringify({ action: "fetch_tasks" }));
  }
  return (
    <div>
      <h3>Status : {connectionStatus}</h3>
      <h3>Last Message : {lastMessage ? lastMessage.data : 'No message received yet'}</h3>
      <button onClick={handleSendMessage} disabled={connectionStatus !== 'open'}>
        Send Message
      </button>
    </div>
  )
}

export default Home;