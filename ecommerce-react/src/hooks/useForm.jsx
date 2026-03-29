import React, { useState } from 'react'
import { validateField, validateForm } from './../utils/validationUtils.js'

export const useForm = (initialState, rules) => {
    const [values, setValues] = useState(initialState)
    const [errors, setErrors] = useState({})
    const [touched, setTouched] = useState({})

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target
        const newValue = type === 'checkbox' ? checked : value

        const newValues = { ...values, [name]: newValue }

        setValues(newValues)
        
        setTouched((prev) => ({ ...prev, [name]: true }))

        const fieldRule = rules[name]
        const error = validateField(fieldRule, newValue, newValues)

        setErrors((prev) => ({ ...prev, [name]: error }))
    }

    const handleSubmit = (onSubmit) => (e) => {
        e.preventDefault()
        const { isValid, errors: formErrors } = validateForm(rules, values, values)
        setErrors(formErrors)

        if (isValid) onSubmit(values)
    }

    const resetForm = () => {
        setValues(initialState)
        setErrors({})
        setTouched({})
    }

    return {
        values,
        handleChange,
        handleSubmit,
        resetForm,
        errors,
        touched
    }
}