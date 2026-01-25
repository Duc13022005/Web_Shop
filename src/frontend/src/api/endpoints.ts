
export const API_ENDPOINTS = {
    AUTH: {
        LOGIN: '/auth/login',
        REGISTER: '/auth/register',
        ME: '/auth/me',
        REFRESH: '/auth/refresh',
    },
    PRODUCTS: {
        LIST: '/products',
        DETAIL: (id: number) => `/products/${id}`,
        CATEGORIES: '/categories',
    },
    CART: {
        GET: '/cart',
        ADD_ITEM: '/cart/items',
        UPDATE_ITEM: (id: number) => `/cart/items/${id}`,
        REMOVE_ITEM: (id: number) => `/cart/items/${id}`,
        CLEAR: '/cart',
    },
    ORDERS: {
        CREATE: '/orders',
        LIST: '/orders',
        DETAIL: (id: number) => `/orders/${id}`,
    },
};
