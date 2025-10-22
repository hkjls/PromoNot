import {BrowserRouter as Router, Route, Routes} from 'react-router-dom'
import type { ReactElement } from 'react'
import { NotionKeyProvider } from './context/notionKeyProvider'
import Home from './pages/Home'
import Authorization from './pages/Authorization'
import { WebSocketProvider } from './context/webSocketProvider';

const App=():ReactElement=>{

  return (
    <Router>
      <div className='Signature Contact'>
        Made by RANDRIANJAFY Joelas
      </div>
      <WebSocketProvider url = {import.meta.env.REACT_APP_API_URL}>
        
        <NotionKeyProvider>
          <Routes>
              <Route path="/" element={<Authorization/>} />
              <Route path="/home" element={<Home/>} />
          </Routes>
        </NotionKeyProvider>

      </WebSocketProvider>
    </Router>
  )
}

export default App
