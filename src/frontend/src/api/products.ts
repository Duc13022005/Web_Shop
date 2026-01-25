import { client } from './client';

export interface Product {
    id: number;
    name: string;
    description: string | null;
    base_price: number;
    sale_price: number | null;
    image_url: string | null;
    category_id: number;
    is_active: boolean;
    unit: string;
}

export const getProducts = async (category?: string, search?: string) => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (search) params.append('search', search); // Backend needs to support search

    const response = await client.get<any>('/products', { params });
    // Handle paginated response structure
    return response.data.items || response.data;
};

export const getProduct = async (id: number) => {
    const response = await client.get<any>(`/products/${id}`); // Changed to any as per instruction, but kept original URL and removed params
    // Handle paginated response structure
    return response.data.items || response.data;
};

export const getCategories = async () => {
    const response = await client.get('/categories');
    return response.data;
};
