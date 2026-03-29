import React from 'react'
import { Link } from 'react-router-dom'

import { Main } from './../components/common/Main.jsx'
import { Tabs } from './../components/layout/Tabs.jsx'

import './../styles/pages/Dashboard.css'

export const Dashboard = () => {
    return (
        <Main className='dashboard'>
            <h1>Bienvenido al Dashboard</h1>
            <Tabs />
            <Link className='link' to='/'>Volver</Link>
        </Main>
    )
}