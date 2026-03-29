import React, { useState, useEffect } from 'react'

import { FavoritesContext } from './../context/FavoritesContext.jsx'

import { useAuth } from './../hooks/useAuth.jsx'

export const FavoritesProvider = ({ children }) => {
    const { user } = useAuth()
    const [favoriteProductIds, setFavoriteProductIds] = useState([])

    useEffect(() => {
        if (!user?.id) return
        const saved = localStorage.getItem(`favorites_${user.id}`)
        try {
            const parsed = JSON.parse(saved)
            setFavoriteProductIds(Array.isArray(parsed) ? parsed : [])
        } catch (e) {
            console.error('Error parsing favorites from localStorage', e)
            setFavoriteProductIds([])
        }
    }, [user?.id])

    useEffect(() => {
        if (!user?.id) return
        localStorage.setItem(`favorites_${user.id}`, JSON.stringify(favoriteProductIds))
    }, [favoriteProductIds, user?.id])

    const toggleFavorite = (productId) => {
        setFavoriteProductIds(prev => {
            const current = Array.isArray(prev) ? prev : []
            return current.includes(productId)
                ? current.filter(id => id !== productId)
                : [...current, productId]
        })
    }

    const isFavorite = (productId) => {
        return favoriteProductIds.includes(productId)
    }

    return (
        <FavoritesContext.Provider value={{ 
            favoriteProductIds, 
            toggleFavorite, 
            isFavorite 
        }}>
            {children}
        </FavoritesContext.Provider>
    )
}