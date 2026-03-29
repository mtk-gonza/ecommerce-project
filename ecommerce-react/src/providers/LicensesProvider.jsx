import React, { useState, useEffect } from 'react'

import { LicensesContext } from './../context/LicensesContext.jsx'

import licenseService from './../services/licenseService.js'

export const LicensesProvider = ({ children }) => {
    const [licenses, setLicenses] = useState([])
    const [errorLicenses, setErrorLicenses] = useState(null)
    const [isLoadingLicenses, setIsLoadingLicenses] = useState(false)

    const actonsLicenses = {
        getLicenses: async () => {
            setErrorLicenses(null)
            setIsLoadingLicenses(true)
            try {
                const response = await licenseService.getLicenses()
                setLicenses(response)
                return response
            } catch (err) {
                setErrorLicenses(err.message)
                throw err
            } finally {
                setIsLoadingLicenses(false)
            }
        },
        getLicenseById: async (id) => {
            setErrorLicenses(null)
            setIsLoadingLicenses(true)
            try {
                const response = await licenseService.getLicenseById(id)
                return response
            } catch (err) {
                setErrorLicenses(err.message)
                throw err
            } finally {
                setIsLoadingLicenses(false)
            }            
        },
        addLicense: async (newLicense) => {
            setErrorLicenses(null)
            setIsLoadingLicenses(true)
            try {
                const response = await licenseService.createLicense(newLicense)
                setLicenses((prev) => [...prev, response])  
                return response               
            } catch (err) {
                setErrorLicenses(err.message)
                throw err
            } finally {
                setIsLoadingLicenses(false)
            }
        },
        updateLicense: async (updatedProduct) => {
            setErrorLicenses(null)
            setIsLoadingLicenses(true)
            try {                
                const response = await licenseService.updateLicense(updatedProduct)
                setLicenses((prev) =>
                    prev.map((p) => (p.id === response.id ? response : p))
                )
                return response
            } catch (err) {
                setErrorLicenses(err.message)
                throw err               
            } finally {
                setIsLoadingLicenses(false)
            }
        },
        deleteLicense: async (id) => {
            setErrorLicenses(null)
            setIsLoadingLicenses(true)
            try {                
                const response = await licenseService.deleteLicense(id);
                setLicenses((prev) => prev.filter((p) => p.id !== id))
                return response || true 
            } catch (err) {
                setErrorLicenses(err.message)
                throw err 
            } finally {
                setIsLoadingLicenses(false)
            }
        }        
    }

    useEffect(() => {
        actonsLicenses.getLicenses()
    }, [])

    return (
        <LicensesContext.Provider value={{ 
            licenses, 
            errorLicenses, 
            isLoadingLicenses,
            ...actonsLicenses 
        }}>
            {children}
        </LicensesContext.Provider>
    )
}