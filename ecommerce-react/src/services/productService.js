import { API_PRODUCTS, API_LICENSES, API_CATEGORIES} from './../config.js'
import { fetchData, fetchDataById, postData, putData, deleteDataById } from './fetchService.js'
import { addEntityTimestamps, updateEntityTimestamp } from './../utils/dateUtils.js'

const getProducts = async () => {
    try {
        const [products, licenses, categories] = await Promise.all([
            fetchData(API_PRODUCTS),
            fetchData(API_LICENSES),
            fetchData(API_CATEGORIES)
        ])

        const licenseMap = Object.fromEntries(licenses.map(l => [l.id, l]))
        const categoryMap = Object.fromEntries(categories.map(c => [c.id, c]))

        const enrichedProducts = products.map(product => ({
            ...product,
            license: licenseMap[product.license_id],
            category: categoryMap[product.category_id]
        }))

        return enrichedProducts
        
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const getProductById = async (id) => {
    try {
        const product  = await fetchDataById(API_PRODUCTS, id)
        const license = await fetchDataById(API_LICENSES, product.license_id)
        const category = await fetchDataById(API_CATEGORIES, product.category_id)

        return {
            ...product,
            license: license || null,
            category: category || null
        } 

    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const createProduct = async (productData) => {
    try {
        const productWithTimestamps = addEntityTimestamps(productData)
        const newProduct = await postData(API_PRODUCTS, productWithTimestamps)        
        return newProduct
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const updateProduct = async (productData) => {
    try {
        const productWithTimestamp = updateEntityTimestamp(productData)
        const updatedProduct = await putData(API_PRODUCTS, productWithTimestamp)
        return updatedProduct
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const deleteProduct = async (id) => {
    try {
        const success = await deleteDataById(API_PRODUCTS, id)
        return success
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const productService = {
    getProducts,
    getProductById,
    createProduct,
    updateProduct,
    deleteProduct
}

export default productService