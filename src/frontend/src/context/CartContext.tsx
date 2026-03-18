import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { cartService, Cart, CartItem } from '../services/cartService';
import { useAuth } from './AuthContext'; 

interface CartContextType {
    cart: Cart | null;
    cartItemCount: number;
    refreshCart: () => Promise<void>;
    addToCart: (productId: number, quantity?: number) => Promise<void>;
    updateItem: (itemId: number, quantity: number) => Promise<void>;
    removeItem: (itemId: number) => Promise<void>;
    clearCart: () => Promise<void>;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider = ({ children }: { children: ReactNode }) => {
    const [cart, setCart] = useState<Cart | null>(null);
    const { isAuthenticated } = useAuth();

    const refreshCart = async () => {
        if (!isAuthenticated) {
            setCart(null);
            return;
        }
        try {
            const fetchedCart = await cartService.getCart();
            setCart(fetchedCart);
        } catch (error) {
            console.error("Failed to fetch cart", error);
        }
    };

    useEffect(() => {
        refreshCart();
    }, [isAuthenticated]);

    const addToCart = async (productId: number, quantity: number = 1) => {
        if (!isAuthenticated) return;
        const updatedCart = await cartService.addToCart(productId, quantity);
        setCart(updatedCart);
    };

    const updateItem = async (itemId: number, quantity: number) => {
        if (!isAuthenticated) return;
        const updatedCart = await cartService.updateItem(itemId, quantity);
        setCart(updatedCart);
    };

    const removeItem = async (itemId: number) => {
        if (!isAuthenticated) return;
        const updatedCart = await cartService.removeItem(itemId);
        setCart(updatedCart);
    };

    const clearCart = async () => {
        if (!isAuthenticated) return;
        await cartService.clearCart();
        await refreshCart();
    };

    return (
        <CartContext.Provider value={{
            cart,
            cartItemCount: cart?.total_items || 0,
            refreshCart,
            addToCart,
            updateItem,
            removeItem,
            clearCart
        }}>
            {children}
        </CartContext.Provider>
    );
};

export const useCart = () => {
    const context = useContext(CartContext);
    if (!context) {
        throw new Error('useCart must be used within a CartProvider');
    }
    return context;
};
