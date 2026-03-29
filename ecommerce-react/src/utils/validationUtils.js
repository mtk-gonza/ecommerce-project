export const validateField = (fieldRules, value, values) => {
    if (fieldRules.required && (!value || value.toString().trim() === '')) {
        return fieldRules.message
    }

    if (fieldRules.validate && typeof fieldRules.validate === 'function') {
        const isValid = fieldRules.validate(value, values)
        if (!isValid) return fieldRules.messageValidate
    }

    if (fieldRules.minLength && value && value.length < fieldRules.minLength) {
        return fieldRules.messageMinLength
    }

    return null
}

export const validateForm = (rules, data, values) => {
    const errors = {}
    let isValid = true

    for (const field in rules) {
        const value = data[field]
        const fieldRules = rules[field]

        const error = validateField(fieldRules, value, values)

        if (error) {
            errors[field] = error
            isValid = false
        }
    }

    return { isValid, errors }
}