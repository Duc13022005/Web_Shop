
import { client } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';

export interface CartItem {
    id: number;
    product_id: number;
    quantity: number;
    product_name: string;
    product_sku: string;
    unit_price: number;
    subtotal: number;
    image_path?: string;
    available_stock: number;
    added_at: string;
}

export interface Cart {
    id: number;
    items: CartItem[];
    total_items: number;
    subtotal: number;
}

export const cartService = {
    getCart: async (): Promise<Cart> => {
        // @ts-ignore
        const response = await client.get(API_ENDPOINTS.CART.GET);
        return response as unknown as Cart;
    },

    addToCart: async (productId: number, quantity: number = 1): Promise<Cart> => {
        // @ts-ignore
        const response = await client.post(API_ENDPOINTS.CART.ADD_ITEM, { product_id: productId, quantity });
        return response as unknown as Cart;
    },

    updateItem: async (itemId: number, quantity: number): Promise<Cart> => {
        // @ts-ignore
        const response = await client.put(API_ENDPOINTS.CART.UPDATE_ITEM(itemId), { quantity });
        return response as unknown as Cart;
    },

    removeItem: async (itemId: number): Promise<Cart> => {
        // @ts-ignore
        const response = await client.delete(API_ENDPOINTS.CART.REMOVE_ITEM(itemId));
        return response as unknown as Cart;
    },

    clearCart: async (): Promise<void> => {
        // @ts-ignore
        await client.delete(API_ENDPOINTS.CART.CLEAR);
    }
};
