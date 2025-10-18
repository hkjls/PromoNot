import {BrowserRouter as Router, Route, Routes} from 'react-router-dom'
import type { ReactElement } from 'react'
import { NotionKeyProvider } from './context/notionKeyContext'
import Home from './pages/Home'
import Authorization from './pages/Authorization'
import { WebSocketProvider } from './context/webSocketProvider'

const App=():ReactElement=>{

  return (
    <Router>
      <div className='Signature Contact'>
        Made by RANDRIANJAFY Joelas
      </div>
      <NotionKeyProvider>
        <WebSocketProvider url="ws://localhost:3000/ws/notion/">
          <Routes>
              <Route path="/" element={<Authorization/>} />
              <Route path="/home" element={<Home/>} />
          </Routes>
        </WebSocketProvider>
      </NotionKeyProvider>
    </Router>
  )
}

export default App
