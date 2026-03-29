import React from 'react'
import { BrowserRouter } from 'react-router-dom'

import { AppRoutes } from './routes/AppRoutes.jsx'

import { AppProvider } from './providers/AppProvider.jsx'

import { Header } from './components/layout/Header.jsx'
import { Footer } from './components/layout/Footer.jsx'

export const App = () => {

    return (
        <AppProvider>
            <BrowserRouter>
                <Header />
                <AppRoutes />
                <Footer />
            </BrowserRouter>
        </AppProvider>
    )
}