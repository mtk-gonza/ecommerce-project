import { useContext } from 'react'

import { LicensesContext } from '../context/LicensesContext.jsx'

export const useLicenses = () => {
    return useContext(LicensesContext)
}