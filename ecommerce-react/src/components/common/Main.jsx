import React from 'react'

import './../../styles/components/common/Main.css'

export const Main = ({children, className = ''}) => {

    return (
        <main className={className}>
            {children}
        </main>
    )
}