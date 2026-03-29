import { API_ROLES } from './../config.js'
import { fetchData, fetchDataById, postData, putData, deleteDataById } from './fetchService.js'
import { addEntityTimestamps, updateEntityTimestamp } from './../utils/dateUtils.js'

const getRoles = async () => {
    try {
        const roles = await fetchData(API_ROLES)
        return roles
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const getRoleById = async (id) => {
    try {
        const Rol = await fetchDataById(API_ROLES, id)
        return Rol
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const createRole = async (roleData) => {
    try {
        const roleWithTimestamps = addEntityTimestamps(roleData)
        const newRole = await postData(API_ROLES, roleWithTimestamps)        
        return newRole
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const updateRole = async (roleData) => {
    try {
        const roleWithTimestamp = updateEntityTimestamp(roleData)
        const updatedRole = await putData(API_ROLES, roleWithTimestamp)
        return updatedRole
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const deleteRole = async (id) => {
    try {
        const success = await deleteDataById(API_ROLES, id)
        return success
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const roleService = {
    getRoles,
    getRoleById,
    createRole,
    updateRole,
    deleteRole
}

export default roleService