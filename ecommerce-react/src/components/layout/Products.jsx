import React, { useState } from 'react'

import { Table } from './../common/Table.jsx'
import { Modal } from './../common/Modal.jsx'
import { Message } from './../common/Message.jsx'
import { ProductForm } from './../forms/ProductForm.jsx'

import { useProducts } from './../../hooks/useProducts.jsx'
import { useConfirm } from './../../hooks/useConfirm.jsx'
import { useWarning } from './../../hooks/useWarning.jsx'

export const Products = () => {
    const [isOpen, setIsOpen] = useState(false)
    const [product, setProduct] = useState({})
    const { products, deleteProduct } = useProducts()
    const { isOpenConfirm, message, title, confirm, onConfirm, onCancel } = useConfirm()
    const { isOpenWarning, warning, titleWarning, messageWarning, handleClosedWarning } = useWarning()

    const columns = [
        { key: 'id', label: 'ID' },
        { key: 'name', label: 'Nombre' },
        { key: 'sku', label: 'Código' },
        { key: 'price', label: 'Precio' },
        { key: 'stock', label: 'Stock' }
    ]

    const handleEdit = (item) => {
        setProduct(item)
        setIsOpen(true)
    }

    const handleDelete = async (item) => {
        console.log('Eliminar', item)
        const confirmed = await confirm(`¿Estas seguro de eliminar producto: ${item.name}`, 'Eliminar Producto')
        if (confirmed) {
            try {
                const response = await deleteProduct(item.id)
                if (response) warning('Eliminado exitosamente', `El Usuario con el correo ${item.email} fue eliminado.`)
            } catch (err) {
                warning('Error al intentar Eliminar',`Error: ${err.message}`)
                console.error(err)
            }
        }
    }

    const handleClosed = () => {
        setIsOpen(false)
        setProduct({})
    }

    return (
        <>
            <Table columns={columns} data={products} onEdit={handleEdit} onDelete={handleDelete} />
            {isOpen &&
                <Modal isOpen={isOpen} onClosed={handleClosed}>
                    <ProductForm selectedItem={product} onClosed={handleClosed} />
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