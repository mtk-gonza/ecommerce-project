export const roleValidationRules = {
    name: {
        required: true,
        message: 'El nombre del ROL es obligatorio',
        minLength: 3,
        messageMinLength: 'El nombre del ROL debe tener al menos 3 caracteres',
    }
}