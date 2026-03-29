import React from 'react'

import './../../styles/components/common/Container.css'

export const Container = ({ children }) => {
    return (
        <div className='container'>
            { children }
        </div>
    )
}