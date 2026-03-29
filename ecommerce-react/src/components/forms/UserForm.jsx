import React, { useRef, useEffect } from 'react'

import { Button } from './../common/Button.jsx'
import { Message } from './../common/Message.jsx'

import { useUsers } from './../../hooks/useUsers.jsx'
import { useRoles } from './../../hooks/useRoles.jsx'
import { useWarning } from './../../hooks/useWarning.jsx'
import { useForm } from './../../hooks/useForm.jsx'

import { userValidationRules } from './../../validations/userValidationRules.js'

import { getFormMessages } from './../../utils/messageUtils.js'

export const UserForm = ({ selectedItem = {}, onClosed }) => {
    const isInitialLoad = useRef(true)
    const { values, handleChange, handleSubmit, errors, resetForm } = useForm(selectedItem, userValidationRules)
    const { addUser, updateUser } = useUsers()
    const { roles } = useRoles()
    const { isOpenWarning, warning, titleWarning, messageWarning, handleClosedWarning } = useWarning()

    const handleRoleChange = (e) => {
        handleChange({ target: { name: 'role_id', value: e.target.value } })
    }

    const onSubmit = async (e) => {
        try {          
            const response = values.id ? await updateUser(values) : await addUser(values)
            const { title, message } = getFormMessages('Usuario', values.id ? 'update' : 'create', !!response)

            warning(title, message, onClosed)

            if (response) {
                resetForm({})
            }

        } catch (err) {
            console.error(err)
            const { title, message } = getFormMessages('Usuario', values.id ? 'update' : 'create', false)
            warning(title, message, onClosed)
        }
    }

    useEffect(() => {
        if (isInitialLoad.current) {
            resetForm(selectedItem)
            isInitialLoad.current = false
        }
    }, [selectedItem])

    return (
        <div className='user-form'>
            <div className='form__header'>
                <h2 className='form__title'>
                    {values.id ? 'Actualizar Usuario' : 'Agregar Usuario'}
                </h2>
            </div>
            <form className='form__content' onSubmit={handleSubmit(onSubmit)} >
                <div className='form__box--grid'>
                    <label className='form__label'>Nombre:</label>
                    <input className='form__input' type='text' name='name' value={values.name} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.name}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Apellido:</label>
                    <input className='form__input' type='text' name='last_name' value={values.last_name} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.last_name}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Email:</label>
                    <input className='form__input' type='text' name='email' value={values.email} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.email}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Contraseña:</label>
                    <input className='form__input' type='password' name='password' value={values.password} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.password}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Rol:</label>
                    <select className='form__select' name='role_id' value={values.role_id || ''} onChange={handleRoleChange} required >
                        <option value=''>Seleccione un Rol</option>
                        {roles.map((role) => (
                            <option key={role.id} value={role.id}>
                                {role.name}
                            </option>
                        ))}
                    </select>
                </div>
                <p className='form__error'>{errors.role_id}</p>
                <div className='form__actions'>
                    <Button type='submit' className={values.id ? 'btn btn-edit' : 'btn btn-add'}>
                        {values.id ? 'Actualizar' : 'Guardar'}
                    </Button>
                    <Button className='btn' onClick={onClosed}>
                        Cancelar
                    </Button>
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