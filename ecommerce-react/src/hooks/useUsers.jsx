import { useContext } from 'react'

import { UsersContext } from './../context/UsersContext.jsx'

export const useUsers = () => {
    return useContext(UsersContext)
}