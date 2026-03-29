import React, { useState, useRef } from 'react'
import { Link } from 'react-router-dom'
import { faChevronUp, faChevronDown } from '@fortawesome/free-solid-svg-icons'

import { Icon } from './Icon.jsx'

import { useCategories } from './../../hooks/useCategories.jsx'

export const ShopMenu = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false)
    const menuRef = useRef(null)

    const { categories } = useCategories()

    const handlerCloseOnMouseLeave = () => {
        setIsMenuOpen(false)
    }

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen)
    }

    return (
        <div className='dropdown-menu' ref={menuRef} onClick={toggleMenu}>
            <div className='dropdown-menu__icons' >
                <div className='navbar__link with-icon'>
                    <p>SHOP</p>
                    <Icon css='icon' icon={!isMenuOpen ? faChevronDown : faChevronUp} />
                </div>
                {isMenuOpen &&(
                    <ul className='dropdown-menu__list' onMouseLeave={handlerCloseOnMouseLeave} >
                        {categories.map((category) => (
                            <li className='dropdown-menu__item-list' key={category.id}>
                                <Link to={`/shop/${category.name}`}>{category.name.toUpperCase()}</Link>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    )
}