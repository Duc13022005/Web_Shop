
import { client } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';

export interface Product {
    id: number;
    sku: string;
    name: string;
    description: string;
    category_id?: number;
    category_name?: string;
    base_price: number;
    sale_price?: number;
    current_price: number;
    unit: string;
    image_path?: string;
    images?: string[];
    specifications?: Record<string, any>;
    available_stock: number;
    is_active: boolean;
}

export const productService = {
    getAll: async (params?: any) => {
        const response = await client.get(API_ENDPOINTS.PRODUCTS.LIST, { params });
        return response.data;
    },

    getById: async (id: number | string): Promise<Product> => {
        const response = await client.get(`${API_ENDPOINTS.PRODUCTS.LIST}/${id}`);
        // Client interceptor already returns response.data
        const p = response as any;
        // Ensure images is an array
        if (!p.images) p.images = [];
        // Ensure image_path is absolute URL if it exists
        // Ensure image_path is absolute URL if it exists
        if (p.image_path && !p.image_path.startsWith('http')) {
            const path = p.image_path.startsWith('/') ? p.image_path.substring(1) : p.image_path;
            const cleanPath = path.startsWith('uploads/') ? path : `uploads/${path}`;
            p.image_path = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/${cleanPath}`;
        }
        // Map images to absolute URLs
        p.images = p.images.map((img: string) => {
            if (img.startsWith('http')) return img;
            const path = img.startsWith('/') ? img.substring(1) : img;
            const cleanPath = path.startsWith('uploads/') ? path : `uploads/${path}`;
            return `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/${cleanPath}`;
        });
        return p;
    }
};
