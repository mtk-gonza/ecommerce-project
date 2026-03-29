import { useState } from 'react'

export const useWarning = () => {
    const [isOpenWarning, setIsOpenWarning] = useState(false)
    const [messageWarning, setMessageWarning] = useState('')
    const [titleWarning, setTitleWarning] = useState('')
    const [onOkCallback, setOnOkCallback] = useState(null)

    const warning = (title, message, onOk = null) => {
        setTitleWarning(title)
        setMessageWarning(message)
        setOnOkCallback(() => onOk || (() => {}))
        setIsOpenWarning(true)
    }

    const handleClosedWarning = () => {
        setMessageWarning('')
        setTitleWarning('')
        if (onOkCallback) {
            onOkCallback()
        }
        setIsOpenWarning(false)        
    }

    return {
        isOpenWarning,
        warning,
        messageWarning,
        titleWarning,
        handleClosedWarning
    }
}