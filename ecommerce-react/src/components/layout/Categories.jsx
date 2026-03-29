import React, { useState } from 'react'

import { Table } from './../common/Table.jsx'
import { Modal } from './../common/Modal.jsx'
import { Message } from './../common/Message.jsx'
import { CategoryForm } from './../forms/CategoryForm.jsx'

import { useCategories } from '../../hooks/useCategories.jsx'
import { useConfirm } from './../../hooks/useConfirm.jsx'
import { useWarning } from './../../hooks/useWarning.jsx'

export const Categories = () => {
    const [isOpen, setIsOpen] = useState(false)
    const [category, setCategory] = useState({})
    const { categories, deleteCategory } = useCategories()
    const { isOpenConfirm, message, title, confirm, onConfirm, onCancel } = useConfirm()
    const { isOpenWarning, warning, titleWarning, messageWarning, handleClosedWarning } = useWarning()

    const columns = [
        { key: 'id', label: 'ID' },
        { key: 'name', label: 'Nombre' },
        { key: 'created_at', label: 'Fecha de Creación' },
        { key: 'updated_at', label: 'Fecha de Actualización' }
    ]

    const handleEdit = (item) => {
        setCategory(item)
        setIsOpen(true)
    }

    const handleDelete = async (item) => {
        const confirmed = await confirm(`¿Estás seguro de eliminar la Categoria: ${item.name}?`, 'Eliminar Categoria')
        if (confirmed) {
            try {
                const response = await deleteCategory(item.id)
                if (response) warning('Eliminado exitosamente', `La Categoria: ${item.name} fue eliminada.`)
            } catch (err) {
                warning('Error al intentar Eliminar',`Error: ${err.message}`)
                console.error(err)
            }
        }
    }

    const handleClosed = () => {
        setIsOpen(false)
        setCategory({})
    }

    return (
        <>
            <Table columns={columns} data={categories} onEdit={handleEdit} onDelete={handleDelete}/>
            {isOpen &&
                <Modal isOpen={isOpen} onClosed={handleClosed}>
                    <CategoryForm selectedItem={category} onClosed={handleClosed}/>
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