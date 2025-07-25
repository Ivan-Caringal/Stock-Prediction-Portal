import { useState, useContext, createContext } from 'react'
const AuthContext = createContext();

const AuthProvidex = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
  return (
    <AuthContext.Provider value={{isLoggedIn, setIsLoggedIn}}>
        {children}
    </AuthContext.Provider>
  )
}

export default AuthProvidex
export {AuthContext};