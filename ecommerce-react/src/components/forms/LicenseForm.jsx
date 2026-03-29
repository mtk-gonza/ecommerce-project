import React, { useRef, useEffect } from 'react'

import { Button } from '../common/Button.jsx'
import { Message } from '../common/Message.jsx'

import { useLicenses } from '../../hooks/useLicenses.jsx'
import { useWarning } from '../../hooks/useWarning.jsx'
import { useForm } from '../../hooks/useForm.jsx'

import { licenseValidationRules } from '../../validations/LicenseValidationRules.js'

import { getFormMessages } from '../../utils/messageUtils.js'

export const LicenseForm = ({ selectedItem = {}, onClosed }) => {
    const isInitialLoad = useRef(true)
    const { values, handleChange, handleSubmit, errors, resetForm } = useForm(selectedItem, licenseValidationRules)
    const { addLicense, updateLicense } = useLicenses()
    const { isOpenWarning, warning, titleWarning, messageWarning, handleClosedWarning } = useWarning()

    const onSubmit = async (e) => {
        try {
            const response = values.id ? await updateLicense(values) : await addLicense(values)
            const { title, message } = getFormMessages('Licencia', values.id ? 'update' : 'create', !!response)

            warning(title, message, onClosed)

            if (response) {
                resetForm({})
            }

        } catch (err) {
            console.error(err)
            const { title, message } = getFormMessages('Licencia', values.id ? 'update' : 'create', false)
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
        <div className='licence-form'>
            <div className='form__header'>
                <h2 className='form__title'>
                    {values.id ? 'Actualizar Licencia' : 'Agregar Licencia'}
                </h2>
            </div>
            <form className='form__content' onSubmit={handleSubmit(onSubmit)} >
                <div className='form__box--grid'>
                    <label className='form__label'>Nombre:</label>
                    <input className='form__input' type='text' name='name' value={values.name} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.name}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Descripcion:</label>
                    <input className='form__input' type='text' name='description' value={values.description} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.description}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Imagen URL</label>
                    <input className='form__input' type='text' name='image' value={values.image} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.image}</p>
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