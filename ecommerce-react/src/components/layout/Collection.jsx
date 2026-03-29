import React from 'react'
import { Link } from 'react-router-dom'

import './../../styles/components/layouts/Collection.css'

export const Collection = ({ license, nameClass }) => {
    return (
        <section className='collection'>
            <article className='collection__content'>
                <h3 className='collection__title'>{license.name}</h3>
                <p className='collection__text'>{license.description}</p>
                <Link className='collection__link' to={`/shop?license_id=${license.id}`} >VER COLECCIÓN</Link>
            </article>
            <picture className={nameClass}>
                <img className='collection__img' src={license.image} alt={`Figura de ${license.name}`} />
            </picture>
        </section>
    )
}