import { useContext } from 'react'

import { CategoriesContext } from './../context/CategoriesContext.jsx'

export const useCategories = () => {
    return useContext(CategoriesContext)
}