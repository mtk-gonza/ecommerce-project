import React from 'react'
import { Link } from 'react-router-dom'

import { Loading } from './Loading.jsx'

import { useAuth } from '../../hooks/useAuth.jsx'
import { useFavorites } from '../../hooks/useFavorites.jsx'

import { news } from '../../utils/newsUtils.js'
import './../../styles/components/common/ProductCard.css'

export const ProductCard = ({ product }) => {
    const { isAuthenticated } = useAuth()
    const { isFavorite, toggleFavorite } = useFavorites()
    const isFav = isFavorite(product.id)
    const isNew = news(product.created_at, 14)
    if (!product) {
        return (
            <div>
                <Loading />
            </div>
        )
    }
    const handleToggle = () => {
        toggleFavorite(product.id)
    }

    return (
        <article className='product-card' >
            <picture className='product-card__cover'>
                {isNew && <span className='product-card__tag'>Nuevo</span>}
                <img className='product-card__img--front slider' src={product.image_front} alt={`Figura coleccionable Funko de un ${product.name}`} />
                <img className='product-card__img--back slider' src={product.image_back} alt={`Figura coleccionable Funko de un ${product.name} en caja`} />
                {isAuthenticated &&
                    <span className='product-card__favorite' onClick={handleToggle}>{isFav ? '❤️' : '🤍'}</span>
                }
            </picture>
            <div className='product-card__content'>
                <p className='product-card__license'>{product.license.name}</p>
                <h4 className='product-card__name'>{product.name}</h4>
                <p className='product-card__price'>${product.price}.-</p>
                <p className='product-card__promo'>{product.dues} CUOTAS SIN INTERÉS</p>
                <Link className='product-card__see-more' to={`/detail/${product.id}`}>VER MAS</Link>
            </div>
        </article>
    )
}