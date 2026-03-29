import { useState, useEffect } from 'react'

import { RolesContext } from './../context/RolesContext.jsx'

import roleService from './../services/roleService.js'

export const RolesProvider = ({ children }) => {
    const [roles, setRoles] = useState([])
    const [errorRoles, setErrorRoles] = useState(null)
    const [isLoadingRoles, setIsLoadingRoles] = useState(false)

    const actionsRoles = {
        getRoles: async () => {
            setErrorRoles(null)
            setIsLoadingRoles(true)
            try {
                const response = await roleService.getRoles()
                setRoles(response)
                return response
            } catch (err) {
                setErrorRoles(err.message)
                throw err
            } finally {
                setIsLoadingRoles(false)
            }
        },
        getRoleById: async (id) => {
            setErrorRoles(null)
            setIsLoadingRoles(true)
            try {
                const response = await roleService.getRoleById(id)
                return response
            } catch (err) {
                setErrorRoles(err.message)
                throw err
            } finally {
                setIsLoadingRoles(false)
            }            
        },
        addRole: async (newRole) => {
            setErrorRoles(null)
            setIsLoadingRoles(true)            
            try {
                const response = await roleService.createRole(newRole)
                setRoles((prev) => [...prev, response])  
                return response              
            } catch (err) {
                setErrorRoles(err.message)
                throw err    
            } finally {
                setIsLoadingRoles(false)
            }
        },
        updateRole: async (updatedRole) => {
            setErrorRoles(null)
            setIsLoadingRoles(true)
            try {                
                const response = await roleService.updateRole(updatedRole)
                setRoles((prev) =>
                    prev.map((p) => (p.id === response.id ? response : p))
                )
                return response
            } catch (err) {
                setErrorRoles(err.message)
                throw err                
            } finally {
                setIsLoadingRoles(false)
            }
        },
        deleteRole: async (id) => {
            setErrorRoles(null)
            setIsLoadingRoles(true)
            try {                
                const response = await roleService.deleteRole(id);
                setRoles((prev) => prev.filter((r) => r.id !== id))
                return response || true  
            } catch (err) {
                setErrorRoles(err.message)
                throw err  
            } finally {
                setIsLoadingRoles(false)
            }
        }  
    }

    useEffect(() => {
        actionsRoles.getRoles()
    }, [])

    return (
        <RolesContext.Provider value={{
            roles,
            errorRoles,
            isLoadingRoles,
            ...actionsRoles
        }}>
            {children}
        </RolesContext.Provider> 
    )
}