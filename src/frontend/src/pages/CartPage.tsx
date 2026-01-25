
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Trash2, Plus, Minus, ArrowRight, ShoppingBag } from 'lucide-react';
import { Layout } from '../components/layout/Layout';
import { useAuth } from '../context/AuthContext';
import { client } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';

interface CartItem {
    id: number; // Cart Item ID, not Product ID
    product_id: number;
    product_name: string;
    product_image?: string;
    quantity: number;
    price: number;
    total: number;
}

interface Cart {
    id: number;
    items: CartItem[];
    total_amount: number;
}

export default function CartPage() {
    const { isAuthenticated } = useAuth();
    const [cart, setCart] = useState<Cart | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    const fetchCart = async () => {
        if (!isAuthenticated) return;
        setIsLoading(true);
        try {
            // @ts-ignore
            const data: any = await client.get(API_ENDPOINTS.CART.GET);
            setCart(data);
        } catch (error) {
            console.error("Failed to fetch cart", error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        if (isAuthenticated) {
            fetchCart();
        } else {
            setIsLoading(false);
        }
    }, [isAuthenticated]);

    const handleQuantityChange = async (itemId: number, newQuantity: number) => {
        if (newQuantity < 1) return;
        // Optimistic UI update could be done here, but let's just wait for API for safety
        try {
            // Phase 2 API might expect specific payload structure. 
            // Assuming simplified update for now or just generic 'update item' endpoint.
            // If API not fully ready for detailed granular updates, implementation might vary.
            // But let's assume standard REST: PUT /cart/items/{id}

            // NOTE: Checking standard REST practice or re-reading endpoints if needed.
            // Assuming API_ENDPOINTS.CART.UPDATE_ITEM(itemId)
            await client.put(API_ENDPOINTS.CART.UPDATE_ITEM(itemId), { quantity: newQuantity });
            fetchCart();
        } catch (error) {
            console.error("Update failed", error);
        }
    };

    const handleRemoveItem = async (itemId: number) => {
        if (!confirm('Remove this item?')) return;
        try {
            await client.delete(API_ENDPOINTS.CART.REMOVE_ITEM(itemId));
            fetchCart();
        } catch (error) {
            console.error("Remove failed", error);
        }
    };

    if (!isAuthenticated) {
        return (
            <Layout>
                <div className="min-h-[60vh] flex flex-col items-center justify-center p-4">
                    <ShoppingBag size={64} className="text-gray-300 mb-4" />
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">Your cart is waiting</h2>
                    <p className="text-gray-500 mb-6">Please sign in to view your cart items</p>
                    <Link
                        to="/login"
                        className="bg-brand-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-brand-700 transition"
                    >
                        Sign In Now
                    </Link>
                </div>
            </Layout>
        );
    }

    if (isLoading) return <Layout><div className="p-20 text-center">Loading Cart...</div></Layout>;

    const isEmpty = !cart || !cart.items || cart.items.length === 0;

    return (
        <Layout>
            <div className="max-w-7xl mx-auto px-4 py-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">Shopping Cart</h1>

                {isEmpty ? (
                    <div className="text-center py-20 bg-white rounded-2xl shadow-sm">
                        <ShoppingBag size={48} className="mx-auto text-gray-300 mb-4" />
                        <p className="text-xl text-gray-500 mb-8">Your cart is empty</p>
                        <Link to="/products" className="text-brand-600 font-bold hover:underline text-lg">
                            Start Shopping
                        </Link>
                    </div>
                ) : (
                    <div className="lg:grid lg:grid-cols-12 lg:gap-8">
                        {/* Cart Items */}
                        <div className="lg:col-span-8">
                            <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
                                <ul className="divide-y divide-gray-100">
                                    {cart!.items.map((item) => (
                                        <li key={item.id} className="p-6 flex flex-col sm:flex-row items-center gap-6 hover:bg-gray-50 transition">
                                            <div className="w-24 h-24 bg-gray-100 rounded-lg overflow-hidden shrink-0">
                                                <img
                                                    src={item.product_image || 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=200&q=80'}
                                                    alt={item.product_name}
                                                    className="w-full h-full object-cover"
                                                />
                                            </div>
                                            <div className="flex-1 text-center sm:text-left">
                                                <h3 className="font-bold text-gray-900 text-lg mb-1">{item.product_name}</h3>
                                                <p className="text-gray-500 text-sm mb-4">${item.price.toFixed(2)}</p>

                                                <div className="flex items-center justify-center sm:justify-start gap-4">
                                                    <div className="flex items-center border border-gray-200 rounded-lg">
                                                        <button
                                                            onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                                                            className="p-2 hover:bg-gray-100 text-gray-500"
                                                        >
                                                            <Minus size={16} />
                                                        </button>
                                                        <span className="w-10 text-center font-medium">{item.quantity}</span>
                                                        <button
                                                            onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                                                            className="p-2 hover:bg-gray-100 text-gray-500"
                                                        >
                                                            <Plus size={16} />
                                                        </button>
                                                    </div>
                                                    <button
                                                        onClick={() => handleRemoveItem(item.id)}
                                                        className="text-red-500 hover:text-red-700 p-2"
                                                        title="Remove item"
                                                    >
                                                        <Trash2 size={18} />
                                                    </button>
                                                </div>
                                            </div>
                                            <div className="text-right">
                                                <p className="font-bold text-xl text-brand-600">${item.total.toFixed(2)}</p>
                                            </div>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>

                        {/* Summary */}
                        <div className="lg:col-span-4 mt-8 lg:mt-0">
                            <div className="bg-white rounded-2xl shadow-sm p-6 sticky top-24">
                                <h2 className="text-lg font-bold text-gray-900 mb-6">Order Summary</h2>

                                <div className="space-y-4 mb-6">
                                    <div className="flex justify-between text-gray-600">
                                        <span>Subtotal</span>
                                        <span className="font-medium">${cart!.total_amount.toFixed(2)}</span>
                                    </div>
                                    <div className="flex justify-between text-gray-600">
                                        <span>Shipping</span>
                                        <span className="text-green-600 font-medium">Free</span>
                                    </div>
                                    <div className="border-t border-gray-100 pt-4 flex justify-between text-lg font-bold text-gray-900">
                                        <span>Total</span>
                                        <span>${cart!.total_amount.toFixed(2)}</span>
                                    </div>
                                </div>

                                <Link
                                    to="/checkout"
                                    className="w-full bg-gray-900 text-white font-bold py-4 rounded-xl hover:bg-brand-600 transition shadow-lg flex items-center justify-center gap-2"
                                >
                                    Proceed to Checkout <ArrowRight size={20} />
                                </Link>
                                <p className="text-center text-xs text-gray-400 mt-4">
                                    Secure Checkout powered by Stripe (Mock)
                                </p>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </Layout>
    );
}
