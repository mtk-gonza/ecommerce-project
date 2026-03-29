import React, { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

import { useAuth } from '../../hooks/useAuth.jsx'

import './../../styles/components/forms/LoginForm.css'

export const LoginForm = () => {
    const [credentials, setCredentials] = useState({ email: '', password: '' })
    const [remember, setRemember] = useState(false)

    const { login, isLoadingAuthUser, errorAuthUser, setErrorAuthUser } = useAuth()
    const navigate = useNavigate()
    const location = useLocation()

    const handleChange = (e) => {
        const { name, value } = e.target
        setCredentials((prev) => ({ ...prev, [name]: value }))

        if (errorAuthUser) {
            setErrorAuthUser(null)
        }
    }

    const handleRememberChange = (e) => {
        setRemember(e.target.checked)
    }

    const handleLogin = async (e) => {
        e.preventDefault()
        try {
            await login(credentials.email, credentials.password, remember)
            const from = location.state?.from || '/'
            navigate(from, { replace: true })
        } catch (err) {
            console.error('Error al iniciar sesión', err)
        }
    }

    return (
        <div className='login-form'>
            <div className='form__header'>
                <h2 className='form__title'>INGRESAR A MI CUENTA</h2>
                <p className='form__subtitle'>Para obtener novedades</p>
            </div>
            <form className='login__form' onSubmit={handleLogin}>
                <div className='form__box--grid'>
                    <label className='form__label' htmlFor='emal'>Email:</label>
                    <input className='form__input' type='email' name='email' placeholder='john.doe@funkoshop.com'
                        onChange={handleChange}
                    />
                </div>
                <div className='form__box--grid'>
                    <label className='form__label' htmlFor='password'>Contraseña:</label>
                    <input className='form__input' type='password' name='password' placeholder='●●●●●●●●●●●' onChange={handleChange} />
                </div>
                <div className='form__error'>
                    {errorAuthUser && (<p>{errorAuthUser}</p>)}
                </div>
                <div className='login__actions'>
                    <a className='form__link' href=''>
                        Olvidé mi contraseña
                    </a>
                    <div className='form__submission'>
                        <input className='btn' type='submit' value={isLoadingAuthUser ? 'Ingresando...' : 'Ingresar'} disabled={isLoadingAuthUser} />
                        <div className='form__remember'>
                            <input type='checkbox' name='remember' checked={remember} onChange={handleRememberChange} />
                            <label htmlFor=''>Recordarme</label>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    )
}