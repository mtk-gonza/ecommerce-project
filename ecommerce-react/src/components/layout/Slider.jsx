import React, { useState } from 'react'
import { faChevronRight, faChevronLeft } from '@fortawesome/free-solid-svg-icons'

import { Container } from './../common/Container.jsx'
import { Icon } from './../common/Icon.jsx'
import { ProductCard } from './../common/ProductCard.jsx'

import './../../styles/components/layouts/Slider.css'

export const Slider = ({ products, title = 'ÚLTIMOS lanzamientos' }) => {
    title = title.toUpperCase()
    const [currentPage, setCurrentPage] = useState(0)
    const itemsPerPage = 3
    const totalPages = Math.ceil(products.length / itemsPerPage)

    const nextSlide = () => {
        setCurrentPage((prevPage) => (prevPage + 1) % totalPages)
    }

    const prevSlide = () => {
        setCurrentPage((prevPage) => (prevPage - 1 + totalPages) % totalPages)
    }

    const startIndex = currentPage * itemsPerPage
    const endIndex = startIndex + itemsPerPage
    const visibleProducts = products.slice(startIndex, endIndex)

    return (
        <section className='slider'>
            <Container>
                <div className='slider__relative'>
                    <h2 className='slider__title'>{title}</h2>
                    <div className={products.length < 3 ? 'slider__cards simple' : 'slider__cards compound'}>
                        {visibleProducts.map((product) => (
                            <ProductCard product={product} key={product.id}></ProductCard>
                        ))}
                    </div>
                    {products.length > 3 &&
                        <div className='slider__arrows'>
                            <button className='pagination__link arrows__left' onClick={prevSlide}>
                                <Icon css='icon' icon={faChevronLeft} />
                            </button>
                            <button className='pagination__link arrows__right' onClick={nextSlide}>
                                <Icon css='icon' icon={faChevronRight} />
                            </button>
                        </div>
                    }
                </div>
            </Container>
        </section>
    )
}