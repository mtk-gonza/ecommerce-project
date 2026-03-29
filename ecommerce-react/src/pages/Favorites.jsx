import React from 'react'

import { Main } from './../components/common/Main.jsx'
import { Container } from './../components/common/Container.jsx'
import { Slider } from './../components/layout/Slider.jsx'

import { useProducts } from './../hooks/useProducts.jsx'
import { useFavorites } from './../hooks/useFavorites.jsx'

import './../styles/pages/Favorites.css'

export const Favorites = () => {
    const { products } = useProducts() 
    const { isFavorite } = useFavorites()
    let favoritesProducts = [...products]
    favoritesProducts = favoritesProducts.filter(product => isFavorite(product.id))
    return (
        <Main className='favorites'>
            <Container>
                <Slider products={favoritesProducts} title='Mis Favoritos'/>
            </Container>
        </Main>
    )
}