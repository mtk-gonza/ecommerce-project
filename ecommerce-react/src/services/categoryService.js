import { API_CATEGORIES } from './../config.js'
import { fetchData, fetchDataById, postData, putData, deleteDataById } from './fetchService.js'
import { addEntityTimestamps, updateEntityTimestamp } from './../utils/dateUtils.js'

const getCategories = async () => {
    try {
        const categories = await fetchData(API_CATEGORIES)
        return categories
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const getCategoryById = async (id) => {
    try {
        const category = await fetchDataById(API_CATEGORIES, id)
        return category
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const createCategory = async (categoryData) => {
    try {
        const categoryWithTimestamps = addEntityTimestamps(categoryData)
        const newCategory = await postData(API_CATEGORIES, categoryWithTimestamps)        
        return newCategory
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const updateCategory = async (categoryData) => {
    try {
        const categoryWithTimestamp = updateEntityTimestamp(categoryData)
        const updatedCategory = await putData(API_CATEGORIES, categoryWithTimestamp)
        return updatedCategory
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const deleteCategory = async (id) => {
    try {
        const success = await deleteDataById(API_CATEGORIES, id)
        return success
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const categoryService = {
    getCategories,
    getCategoryById,
    createCategory,
    updateCategory,
    deleteCategory
}

export default categoryService