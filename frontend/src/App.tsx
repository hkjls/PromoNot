import {BrowserRouter as Router, Route, Routes} from 'react-router-dom'
import type { ReactElement } from 'react'
import { NotionKeyProvider } from './context/notionKeyContext'
// import Home from './pages/Home'
import Authorization from './pages/Authorization'

const App=():ReactElement=>{

  return (
    <Router>
      <div className='Signature Contact'>
        Made by RANDRIANJAFY Joelas
      </div>
      <NotionKeyProvider>
        <Routes>
            <Route path="/" element={<Authorization/>} />
        </Routes>
      </NotionKeyProvider>
    </Router>
  )
}

export default App
