import React from 'react'
import { Link } from 'react-router-dom'

import { Main } from './../components/common/Main.jsx'
import { Container } from '../components/common/Container.jsx'

import './../styles/pages/Unauthorized.css'

export const Unauthorized = () => {
    return (
        <Main className='unauthorized'>
            <Container >
                <div className='unauthorized__content'>
                    <h2>Acceso Denegado</h2>
                    <p>No tienes permiso para acceder a esta página.</p>
                    <Link className='link' to='/dashboard'>Volver al inicio</Link>
                </div>
            </Container>
        </Main>
    )
}