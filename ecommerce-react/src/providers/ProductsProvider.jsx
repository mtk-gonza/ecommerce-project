import React, { useState, useEffect } from 'react'

import { ProductsContext } from './../context/ProductsContext.jsx'

import productService from './../services/productService.js'

import { news } from './../utils/newsUtils.js'

export const ProductsProvider = ({ children }) => {
    const [products, setProducts] = useState([])
    const [latestReleases, setLatestReleases] = useState([])
    const [errorProducts, setErrorProducts] = useState(null)
    const [isLoadingProducts, setIsLoadingProducts] = useState(false)

    const actionsProducts = {
        getProducts: async () => {
            setErrorProducts(null)
            setIsLoadingProducts(true)
            try {
                const response = await productService.getProducts()
                setProducts(response)
                return response
            } catch (err) {
                setErrorProducts(err.message)
                throw err
            } finally {
                setIsLoadingProducts(false)
            }
        },
        getLatestRealses: async () => {
            setErrorProducts(null)
            setIsLoadingProducts(true)
            try {
                const response = await productService.getProducts()
                const releases = response.filter(product => news(product.created_at, 30))
                setLatestReleases(releases)
                return releases
            } catch (err) {
                setErrorProducts(err.message)
                throw err
            } finally {
                setIsLoadingProducts(false)
            }
        },
        getProductById: async (id) => {
            setErrorProducts(null)
            setIsLoadingProducts(true)
            try {
                const response = await productService.getProductById(id)
                return response
            } catch (err) {
                setErrorProducts(err.message)
                throw err
            } finally {
                setIsLoadingProducts(false)
            }            
        },
        addProduct: async (newProduct) => {
            setErrorProducts(null)
            setIsLoadingProducts(true)
            try {
                const response = await productService.createProduct(newProduct)
                setProducts((prev) => [...prev, response]) 
                setLatestReleases((prev) => [...prev, response])  
                return response             
            } catch (err) {
                setErrorProducts(err.message)
                throw err
            } finally {
                setIsLoadingProducts(false)
            }
        },
        updateProduct: async (updatedProduct) => {
            setErrorProducts(null)
            setIsLoadingProducts(true)
            try {                
                const response =  await productService.updateProduct(updatedProduct)
                setProducts((prev) =>
                    prev.map((p) => (p.id === response.id ? response : p))
                )
                return response
            } catch (err) {
                setErrorProducts(err.message)
                throw err               
            } finally {
                setIsLoadingProducts(false)
            }
        },
        deleteProduct: async (id) => {
            setErrorProducts(null)
            setIsLoadingProducts(true)
            try {                
                const response = await productService.deleteProduct(id);
                setProducts((prev) => prev.filter((p) => p.id !== id))
                return response || true  
            } catch (err) {
                setErrorProducts(err.message)
                throw err  
            } finally {
                setIsLoadingProducts(false)
            }
        }
    }

    useEffect(() => {
        actionsProducts.getProducts()
        actionsProducts.getLatestRealses()
    }, [])

    return (
        <ProductsContext.Provider value={{
            products,
            latestReleases,
            errorProducts,
            isLoadingProducts,
            ...actionsProducts
        }}>
            {children}
        </ProductsContext.Provider>
    )
}