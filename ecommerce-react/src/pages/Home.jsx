import React from 'react'

import { Main } from './../components/common/Main.jsx'
import { Hero } from './../components/layout/Hero.jsx'
import { Collection } from './../components/layout/Collection.jsx'
import { Container } from './../components/common/Container.jsx'
import { Slider } from './../components/layout/Slider.jsx'

import { useLicenses } from '../hooks/useLicenses.jsx'
import { useProducts } from './../hooks/useProducts.jsx'
import { useCart } from './../hooks/useCart.jsx'

import './../styles/pages/Home.css'

export const Home = () => {
    const { licenses } = useLicenses()
    const { latestReleases } = useProducts()
    const { addToCart } = useCart()

    return (
        <Main className='home'>
            <Hero />
            <Container>                
            {licenses.map((license, index) => (
                <Collection
                    key={license.id}
                    license={license}
                    nameClass={index % 2 === 0 ? 'collection__cover__par' : 'collection__cover'}
                />
            ))}
            </Container>
            <Slider products={latestReleases} addToCart={addToCart} />
        </Main>
    )
}