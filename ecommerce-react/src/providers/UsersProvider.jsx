import { useState, useEffect } from 'react'

import { UsersContext } from './../context/UsersContext.jsx'
import userService from './../services/userService.js'

export const UsersProvider = ({ children }) => {
    const [users, setUsers] = useState([])
    const [errorUsers, setErrorUsers] = useState(null)
    const [isLoadingUsers, setIsLoadingUsers] = useState(false)

    const actionsUsers = {
        getUsers: async () => {
            setErrorUsers(null)
            setIsLoadingUsers(true)
            try {
                const response = await userService.getUsers()
                setUsers(response)
                return response
            } catch (err) {
                setErrorUsers(err.message)
                throw err
            } finally {
                setIsLoadingUsers(false)
            }
        },
        getUserById: async (id) => {
            setErrorUsers(null)
            setIsLoadingUsers(true)
            try {
                const response = await userService.getUserById(id)
                return response
            } catch (err) {
                setErrorUsers(err.message)
                throw err
            } finally {
                setIsLoadingUsers(false)
            }
        },
        addUser: async (newUser) => {
            setErrorUsers(null)
            setIsLoadingUsers(true)
            try {
                const response = await userService.createUser(newUser)
                setUsers((prev) => [...prev, response])
                return response
            } catch (err) {
                setErrorUsers(err.message)
                throw err
            } finally {
                setIsLoadingUsers(false)
            }
        },
        updateUser: async (updatedUser) => {
            setErrorUsers(null)
            setIsLoadingUsers(true)
            try {
                const response = await userService.updateUser(updatedUser)
                setUsers((prev) =>
                    prev.map((p) => (p.id === response.id ? response : p))
                )
                return response                
            } catch (err) {
                setErrorUsers(err.message)
                throw err
            } finally {
                setIsLoadingUsers(false)
            }
        },
        deleteUser: async (id) => {
            setErrorUsers(null)
            setIsLoadingUsers(true)
            try {
                const response = await userService.deleteUser(id)
                setUsers((prev) => prev.filter((u) => u.id !== id))  
                return response || true              
            } catch (err) {
                setErrorUsers(err.message)
                throw err
            } finally {
                setIsLoadingUsers(false)
            }
        }
    }

    useEffect(() => {
        actionsUsers.getUsers()
    }, [])

    return (
        <UsersContext.Provider value={{
            users,
            errorUsers,
            isLoadingUsers,
            ...actionsUsers
        }}>
            {children}
        </UsersContext.Provider>
    )
}