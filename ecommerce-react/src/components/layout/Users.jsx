import React, { useState } from 'react'

import { Table } from './../common/Table.jsx'
import { Modal } from './../common/Modal.jsx'
import { Message } from './../common/Message.jsx'
import { UserForm } from './../forms/UserForm.jsx'

import { useUsers } from './../../hooks/useUsers.jsx'
import { useConfirm } from './../../hooks/useConfirm.jsx'
import { useWarning } from './../../hooks/useWarning.jsx'

export const Users = () => {
    const [isOpen, setIsOpen] = useState(false)
    const [user, setUser] = useState({})
    const { users, deleteUser } = useUsers()
    const { isOpenConfirm, message, title, confirm, onConfirm, onCancel } = useConfirm()
    const { isOpenWarning, warning, titleWarning, messageWarning, handleClosedWarning } = useWarning()

    const columns = [
        { key: 'id', label: 'ID' },
        { key: 'name', label: 'Nombre' },
        { key: 'last_name', label: 'Apellido' },
        { key: 'created_at', label: 'Fecha de Creación' },
        { key: 'updated_at', label: 'Fecha de Actualización' }
    ]

    const handleEdit = (item) => {
        setUser(item)
        setIsOpen(true)
    }

    const handleDelete = async (item) => {
        const confirmed = await confirm(`¿Estás seguro de eliminar al Usuario: ${item.email}?`, 'Eliminar Usuario')
        if (confirmed) {
            try {
                const response = await deleteUser(item.id)
                if (response) warning('Eliminado exitosamente', `El Usuario con el correo ${item.email} fue eliminado.`)
            } catch (err) {
                warning('Error al intentar Eliminar',`Error: ${err.message}`)
                console.error(err)
            }
        }
    }

    const handleClosed = () => {
        setIsOpen(false)
        setUser({})
    }

    return (
        <>
            <Table columns={columns} data={users} onEdit={handleEdit} onDelete={handleDelete} />
            {isOpen &&
                <Modal isOpen={isOpen} onClosed={handleClosed}>
                    <UserForm selectedItem={user} onClosed={handleClosed} />
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