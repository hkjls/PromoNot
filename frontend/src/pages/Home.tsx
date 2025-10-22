import type { ReactElement } from 'react';
import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useWebSocket } from '../context/useWebSocket';

const Home=():ReactElement=>{
  const [searchParms] = useSearchParams();
  const [parms, setParms] = useState<string | null>(searchParms.get('userId'))

  const {connectionStatus, lastMessage, sendMessage} = useWebSocket()

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