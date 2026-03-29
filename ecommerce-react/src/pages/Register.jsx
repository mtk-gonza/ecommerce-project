import React from 'react'

import { Main } from './../components/common/Main.jsx'
import { Container } from './../components/common/Container.jsx'
import { RegisterForm } from './../components/forms/RegisterForm.jsx'

import './../styles/pages/Register.css'

export const Register = () => {

    return (
        <Main className='register'>
            <Container>
                <RegisterForm />
            </Container>
        </Main>
    )
}