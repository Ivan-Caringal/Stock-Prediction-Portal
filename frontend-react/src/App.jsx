import { useState } from 'react'
import './assets/css/style.css'
import Header from './components/Header'
import Footer from './components/Footer'
import Main from './components/Main'
import Register from './components/Register'
import Login from './components/Login'
import Test1 from './components/test1'
import { BrowserRouter, Routes, Route } from "react-router-dom"
import AuthProvider from './AuthProvider'
import Dashboard from './components/dashboard/Dashboard'

import PublicRoute from './PublicRoute'
import PrivateRoute from './Privateroute'

function App() {
  
  return (
    <>
    <AuthProvider>
      <BrowserRouter>
      <Header />
      <Routes>
        <Route path='/' element={<Main />} />
        <Route path='/register' element={<PublicRoute><Register /></PublicRoute>} />
        <Route path='/login' element={<PublicRoute><Login /></PublicRoute>} />
        <Route path='/dashboard' element={<PrivateRoute><Dashboard /></PrivateRoute>} />
      </Routes>
      <Footer />
      </BrowserRouter>
    </AuthProvider>
  
    </>
  )
}

export default App
