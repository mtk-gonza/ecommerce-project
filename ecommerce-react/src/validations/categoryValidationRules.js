export const categoryValidationRules = {
    name: {
        required: true,
        message: 'El nombre de la CATEGORIA es obligatorio',
        minLength: 3,
        messageMinLength: 'La CATEGORIA debe tener al menos 3 caracteres',
    },
    description: {
        required: true,
        message: 'La descripción es obligatoria',
        minLength: 20,
        messageMinLength: 'La descripción debe tener al menos 20 caracteres',
    }
}