
export const API_ENDPOINTS = {
    AUTH: {
        LOGIN: '/auth/login',
        REGISTER: '/auth/register',
        ME: '/auth/me',
        REFRESH: '/auth/refresh',
        CHANGE_PASSWORD: '/auth/change-password',
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
    ADMIN: {
        DASHBOARD: '/admin/dashboard',
        EMPLOYEES: '/admin/employees',
        EMPLOYEES_DETAIL: (id: number) => `/admin/employees/${id}`,
        PRODUCTS: '/admin/products',
    }
};
