import React from 'react'

import { Main } from './../components/common/Main.jsx'
import { Container } from './../components/common/Container.jsx'
import { LoginForm } from './../components/forms/LoginForm.jsx'

import './../styles/pages/Login.css'

export const Login = () => {
    return (
        <Main className='login'>
            <Container>
                <LoginForm />
            </Container>
        </Main>
    )
}