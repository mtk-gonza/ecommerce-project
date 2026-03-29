import { useContext } from 'react'

import { FavoritesContext } from './../context/FavoritesContext.jsx'

export const useFavorites = () => {
    return useContext(FavoritesContext)
}