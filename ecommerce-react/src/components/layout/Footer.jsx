import React from 'react'
import { Link } from 'react-router-dom'

import { Container } from './../common/Container.jsx'

import logo from './../../assets/logo.svg'
import './../../styles/components/layouts/Footer.css'

export const Footer = () => { 
    return (
        <footer className='footer'>
            <Container>
                <div className='footer__container'>
                    <ul className='footer__links'>
                        <li><Link className='footer__link' to='/returns'>Devoluciones</Link></li>
                        <li><Link className='footer__link' to='/terms'>Términos y Condiciones</Link></li>
                        <li><Link className='footer__link' to='/privacy'>Política de Privacidad</Link></li>
                    </ul>    
                    <picture className='footer__logo'>
                        <img src={logo} alt='Isotipo de la marca FunkoShop'/>    
                    </picture>
                </div>
                <p className='footer__copy'>All rights reserved 2025 - FunkoShop of Gonzalo Gonzalez &copy;</p>
            </Container>
        </footer>
    )
}