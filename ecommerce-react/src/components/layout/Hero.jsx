import React from 'react'
import { Link } from 'react-router-dom'

import { Container } from './../common/Container.jsx'

import './../../styles/components/layouts/Hero.css'

export const Hero = () => {
    return (
        <section className='hero'>
            <Container>
                <article className='hero__content'>
                    <h3 className='hero__title'>Nuevos Ingresos</h3>
                    <p className='hero__text'>Descubri el próximo Funko Pop de tu colección</p>                    
                    <Link className='hero__link' to='/shop'>SHOP</Link>   
                </article>          
            </Container>
        </section>
    )
}