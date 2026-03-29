import React, { useState } from 'react'

import { Table } from './../common/Table.jsx'
import { Modal } from './../common/Modal.jsx'
import { Message } from './../common/Message.jsx'
import { RoleForm } from './../forms/RoleForm.jsx'

import { useRoles } from '../../hooks/useRoles.jsx'
import { useConfirm } from './../../hooks/useConfirm.jsx'
import { useWarning } from './../../hooks/useWarning.jsx'

export const Roles = () => {
    const [isOpen, setIsOpen] = useState(false)
    const [role, setRole] = useState({})
    const { roles, deleteRole } = useRoles()
    const { isOpenConfirm, message, title, confirm, onConfirm, onCancel } = useConfirm()
    const { isOpenWarning, warning, titleWarning, messageWarning, handleClosedWarning } = useWarning()

    const columns = [
        { key: 'id', label: 'ID' },
        { key: 'name', label: 'Nombre' },
        { key: 'created_at', label: 'Fecha de Creación' },
        { key: 'updated_at', label: 'Fecha de Actualización' }
    ]

    const handleEdit = (item) => {
        setRole(item)
        setIsOpen(true)
    }

    const handleDelete = async (item) => {
        const confirmed = await confirm(`¿Estás seguro de eliminar el rol: ${item.name}?`, 'Eliminar Rol')
        if (confirmed) {
            try {
                const response = await deleteRole(item.id)
                if (response) warning('Eliminado exitosamente', `El Rol: ${item.name} fue eliminado.`)
            } catch (err) {
                warning('Error al intentar Eliminar', `Error: ${err.message}`)
                console.error(err)
            }
        }
    }

    const handleClosed = () => {
        setIsOpen(false)
        setRole({})
    }

    return (
        <>
            <Table columns={columns} data={roles} onEdit={handleEdit} onDelete={handleDelete} />
            {isOpen &&
                <Modal isOpen={isOpen} onClosed={handleClosed}>
                    <RoleForm selectedItem={role} onClosed={handleClosed} />
                </Modal>
            }
            {isOpenConfirm && (
                <Message
                    isOpen={isOpenConfirm}
                    title={title}
                    message={message}
                    onConfirm={onConfirm}
                    onCancel={onCancel}
                    isConfirm={true}
                />
            )}
            {isOpenWarning && (
                <Message
                    isOpen={isOpenWarning}
                    title={titleWarning}
                    message={messageWarning}
                    onCancel={handleClosedWarning}
                    isConfirm={false}
                />
            )}
        </>
    )
}