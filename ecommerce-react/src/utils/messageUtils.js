export const getFormMessages = (type, operationType = 'create', success = true) => {
    const operations = {
        create: {
            actionVerb: 'crear',
            pastParticiple: 'creado',
            noun: 'Creación'
        },
        update: {
            actionVerb: 'actualizar',
            pastParticiple: 'actualizado',
            noun: 'Actualización'
        },
        delete: {
            actionVerb: 'eliminar',
            pastParticiple: 'eliminado',
            noun: 'Eliminación'
        }
    }

    const op = operations[operationType] || operations.create;

    if (success) {
        return {
            title: `${type} ${op.pastParticiple}`,
            message: `${type} ${op.pastParticiple} exitosamente`,
        }
    } else {
        return {
            title: `Error al ${op.noun} ${type}`,
            message: `Hubo un problema al ${op.actionVerb} el ${type}`,
        }
    }
}