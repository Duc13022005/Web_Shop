
import { useLocation, Link } from 'react-router-dom';
import { CheckCircle, Home } from 'lucide-react';
import { Layout } from '../components/layout/Layout';

export default function OrderSuccessPage() {
    const location = useLocation();
    const orderId = location.state?.orderId;

    return (
        <Layout>
            <div className="min-h-[70vh] flex flex-col items-center justify-center p-4 text-center">
                <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mb-6 text-green-600">
                    <CheckCircle size={40} />
                </div>

                <h1 className="text-3xl font-bold text-gray-900 mb-4">Order Placed Successfully!</h1>

                {orderId ? (
                    <p className="text-lg text-gray-600 mb-8">
                        Thank you for your purchase. Your order ID is <span className="font-bold text-gray-900">#{orderId}</span>.
                    </p>
                ) : (
                    <p className="text-lg text-gray-600 mb-8">Thank you for your purchase.</p>
                )}

                <div className="flex gap-4">
                    <Link
                        to="/"
                        className="inline-flex items-center gap-2 bg-gray-900 text-white px-6 py-3 rounded-xl font-bold hover:bg-brand-600 transition"
                    >
                        <Home size={20} /> Return Home
                    </Link>
                    <Link
                        to="/products"
                        className="inline-flex items-center gap-2 bg-gray-100 text-gray-700 px-6 py-3 rounded-xl font-bold hover:bg-gray-200 transition"
                    >
                        Continue Shopping
                    </Link>
                </div>
            </div>
        </Layout>
    );
}
