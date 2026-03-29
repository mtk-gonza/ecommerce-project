export const userValidationRules = {
    name: {
        required: true,
        message: 'El nombre es obligatorio',
        minLength: 3,
        messageMinLength: 'El NOMBRE debe tener al menos 3 caracteres',
    },
    last_name: {
        required: true,
        message: 'El apellido es obligatorio',
        minLength: 3,
        messageMinLength: 'El APELLIDO debe tener al menos 3 caracteres',
    },
    email: {
        required: true,
        validate: (email) => /\S+@\S+\.\S+/.test(email),
        messageValidate: 'Email válido requerido'
    },
    role_id: {
        required: true,
        validate: value => !isNaN(Number(value)) && Number(value) > 0,
        messageValidate: 'Debe seleccionar un ROL válido',
    },
    password: {
        required: true,
        validate: (pass) => pass.length >= 6,
        messageValidate: 'La CONTRASEÑA debe tener al menos 6 caracteres'
    }
}