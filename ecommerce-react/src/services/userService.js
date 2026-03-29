import { API_USERS, API_ROLES } from './../config.js'
import { fetchData, fetchDataById, postData, putData, deleteDataById } from './fetchService.js'
import { addEntityTimestamps, updateEntityTimestamp } from './../utils/dateUtils.js'

const getUsers = async () => {
    try {
        const [users, roles] = await Promise.all([
            fetchData(API_USERS),
            fetchData(API_ROLES)
        ])

        const rolesMap = Object.fromEntries(roles.map(r => [r.id, r]))

        const enrichedUsers = users.map(user => ({
            ...user,
            rol: rolesMap[user.rol_id],
        }))

        return enrichedUsers 

    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const getUserById = async (id) => {
    try {
        const user = await fetchDataById(API_USERS, id)
        const role = await fetchDataById(API_ROLES, user.rol_id)

        return {
            ...user,
            rol: role || null
        }

    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const createUser = async (userData) => {
    try {
        const userWithTimestamps = addEntityTimestamps(userData)
        const newUser = await postData(API_USERS, userWithTimestamps)
        return newUser
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const updateUser = async (userData) => {
    try {
        const userWithTimestamp = updateEntityTimestamp(userData)
        const updatedUser = await putData(API_USERS, userWithTimestamp)
        return updatedUser
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const deleteUser = async (id) => {
    try {
        return await deleteDataById(API_USERS, id)
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const userService = {
    getUsers,
    getUserById,
    createUser,
    updateUser,
    deleteUser
}

export default userService