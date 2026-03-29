import { useState } from 'react'

export const useConfirm = () => {
    const [isOpenConfirm, setIsOpenConfim] = useState(false)
    const [message, setMessage] = useState('')
    const [title, setTitle] = useState('Confirmar')
    const [callback, setCallback] = useState(null)

    const confirm = (msg, titleMsg = 'Confirmar') => {
        setTitle(titleMsg)
        setMessage(msg)
        return new Promise((resolve) => {
            setCallback(() => resolve)
            setIsOpenConfim(true)
        })
    }

    const handleConfirm = () => {
        if (callback) callback(true)
        setIsOpenConfim(false)
    }

    const handleCancel = () => {
        if (callback) callback(false)
        setIsOpenConfim(false)
    }

    return {
        isOpenConfirm,
        message,
        title,
        confirm,
        onConfirm: handleConfirm,
        onCancel: handleCancel
    }
}