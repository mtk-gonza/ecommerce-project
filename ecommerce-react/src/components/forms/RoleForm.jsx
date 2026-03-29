import React, { useRef, useEffect } from 'react'

import { Button } from './../common/Button.jsx'
import { Message } from './../common/Message.jsx'

import { useRoles } from './../../hooks/useRoles.jsx'
import { useWarning } from './../../hooks/useWarning.jsx'
import { useForm } from './../../hooks/useForm.jsx'

import { roleValidationRules } from './../../validations/roleValidationRules.js'

import { getFormMessages } from './../../utils/messageUtils.js'

export const RoleForm = ({ selectedItem = {}, onClosed }) => {
    const isInitialLoad = useRef(true)
    const { values, handleChange, handleSubmit, errors, resetForm } = useForm(selectedItem, roleValidationRules)
    const { addRole, updateRole } = useRoles()
    const { isOpenWarning, warning, titleWarning, messageWarning, handleClosedWarning } = useWarning()

    const onSubmit = async () => {
        try {
            const response = values.id ? await updateRole(values) : await addRole(values)
            const { title, message } = getFormMessages('Rol', values.id ? 'update' : 'create', !!response)

            warning(title, message, onClosed)

            if (response) {
                resetForm({})
            }

        } catch (err) {
            console.error(err)
            const { title, message } = getFormMessages('Rol', values.id ? 'update' : 'create', false)
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
        <div className='rol-form'>
            <div className='form__header'>
                <h2 className='form__title'>
                    {values.id ? 'Actualizar Rol' : 'Agregar Rol'}
                </h2>
            </div>
            <form className='form__content' onSubmit={handleSubmit(onSubmit)} >
                <div className='form__box--grid'>
                    <label className='form__label'>Nombre:</label>
                    <input className='form__input' type='text' name='name' value={values.name} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.name}</p>
                <div className='form__actions'>
                    <Button type='submit' className='btn btn-edit'>
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