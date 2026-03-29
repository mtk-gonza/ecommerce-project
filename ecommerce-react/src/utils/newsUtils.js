export const news = (dateString, days = 14) => {
    const createdAt = new Date(dateString)
    const now = new Date()
    const cutoffDate = new Date(now.getTime() - days * 24 * 60 * 60 * 1000)

    return createdAt > cutoffDate
}