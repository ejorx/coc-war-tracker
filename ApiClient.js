const { BASE_URL, BEARER_TOKEN } = require('./constants');

class ApiClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
        this.headers = {
            'Content-Type': 'application/json',
            // Puedes agregar aquí otras cabeceras por defecto, como la de autorización
            // 'Authorization': 'Bearer TU_TOKEN_AQUI'
        };
    }

    async _handleResponse(response) {
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ message: response.statusText }));
            throw new Error(`Error en la petición: ${response.status} - ${errorData.message || response.statusText}`);
        }
        return response.json();
    }

    async get(endpoint) {
        const response = await fetch(`${this.baseURL}/${endpoint}`, {
            method: 'GET',
            headers: this.headers,
        });
        return this._handleResponse(response);
    }

    // async post(endpoint, data) {
    //     const response = await fetch(`${this.baseURL}/${endpoint}`, {
    //         method: 'POST',
    //         headers: this.headers,
    //         body: JSON.stringify(data),
    //     });
    //     return this._handleResponse(response);
    // }

    // // Puedes agregar más métodos como put, delete, etc.
    // async put(endpoint, data) {
    //     const response = await fetch(`${this.baseURL}/${endpoint}`, {
    //         method: 'PUT',
    //         headers: this.headers,
    //         body: JSON.stringify(data),
    //     });
    //     return this._handleResponse(response);
    // }
}