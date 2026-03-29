export const licenseValidationRules = {
    name: {
        required: true,
        message: 'El nombre de la LICENCIA es obligatorio',
        minLength: 3,
        messageMinLength: 'La LICENCIA debe tener al menos 3 caracteres',
    },
    description: {
        required: true,
        message: 'La descripción es obligatoria',
        minLength: 10,
        messageMinLength: 'La descripción debe tener al menos 10 caracteres',
    },
    image: {
        required: true,
        message: 'La URL de la imagen es obligatoria',
        minLength: 20,
        messageMinLength: 'La URL de la imagen debe tener al menos 20 caracteres'
    }
}