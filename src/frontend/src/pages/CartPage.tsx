
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Trash2, Plus, Minus, ArrowRight, ShoppingBag } from 'lucide-react';
import { Layout } from '../components/layout/Layout';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { cartService, Cart } from '../services/cartService';
import { toast } from 'react-hot-toast';

export default function CartPage() {
    const { isAuthenticated } = useAuth();
    const { refreshCart } = useCart();

    const [cart, setCart] = useState<Cart | null>(null);
    const [loading, setLoading] = useState(true);

    const fetchCart = async () => {
        if (!isAuthenticated) return;
        setLoading(true);
        try {
            const data = await cartService.getCart();
            setCart(data);
        } catch (error) {
            console.error("Failed to fetch cart", error);
            toast.error("Không thể tải giỏ hàng");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (isAuthenticated) {
            fetchCart();
        } else {
            setLoading(false);
        }
    }, [isAuthenticated]);

    const handleQuantityChange = async (itemId: number, newQuantity: number) => {
        if (newQuantity < 1) return;
        try {
            await cartService.updateItem(itemId, newQuantity);
            fetchCart(); // Refresh cart data
            refreshCart(); // Refresh global count
        } catch (error) {
            console.error("Update failed", error);
            toast.error("Cập nhật số lượng thất bại");
        }
    };

    const handleRemoveItem = async (itemId: number) => {
        if (!confirm('Bạn có chắc muốn xóa sản phẩm này?')) return;
        try {
            await cartService.removeItem(itemId);
            toast.success("Đã xóa sản phẩm");
            fetchCart();
            refreshCart();
        } catch (error) {
            console.error("Remove failed", error);
            toast.error("Xóa thất bại");
        }
    };

    const formatPrice = (price: number) => {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price);
    };

    if (!isAuthenticated) {
        return (
            <Layout>
                <div className="min-h-[60vh] flex flex-col items-center justify-center p-4">
                    <ShoppingBag size={64} className="text-gray-300 mb-4" />
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">Giỏ hàng của bạn đang đợi</h2>
                    <p className="text-gray-500 mb-6">Vui lòng đăng nhập để xem giỏ hàng</p>
                    <Link
                        to="/login"
                        className="bg-brand-600 text-white px-8 py-3 rounded-xl font-bold hover:bg-brand-700 transition"
                    >
                        Đăng nhập ngay
                    </Link>
                </div>
            </Layout>
        );
    }

    if (loading) return <Layout><div className="flex justify-center items-center h-[50vh]"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div></div></Layout>;

    const isEmpty = !cart || !cart.items || cart.items.length === 0;

    return (
        <Layout>
            <div className="bg-gray-50 min-h-screen py-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-8">Giỏ hàng của bạn</h1>

                    {isEmpty ? (
                        <div className="text-center py-20 bg-white rounded-2xl shadow-sm">
                            <ShoppingBag size={64} className="mx-auto text-gray-300 mb-4" />
                            <p className="text-xl text-gray-500 mb-8">Giỏ hàng trống</p>
                            <Link to="/products" className="text-brand-600 font-bold hover:underline text-lg">
                                Tiếp tục mua sắm
                            </Link>
                        </div>
                    ) : (
                        <div className="lg:grid lg:grid-cols-12 lg:gap-8">
                            {/* Cart Items */}
                            <div className="lg:col-span-8">
                                <div className="bg-white rounded-2xl shadow-sm overflow-hidden mb-6">
                                    <ul className="divide-y divide-gray-100">
                                        {cart!.items.map((item) => (
                                            <li key={item.id} className="p-6 flex flex-col sm:flex-row items-center gap-6 hover:bg-gray-50 transition">
                                                <div className="w-24 h-24 bg-gray-100 rounded-lg overflow-hidden shrink-0 border border-gray-200">
                                                    <img
                                                        src={item.image_path ? (item.image_path.startsWith('http') ? item.image_path : `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/uploads/${item.image_path}`) : 'https://via.placeholder.com/200'}
                                                        alt={item.product_name}
                                                        className="w-full h-full object-cover"
                                                    />
                                                </div>
                                                <div className="flex-1 text-center sm:text-left w-full">
                                                    <h3 className="font-bold text-gray-900 text-lg mb-1">{item.product_name}</h3>
                                                    <p className="text-gray-500 text-sm mb-4">Mã SP: {item.product_sku}</p>
                                                    <div className="text-sm text-gray-500 mb-2 sm:hidden">
                                                        Đơn giá: {formatPrice(item.unit_price)}
                                                    </div>

                                                    <div className="flex items-center justify-center sm:justify-start gap-4">
                                                        <div className="flex items-center border border-gray-200 rounded-lg bg-white">
                                                            <button
                                                                onClick={() => handleQuantityChange(item.id, item.quantity - 1)}
                                                                className="p-2 hover:bg-gray-100 text-gray-600 transition"
                                                            >
                                                                <Minus size={16} />
                                                            </button>
                                                            <span className="w-10 text-center font-medium text-gray-900">{item.quantity}</span>
                                                            <button
                                                                onClick={() => handleQuantityChange(item.id, item.quantity + 1)}
                                                                className="p-2 hover:bg-gray-100 text-gray-600 transition"
                                                            >
                                                                <Plus size={16} />
                                                            </button>
                                                        </div>
                                                        <button
                                                            onClick={() => handleRemoveItem(item.id)}
                                                            className="text-gray-400 hover:text-red-500 p-2 transition"
                                                            title="Xóa sản phẩm"
                                                        >
                                                            <Trash2 size={18} />
                                                        </button>
                                                    </div>
                                                </div>
                                                <div className="text-right min-w-[120px]">
                                                    <div className="text-xs text-gray-400 mb-1 hidden sm:block">Thành tiền</div>
                                                    <p className="font-bold text-xl text-brand-600">{formatPrice(item.subtotal)}</p>
                                                </div>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>

                            {/* Summary */}
                            <div className="lg:col-span-4">
                                <div className="bg-white rounded-2xl shadow-sm p-6 sticky top-24">
                                    <h2 className="text-lg font-bold text-gray-900 mb-6">Tổng đơn hàng</h2>

                                    <div className="space-y-4 mb-6">
                                        <div className="flex justify-between text-gray-600">
                                            <span>Tạm tính</span>
                                            <span className="font-medium">{formatPrice(cart!.subtotal)}</span>
                                        </div>
                                        <div className="flex justify-between text-gray-600">
                                            <span>Phí vận chuyển</span>
                                            <span className="text-green-600 font-medium">Miễn phí</span>
                                        </div>
                                        <div className="border-t border-gray-100 pt-4 flex justify-between text-lg font-bold text-gray-900">
                                            <span>Tổng cộng</span>
                                            <span className="text-brand-600">{formatPrice(cart!.subtotal)}</span>
                                        </div>
                                    </div>

                                    <Link
                                        to="/checkout"
                                        className="w-full bg-brand-600 text-white font-bold py-4 rounded-xl hover:bg-brand-700 transition shadow-lg flex items-center justify-center gap-2 shadow-brand-600/30"
                                    >
                                        Thanh toán <ArrowRight size={20} />
                                    </Link>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </Layout>
    );
}
