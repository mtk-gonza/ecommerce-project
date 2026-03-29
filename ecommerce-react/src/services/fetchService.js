export const fetchData = async (url) => {
    try {
        const response = await fetch(url)

        if (!response.ok) throw new Error(`Error al cargar datos desde ${url}`)

        return await response.json()

    } catch (err) {
        console.error(err)
    }
}

export const fetchDataById = async (url, id) => {
    try {
        const response = await fetch(`${url}/${id}`)

        if (!response.ok) throw new Error(`Error al cargar el dato desde ${url} con ID: ${id}`)

        return await response.json()

    } catch (err) {
        console.error(err.message)
    }
}

export const postData = async (url, data) => {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })

        if (!response.ok) throw new Error(`Error al agregar desde ${url}`)

        return await response.json()

    } catch (err) {
        console.error(err.message)
    }
}

export const putData = async (url, data) => {    
    try {
        const response = await fetch(`${url}/${data.id}`,
            {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })

        if (!response.ok) throw Error(`Error al actualizar desde ${url}`)

        return await response.json()

    } catch (err) {
        console.error(err.message)
    }
}

export const deleteDataById = async (url, id) => {
    try {
        const response = await fetch(`${url}/${id}`, {
            method: 'DELETE',
        })

        if (!response.ok) throw Error(`Error al eliminar desde ${url}`)

        return true

    } catch (err) {
        console.error(err.message)
    }
}