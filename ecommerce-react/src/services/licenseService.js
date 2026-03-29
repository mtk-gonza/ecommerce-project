import { API_LICENSES } from './../config.js'
import { fetchData, fetchDataById, postData, putData, deleteDataById } from './fetchService.js'
import { addEntityTimestamps, updateEntityTimestamp } from './../utils/dateUtils.js'

const getLicenses = async () => {
    try {
        const licenses = await fetchData(API_LICENSES)
        return licenses
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const getLicenseById = async (id) => {
    try {
        const license = await fetchDataById(API_LICENSES, id)
        return license
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const createLicense = async (licenseData) => {
    try {
        const licenseWithTimestamps = addEntityTimestamps(licenseData)
        const newLicense = await postData(API_LICENSES, licenseWithTimestamps)  
        return newLicense        
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const updateLicense = async (licenseData) => {
    try {
        const licenseWithTimestamp = updateEntityTimestamp(licenseData)
        const updatedLicense = await putData(API_LICENSES, licenseWithTimestamp)
        return updatedLicense
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const deleteLicense = async (id) => {
    try {
        const success = await deleteDataById(API_LICENSES, id)
        return success
    } catch (err) {
        console.error(err.message)
        throw err
    }
}

const licenseService = {
    getLicenses,
    getLicenseById,
    createLicense,
    updateLicense,
    deleteLicense
}

export default licenseService