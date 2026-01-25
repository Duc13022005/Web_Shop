import axios from 'axios';

// Vite exposes env variables via import.meta.env
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export const client = axios.create({
    baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add interceptor to attach JWT token if available
client.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Add interceptor to simple response data or handle errors
client.interceptors.response.use(
    (response) => {
        return response.data;
    },
    (error) => {
        if (error.response && error.response.status === 401) {
            // Optional: Redirect to login or clear token if 401
            // localStorage.removeItem('token');
            // window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

