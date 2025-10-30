import type { ReactElement } from 'react';
import { useState,useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useWebSocket } from '../context/useWebSocket';

const Home=():ReactElement=>{
  const [searchParms] = useSearchParams();
  const [parms, setParms] = useState<string | null>(searchParms.get('userId'))

  const {connectionStatus, lastMessage, sendMessage, add_url} = useWebSocket()

  useEffect(()=>{
    add_url(import.meta.env.VITE_WEBSOCKET_URL)
  })

  const handleSendMessage=()=>{
    sendMessage(JSON.stringify({action: "fetch_tasks", user_id:parms}))
    setParms(parms)
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