import React, { useState, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { faUserCircle, faSignOut, faChevronUp, faChevronDown, faSignIn } from '@fortawesome/free-solid-svg-icons'

import { Icon } from './Icon.jsx'
import { useAuth } from '../../hooks/useAuth.jsx'

import './../../styles/components/common/AccountMenu.css'

export const AccountMenu = () => {
    const { logout, authUser, isAuthenticated } = useAuth()

    const [isMenuOpen, setIsMenuOpen] = useState(false)
    const menuRef = useRef(null)

    const navidate = useNavigate()

    const handlerCloseOnMouseLeave = () => {
        setIsMenuOpen(false)
    }

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen)
    }

    const handleLogout = () => {
        logout()
        navidate('/login')
    }

    return (
        <div className='dropdown-menu' ref={menuRef} onClick={toggleMenu}>
            {!isAuthenticated ?
                <Link className='dropdown-menu__link' to='/login'>
                    <Icon icon={faSignIn} className='dropdown-menu__sign-in' />
                </Link>
                :
                <>
                    <div className='dropdown-menu__icons' >
                        <p className='navbar__link with-icon'>
                            <Icon css='ico_user' icon={faUserCircle} />
                            <Icon css='icon' icon={!isMenuOpen ? faChevronDown : faChevronUp} />
                        </p>
                    </div>
                    {isMenuOpen && (
                        <ul className='dropdown-menu__list' onMouseLeave={handlerCloseOnMouseLeave}>
                            <li className='account-menu__user-name'>{authUser.name} {authUser.lastName}</li>
                            <li className='dropdown-menu__item-list'>
                                <Link to='/favorites'>
                                    Mis Favoritos
                                </Link>
                            </li>
                            {authUser.role_id == 1 &&
                                <li className='dropdown-menu__item-list'>
                                    <Link to='/dashboard'>
                                        Dashboard
                                    </Link>
                                </li>
                            }
                            <li className='account-menu__sign-out' onClick={handleLogout}>
                                <Icon icon={faSignOut} className='sign-in-icon' />
                                <span>Cerrar sesión</span>
                            </li>
                        </ul>
                    )}
                </>
            }
        </div>
    )
}