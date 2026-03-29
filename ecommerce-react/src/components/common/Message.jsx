import React from 'react'

import { Modal } from './Modal'

import './../../styles/components/common/Message.css'

export const Message = ({ isOpen, title = 'Confirmar', message = '¿Estás seguro?', onConfirm, onCancel, isConfirm = false }) => {
    return (
        <Modal
            isOpen={isOpen}
            onClosed={onCancel}
            title={title}
            confirm={onConfirm}
            cancel={onCancel}
        >
            <div className='message'>
                <p>{message}</p>
                <div className={isConfirm ? 'message__actions' : 'message__actions'}>
                    {isConfirm ?
                        <>
                            <button className='btn' onClick={onConfirm}>SI</button>
                            <button className='btn btn-dark' onClick={onCancel}>NO</button>
                        </>
                        :
                        <button className='btn btn-add' onClick={onCancel}>OK</button>

                    }
                </div>
            </div>
        </Modal>
    )
}