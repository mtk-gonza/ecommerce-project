import React, { useRef, useEffect } from 'react'

import { Button } from './../common/Button.jsx'
import { Message } from './../common/Message.jsx'

import { useProducts } from './../../hooks/useProducts.jsx'
import { useCategories } from './../../hooks/useCategories.jsx'
import { useLicenses } from '../../hooks/useLicenses.jsx'
import { useWarning } from './../../hooks/useWarning.jsx'
import { useForm } from './../../hooks/useForm.jsx'

import { productValidationRules } from './../../validations/productValidationRules.js'

import { getFormMessages } from './../../utils/messageUtils.js'

export const ProductForm = ({ selectedItem = {}, onClosed }) => {
    const isInitialLoad = useRef(true)
    const { values, handleChange, handleSubmit, errors, resetForm } = useForm(selectedItem, productValidationRules)
    const { addProduct, updateProduct } = useProducts()
    const { categories } = useCategories()
    const { licenses } = useLicenses()
    const { isOpenWarning, warning, titleWarning, messageWarning, handleClosedWarning } = useWarning()

    const handleCategoryChange = (e) => {
        handleChange({ target: { name: 'category_id', value: e.target.value } })
    }

    const handleLicenseChange = (e) => {
        handleChange({ target: { name: 'license_id', value: e.target.value } })
    }

    const onSubmit = async (e) => {
        try {
            const response = values.id ? await updateProduct(values) : await addProduct(values)
            const { title, message } = getFormMessages('Producto', values.id ? 'update' : 'create', !!response)

            warning(title, message, onClosed)

            if (response) {
                resetForm({})
            }

        } catch (err) {
            console.error(err)
            const { title, message } = getFormMessages('Producto', values.id ? 'update' : 'create', false)
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
        <div className='product-form'>
            <div className='form__header'>
                <h2 className='form__title'>
                    {values.id ? 'Actualizar Producto' : 'Agregar Producto'}
                </h2>
            </div>
            <form className='form__content' onSubmit={handleSubmit(onSubmit)} >
                <div className='form__box--grid'>
                    <label className='form__label'>Nombre:</label>
                    <input className='form__input' type='text' name='name' value={values.name} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.name}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>N° De Serie:</label>
                    <input className='form__input' type='text' name='sku' value={values.sku} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.sku}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Descripcion:</label>
                    <input className='form__input' type='text' name='description' value={values.description} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.description}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Precio:</label>
                    <input className='form__input' type='number' name='price' value={values.price} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.price}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Stock:</label>
                    <input className='form__input' type='number' name='stock' value={values.stock} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.stock}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Descuento:</label>
                    <input className='form__input' type='number' name='discount' value={values.discount} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.discount}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Cuotas:</label>
                    <input className='form__input' type='number' name='dues' value={values.dues} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.dues}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Especial:</label>
                    <select className='form__select' name='special' value={values.special} onChange={handleCategoryChange} required >
                        <option value=''>Seleccione si es Especial</option>
                        <option value={true}>SI</option>
                        <option value={false}>NO</option>
                    </select>
                </div>
                <p className='form__error'>{errors.special}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>URL FRONT</label>
                    <input className='form__input' type='text' name='image_front' value={values.image_front} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.image_front}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>URL BACK</label>
                    <input className='form__input' type='text' name='image_back' value={values.description} onChange={handleChange} required />
                </div>
                <p className='form__error'>{errors.image_back}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Licencia:</label>
                    <select className='form__select' name='license_id' value={values.license_id || ''} onChange={handleLicenseChange} required >
                        <option value=''>Seleccione una Licencia</option>
                        {licenses.map((license) => (
                            <option key={license.id} value={license.id}>
                                {license.name}
                            </option>
                        ))}
                    </select>
                </div>
                <p className='form__error'>{errors.license_id}</p>
                <div className='form__box--grid'>
                    <label className='form__label'>Categoría:</label>
                    <select className='form__select' name='category_id' value={values.category_id || ''} onChange={handleCategoryChange} required >
                        <option value=''>Seleccione una Categoría</option>
                        {categories.map((category) => (
                            <option key={category.id} value={category.id}>
                                {category.name}
                            </option>
                        ))}
                    </select>
                </div>
                <p className='form__error'>{errors.category_id}</p>
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