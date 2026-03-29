import { useContext } from 'react'

import { RolesContext } from './../context/RolesContext.jsx'

export const useRoles = () => {
    return useContext(RolesContext)
}