import React from 'react'

import loading from './../../assets/loading.gif'

import './../../styles/components/common/Loading.css'

export const Loading = () => {
    return (
        <img className='img_loading' src={loading} alt='Image loading' />
    )
}