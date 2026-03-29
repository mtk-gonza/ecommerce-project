import { useContext } from 'react'

import { ProductsContext } from './../context/ProductsContext.jsx'

export const useProducts = () => {
    return useContext(ProductsContext)
}