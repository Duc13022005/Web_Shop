
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { cartService } from '../services/cartService';
import { useAuth } from './AuthContext'; // Assuming AuthContext exists

interface CartContextType {
    cartItemCount: number;
    refreshCart: () => Promise<void>;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider = ({ children }: { children: ReactNode }) => {
    const [cartItemCount, setCartItemCount] = useState(0);
    const { isAuthenticated } = useAuth(); // Assuming AuthContext exposes this

    const refreshCart = async () => {
        if (!isAuthenticated) {
            setCartItemCount(0);
            return;
        }
        try {
            const cart = await cartService.getCart();
            setCartItemCount(cart.total_items);
        } catch (error) {
            console.error("Failed to fetch cart count", error);
        }
    };

    useEffect(() => {
        refreshCart();
    }, [isAuthenticated]);

    return (
        <CartContext.Provider value={{ cartItemCount, refreshCart }}>
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
