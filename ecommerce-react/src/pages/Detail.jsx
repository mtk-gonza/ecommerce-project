import React, { useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { Main } from './../components/common/Main.jsx'
import { Loading } from './../components/common/Loading.jsx'
import { ProductDetail } from './../components/common/ProductDetail.jsx'
import { Slider } from './../components/layout/Slider.jsx'

import { useProducts } from './../hooks/useProducts.jsx'

import './../styles/pages/Detail.css'

export const Detail = () => {    
    const { product_id } = useParams()
    const { products } = useProducts()

    useEffect(() => {
        window.scrollTo(0, 0)
    }, [product_id])

    const product = products.find(producto => producto.id == product_id)
    const productsColection = products.filter(item => item.license_id == product.license_id & item.id != product.id)

    if (!product) {
        return (
            <Loading/>                
        )
    }

    return (
        <Main className='detail'>
            <ProductDetail product={product}/>
            {productsColection.length > 1 &&  <Slider products={productsColection} title='COLECCIÓN'/>}            
        </Main>
    )
}