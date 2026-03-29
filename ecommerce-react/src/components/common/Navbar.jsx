import React from 'react'
import { Link } from 'react-router-dom'

import { Cart } from './Cart.jsx'
import { AccountMenu } from './AccountMenu.jsx'
import { ShopMenu } from './ShopMenu.jsx'


import { useAuth } from '../../hooks/useAuth.jsx'

import './../../styles/components/common/Navbar.css'

export const Navbar = () => {
    const { isAuthenticated, authUser } = useAuth()

    return (
        <nav className='navbar'>
            <ul className='navbar__menu'>
                <li className='navbar__item'>
                    <ShopMenu />
                </li>
                <li className='navbar__item'>
                    <Link className='navbar__link' to='/contact'>CONTACTO</Link>
                </li>
                {!isAuthenticated ?
                        <li className='navbar__item'>
                            <Link className='navbar__link' to='/register'>REGISTER</Link>
                        </li>
                    :
                    <>
                        <li className='navbar__item'>
                            <Link className='navbar__link' to='/favorites'>MIS FAVORITOS</Link>
                        </li>
                        {authUser?.role.name == 'admin' &&
                            <li className='navbar__item'>
                                <Link className='navbar__link' to='/dashboard'>DASHBOARD</Link>
                            </li>
                        }
                    </>
                }
                <li className='navbar__item'>
                    <Cart />
                </li>
                <li className='navbar__item'>
                    <AccountMenu />
                </li>
            </ul>
        </nav>
    )
}