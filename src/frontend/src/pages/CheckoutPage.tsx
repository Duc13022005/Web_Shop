
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Layout } from '../components/layout/Layout';
import { useAuth } from '../context/AuthContext';
import { client } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';

interface ShippingAddress {
    full_name: string;
    phone: string;
    address_line: string;
    city: string;
}

export default function CheckoutPage() {
    const { isAuthenticated, user } = useAuth();
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(false);
    const [cartTotal, setCartTotal] = useState(0);

    // Form State
    const [formData, setFormData] = useState<ShippingAddress>({
        full_name: user?.full_name || '',
        phone: '',
        address_line: '',
        city: 'Hanoi'
    });

    // Check auth and cart total on mount
    useEffect(() => {
        if (!isAuthenticated) {
            navigate('/login');
            return;
        }

        // Fetch cart total to display summary
        client.get(API_ENDPOINTS.CART.GET)
            .then((res: any) => {
                if (!res.items || res.items.length === 0) {
                    navigate('/cart'); // Empty cart, go back
                }
                setCartTotal(res.total_amount);
            })
            .catch(() => navigate('/cart'));
    }, [isAuthenticated, navigate]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            // Build shipping address string from form
            const shippingAddress = `${formData.full_name}, ${formData.phone}, ${formData.address_line}, ${formData.city}`;

            // Create Order
            // Payload match src/orders/schemas.py OrderCreate
            const payload = {
                shipping_address: shippingAddress,
                payment_method: "cod" // Defaulting to COD for Phase 2/3
            };

            // @ts-ignore
            const order: any = await client.post(API_ENDPOINTS.ORDERS.CREATE, payload);

            // Redirect to success
            navigate('/order-success', { state: { orderId: order.id } });

        } catch (error) {
            console.error("Checkout failed", error);
            alert("Checkout failed. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Layout>
            <div className="max-w-3xl mx-auto px-4 py-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-8">Checkout</h1>

                <div className="bg-white rounded-2xl shadow-sm p-6 md:p-8">
                    <form onSubmit={handleSubmit} className="space-y-6">

                        {/* Shipping Info */}
                        <div className="border-b border-gray-100 pb-6">
                            <h2 className="text-xl font-bold text-gray-900 mb-4">Shipping Information</h2>
                            <div className="grid grid-cols-1 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
                                    <input
                                        type="text"
                                        required
                                        className="w-full rounded-lg border-gray-300 focus:ring-brand-500 focus:border-brand-500"
                                        value={formData.full_name}
                                        onChange={e => setFormData({ ...formData, full_name: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                                    <input
                                        type="tel"
                                        required
                                        className="w-full rounded-lg border-gray-300 focus:ring-brand-500 focus:border-brand-500"
                                        value={formData.phone}
                                        onChange={e => setFormData({ ...formData, phone: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Address</label>
                                    <textarea
                                        required
                                        rows={3}
                                        className="w-full rounded-lg border-gray-300 focus:ring-brand-500 focus:border-brand-500"
                                        value={formData.address_line}
                                        onChange={e => setFormData({ ...formData, address_line: e.target.value })}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">City</label>
                                    <select
                                        className="w-full rounded-lg border-gray-300 focus:ring-brand-500 focus:border-brand-500"
                                        value={formData.city}
                                        onChange={e => setFormData({ ...formData, city: e.target.value })}
                                    >
                                        <option value="Hanoi">Hanoi</option>
                                        <option value="HCMC">Ho Chi Minh City</option>
                                        <option value="Danang">Da Nang</option>
                                    </select>
                                </div>
                            </div>
                        </div>

                        {/* Order Summary */}
                        <div className="border-b border-gray-100 pb-6">
                            <h2 className="text-xl font-bold text-gray-900 mb-4">Order Summary</h2>
                            <div className="flex justify-between text-lg font-bold">
                                <span>Total Amount</span>
                                <span>${cartTotal.toFixed(2)}</span>
                            </div>
                            <p className="text-sm text-gray-500 mt-2">Payment Method: Cash on Delivery (COD)</p>
                        </div>

                        {/* Submit */}
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full bg-brand-600 text-white font-bold py-4 rounded-xl hover:bg-brand-700 transition shadow-lg disabled:opacity-50"
                        >
                            {isLoading ? 'Processing Order...' : 'Place Order'}
                        </button>
                    </form>
                </div>
            </div>
        </Layout>
    );
}
