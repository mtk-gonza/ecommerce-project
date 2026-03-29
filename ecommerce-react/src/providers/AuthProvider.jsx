import React, { useState, useEffect } from 'react'

import { AuthContext } from './../context/AuthContext.jsx'

import { login, logout } from './../services/authService.js'

export const AuthProvider = ({ children }) => {
    const [authUser, setAuthUser] = useState(null)
    const [isAuthenticated, setIsAuthenticated] = useState(false)
    const [isLoadingAuthUser, setIsLoadingAuthUser] = useState(true)
    const [errorAuthUser, setErrorAuthUser] = useState(null)

    useEffect(() => {
        const storedUser = localStorage.getItem('user')
        if (storedUser) {
            try {
                const parsedUser = JSON.parse(storedUser)
                setAuthUser(parsedUser)
                setIsAuthenticated(true)
            } catch (err) {
                console.error('Error al parsear usuario almacenado', err)
            }
        }
        setIsLoadingAuthUser(false)
    }, [])

    const handleLogin = async (email, password, remember = false) => {
        setErrorAuthUser(null)
        setIsLoadingAuthUser(true)
        try {
            const reponse = await login(email, password)          
            setAuthUser(reponse)
            setIsAuthenticated(true)
            if (remember) {
                localStorage.setItem('user', JSON.stringify(reponse))

            } else {
                sessionStorage.setItem('user', JSON.stringify(reponse))                
            }
            return reponse
        } catch (err) {
            setErrorAuthUser(err.message || 'Hubo un problema al iniciar sesión')
            throw err
        } finally {
            setIsLoadingAuthUser(false)
        }
    }

    const handleLogout = () => {
        setAuthUser(null)
        setIsAuthenticated(false)
        logout()
    }
    
    return (
        <AuthContext.Provider value={{ 
            authUser, 
            isAuthenticated, 
            isLoadingAuthUser, 
            errorAuthUser, 
            setErrorAuthUser, 
            login: handleLogin,
            logout: handleLogout
        }}>
            {children}
        </AuthContext.Provider>
    )
}