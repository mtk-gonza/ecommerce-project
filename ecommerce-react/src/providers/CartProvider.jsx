import React, { useState } from 'react'

import { CartContext } from './../context/CartContext.jsx'

export const CartProvider = ({children}) => {
    const [cartItems, setCartItems] = useState([])

    const addToCart = (productToAdd) => {
        const { id, quantity, stock } = productToAdd

        setCartItems(prevItems => {
            const existingItem = prevItems.find(item => item.id === id)

            if (existingItem) {
                const newQuantity = existingItem.quantity + quantity
                if (newQuantity > stock) {
                    alert(`Solo quedan ${stock - existingItem.quantity} disponibles.`)
                    return prevItems
                }
                return prevItems.map(item =>
                    item.id === id ? { ...item, quantity: newQuantity } : item
                )
            } else {
                if (quantity > stock) {
                    alert(`Solo hay ${stock} disponibles.`)
                    return prevItems
                }
                return [...prevItems, { ...productToAdd }]
            }
        })
    }

    const removeFromCart = (product) => {
        setCartItems(prevItems =>
            prevItems.reduce((acc, item) => {
                if (item.id === product.id) {
                    if (item.quantity > 1) {                        
                        acc.push({ ...item, quantity: item.quantity - 1 })
                    }                    
                } else {
                    acc.push(item)
                }
                return acc
            }, [])
        )
    }

    const clearCart = () => {
        setCartItems([])
    }

    return (
        <CartContext.Provider value={{ 
            cartItems, 
            clearCart, 
            addToCart, 
            removeFromCart 
        }}>
            {children}
        </CartContext.Provider>
    )
}