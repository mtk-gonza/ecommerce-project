import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { faBars, faTimesCircle } from '@fortawesome/free-solid-svg-icons'

import { Container } from './../common/Container.jsx'
import { Navbar } from './../common/Navbar.jsx'
import { Icon } from '../common/Icon.jsx'

import logoHorizontal from './../../assets/logo_horizontal.svg'
import logo from './../../assets/logo.svg'
import { useIsMobile } from './../../hooks/useIsMobile.jsx'
import './../../styles/components/layouts/Header.css'

export const Header = () => {
    const [menuOpen, setMenuOpen] = useState(false)
    const isMobile = useIsMobile(1024)

    return (
        <header className='header'>
            <Container>
                <div className='header__top'>
                    <div className='header__logo'>
                        <Link to='/'>
                            {isMobile ? (
                                <img className='mobile-logo' src={logo} alt='FunkoShop Logotipo' />
                            ) : (
                                <img className='desktop-logo' src={logoHorizontal} alt='FunkoShop Logotipo Horizontal' />
                            )}
                        </Link>
                    </div>
                    {isMobile ? (
                        <div  onClick={() => setMenuOpen(true)} >
                            <Icon css='header__burger' icon={faBars} aria-label='Abrir menú'/>
                        </div>
                    ) : (
                        <nav className='header__navbar-desktop'>
                            <Navbar />
                        </nav>
                    )}
                </div>
                {isMobile && menuOpen && (
                    <div className='header__menu-overlay'>
                        <Container>
                            <div className='header__close' aria-label='Cerrar menú' onClick={() => setMenuOpen(false)} >
                                <Icon css='icon' icon={faTimesCircle} />
                            </div>
                        <Navbar />
                        </Container>
                    </div>
                )}
            </Container>
        </header>
    )
}