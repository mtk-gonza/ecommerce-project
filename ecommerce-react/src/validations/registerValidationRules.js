export const registerValidationRules = {
    name: {
        required: true,
        message: 'El nombre es obligatorio',
        minLength: 3,
        messageMinLength: 'El nombre debe tener al menos 3 caracteres',
    },
    last_name: {
        required: true,
        message: 'El apellido es obligatorio',
        minLength: 3,
        messageMinLength: 'El apellido debe tener al menos 3 caracteres',
    },
    email: {
        required: true,
        message: 'El correo electrónico es obligatorio',
        validate: value => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
        messageValidate: 'Debe ingresar un correo válido',
    },
    password: {
        required: true,
        message: 'La contraseña es obligatoria',
        minLength: 6,
        messageMinLength: 'La contraseña debe tener al menos 6 caracteres'
    },
    rePassword: {
        required: true,
        message: 'Debe repetir la contraseña',
        validate: (value, allValues) => {            
            if (!value || !allValues?.password) return true
            return value === allValues.password        
        },
        messageValidate: 'Las contraseñas no coinciden'
    },
    isCheck: {
        required: true,
        message: 'Debe aceptar los términos y condiciones',
        validate: value => value === true,
        messageValidate: 'Debe aceptar los términos y condiciones',
    }
}