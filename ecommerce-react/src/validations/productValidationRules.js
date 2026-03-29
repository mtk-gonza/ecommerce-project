export const productValidationRules = {
    name: {
        required: true,
        message: 'El nombre del PRODUCTO es obligatorio',
        minLength: 3,
        messageMinLength: 'El nombre del PRODUCTO debe tener al menos 3 caracteres',
    },
    sku: {
        required: true,
        message: 'El SKU es obligatorio',
        minLength: 6,
        messageMinLength: 'El SKU debe tener al menos 6 caracteres',
    },
    description: {
        required: true,
        message: 'La descripción es obligatoria',
        minLength: 10,
        messageMinLength: 'La descripción debe tener al menos 10 caracteres',
    },
    price: {
        required: true,
        message: 'El precio es obligatorio',
        validate: value => !isNaN(Number(value)) && Number(value) > 0,
        messageValidate: 'El precio debe ser un número mayor a 0',
    },
    stock: {
        required: true,
        message: 'El stock es obligatorio',
        validate: value => !isNaN(Number(value)) && Number(value) >= 0,
        messageValidate: 'El stock debe ser un número igual o mayor a 0',
    },
    discount: {
        required: false,
        validate: value => {
            const num = Number(value)
            return !isNaN(num) && num >= 0 && num <= 100
        },
        messageValidate: 'El descuento debe ser un número entre 0 y 100',
    },
    dues: {
        required: false,
        validate: value => {
            const num = Number(value)
            return !isNaN(num) && num >= 0 && num <= 48
        },
        messageValidate: 'Las cuotas deben ser un número entre 0 y 48',
    },
    special: {
        required: false,
        validate: value => typeof value === 'boolean',
        messageValidate: 'El campo especial debe ser verdadero o falso',
    },
    image_front: {
        required: true,
        message: 'La URL de la imagen frontal es obligatoria',
        minLength: 20,
        messageMinLength: 'La URL de la imagen debe tener al menos 20 caracteres'
    },
    image_back: {
        required: true,
        message: 'La URL de la imagen trasera es obligatoria',
        minLength: 20,
        messageMinLength: 'La URL de la imagen debe tener al menos 20 caracteres'
    },
    licence_id: {
        required: true,
        validate: value => !isNaN(Number(value)) && Number(value) > 0,
        messageValidate: 'Debe seleccionar una licencia válida',
    },
    category_id: {
        required: true,
        validate: value => !isNaN(Number(value)) && Number(value) > 0,
        messageValidate: 'Debe seleccionar una categoría válida',
    }
}