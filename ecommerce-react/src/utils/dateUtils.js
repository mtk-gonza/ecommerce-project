export const addEntityTimestamps = (data) => {
    return {
        ...data,
        created_at: new Date().toISOString().slice(0, 19),
        updated_at: new Date().toISOString().slice(0, 19)
    }
}

export const updateEntityTimestamp = (data) => {
    return {
        ...data,
        updated_at: new Date().toISOString().slice(0, 19)
    }
} 