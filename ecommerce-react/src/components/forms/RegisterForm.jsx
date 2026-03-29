import React from 'react'
import { Link } from 'react-router-dom'

import { Message } from './../common/Message.jsx'

import { useUsers } from './../../hooks/useUsers.jsx'
import { useWarning } from './../../hooks/useWarning.jsx'
import { useForm } from './../../hooks/useForm.jsx'

import { registerValidationRules } from './../../validations/registerValidationRules.js'

import { getFormMessages } from './../../utils/messageUtils.js'

import './../../styles/components/forms/RegisterForm.css'

const initialRegisterState = {
    name: '',
    last_name: '',
    email: '',
    password: '',
    rePassword: '',
    isCheck: false
}

export const RegisterForm = () => {
    const { values, handleChange, handleSubmit, errors, resetForm } = useForm(initialRegisterState, registerValidationRules)
    const { addUser } = useUsers()
    const { isOpenWarning, warning, titleWarning, messageWarning, handleClosedWarning } = useWarning()

    const onSubmit = async () => {
        try {
            values.role_id = 2
            const response = await addUser(values)
            const { title, message } = getFormMessages('Usuario', 'create', !!response)

            warning(title, message, handleClosedWarning)

            if (response) {
                resetForm(initialRegisterState)
            }

        } catch (err) {
            console.error(err)
            const { title, message } = getFormMessages('Usuario', 'create', false)
            warning(title, message, handleClosedWarning)
        }
    }

    return (
        <div className='register-form'>
            <div className='register__header'>
                <h2 className='register__title'>CREA TU CUENTA</h2>
                <p className='register__subtitle'>Completa el formulario para ser parte del mundo de los Funkos</p>
            </div>
            <form className='form__content' onSubmit={handleSubmit(onSubmit)}>
                <div className='form__box--grid'>
                    <label className='form__label'>Nombre:</label>
                    <input className='form__input' type='text' name='name' placeholder='John' value={values.name} onChange={handleChange} />
                </div>
                <p className='form__error'>{errors.name}</p>
                <div className='form__box--grid'>
                    <label className='form__label' htmlFor='last_name'>Apellido:</label>
                    <input className='form__input' type='text' name='last_name' placeholder='Doe' value={values.last_name || ''} onChange={handleChange} />
                </div>
                <p className='form__error'>{errors.last_name}</p>
                <div className='form__box--grid'>
                    <label className='form__label' htmlFor='email'>Email:</label>
                    <input className='form__input' type='email' name='email' placeholder='johndoe@funkoshop.com' value={values.email || ''} onChange={handleChange} />
                </div>
                <p className='form__error'>{errors.email}</p>
                <div className='form__box--grid'>
                    <label className='form__label' htmlFor='password'>Contraseña:</label>
                    <input className='form__input' type='password' name='password' placeholder='●●●●●●●●●●●' value={values.password || ''} onChange={handleChange} />
                </div>
                <p className='form__error'>{errors.password}</p>
                <div className='form__box--grid'>
                    <label className='form__label' htmlFor='rePassword'>Repite Contraseña:</label>
                    <input className='form__input' type='password' name='rePassword' placeholder='●●●●●●●●●●●' value={values.rePassword || ''} onChange={handleChange} />
                </div>
                <p className='form__error'>{errors.rePassword}</p>
                <div className='form__submission'>
                    <input className='form__btn btn btn--primary btn--large' type='submit' value='Registrar' />
                    <div className='form__terms'>
                        <input type='checkbox' name='isCheck' checked={values.isCheck} onChange={handleChange} />
                        <label>Acepto <Link className='form__link' to='/terms'>Términos y Condiciones</Link></label>
                    </div>
                    <p className='form__error'>{errors.isCheck}</p>
                </div>
            </form>
            {isOpenWarning && (
                <Message
                    isOpen={isOpenWarning}
                    title={titleWarning}
                    message={messageWarning}
                    onCancel={handleClosedWarning}
                    isConfirm={false}
                />
            )}
        </div>
    )
}