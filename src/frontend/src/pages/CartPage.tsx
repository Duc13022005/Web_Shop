import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Trash2, Plus, Minus, ArrowRight, ShoppingBag, Tag, Package, Clock } from 'lucide-react';
import { Layout } from '../components/layout/Layout';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { cartService, Cart } from '../services/cartService';
import { client } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';
import { toast } from 'react-hot-toast';

type TabView = 'cart' | 'history';

export default function CartPage() {
    const { isAuthenticated } = useAuth();
    const { cart, refreshCart, updateItem, removeItem, cartItemCount } = useCart();
    const navigate = useNavigate();

    const [activeTab, setActiveTab] = useState<TabView>('cart');
    const [loading, setLoading] = useState(false);
    
    // Voucher states
    const [voucherCode, setVoucherCode] = useState('');
    const [appliedVoucher, setAppliedVoucher] = useState<{code: string, discount: number} | null>(null);

    // Order History states
    const [orders, setOrders] = useState<any[]>([]);
    const [loadingOrders, setLoadingOrders] = useState(false);

    // Component Mount
    useEffect(() => {
        if (!isAuthenticated) return;
        if (activeTab === 'history') {
            fetchOrders();
        }
    }, [isAuthenticated, activeTab]);

    const fetchOrders = async () => {
        setLoadingOrders(true);
        try {
            const res: any = await client.get(API_ENDPOINTS.ORDERS.LIST);
            setOrders(res.items || res); // Depending on backend response format
        } catch (err) {
            console.error("Failed to fetch orders", err);
            // Optionally set mock orders if no API exists yet
        } finally {
            setLoadingOrders(false);
        }
    };

    const handleQuantityChange = async (itemId: number, newQuantity: number) => {
        if (newQuantity < 1) return;
        await updateItem(itemId, newQuantity);
    };

    const handleRemoveItem = async (itemId: number) => {
        if (!confirm('Bạn có chắc muốn xóa sản phẩm này?')) return;
        await removeItem(itemId);
        toast.success("Đã xóa sản phẩm");
    };

    const handleApplyVoucher = () => {
        const mockVouchers: {[key: string]: number} = {
            'GIAM10K': 10000,
            'FREESHIP': 15000,
            'SALE20': 20000
        };

        const code = voucherCode.toUpperCase();
        if (mockVouchers[code]) {
            setAppliedVoucher({ code, discount: mockVouchers[code] });
            toast.success(`Áp dụng thành công voucher ${code}`);
        } else {
            setAppliedVoucher(null);
            toast.error("Mã giảm giá không hợp lệ");
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
                    <p className="text-gray-500 mb-6">Vui lòng đăng nhập để xem giỏ hàng và lịch sử mua hàng</p>
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

    const isEmpty = !cart || !cart.items || cart.items.length === 0;
    const subtotal = cart?.subtotal || 0;
    const discountAmount = appliedVoucher ? appliedVoucher.discount : 0;
    const total = Math.max(0, subtotal - discountAmount);

    return (
        <Layout>
            <div className="bg-gray-50 min-h-screen py-10">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    
                    {/* Tab Navigation */}
                    <div className="flex space-x-8 mb-8 border-b border-gray-200">
                        <button
                            onClick={() => setActiveTab('cart')}
                            className={`pb-4 text-lg font-bold transition-all relative ${activeTab === 'cart' ? 'text-brand-600' : 'text-gray-500 hover:text-gray-900'}`}
                        >
                            Đơn hàng của tôi
                            {activeTab === 'cart' && <span className="absolute bottom-0 left-0 w-full h-1 bg-brand-600 rounded-t-full"></span>}
                        </button>
                        <button
                            onClick={() => setActiveTab('history')}
                            className={`pb-4 text-lg font-bold transition-all relative ${activeTab === 'history' ? 'text-brand-600' : 'text-gray-500 hover:text-gray-900'}`}
                        >
                            Lịch sử mua hàng
                            {activeTab === 'history' && <span className="absolute bottom-0 left-0 w-full h-1 bg-brand-600 rounded-t-full"></span>}
                        </button>
                    </div>

                    {/* CART TAB */}
                    {activeTab === 'cart' && (
                        isEmpty ? (
                            <div className="text-center py-20 bg-white rounded-2xl shadow-sm">
                                <ShoppingBag size={64} className="mx-auto text-gray-300 mb-4" />
                                <p className="text-xl text-gray-500 mb-8">Giỏ hàng trống</p>
                                <Link to="/products" className="text-brand-600 font-bold hover:underline text-lg">
                                    Tiếp tục mua sắm
                                </Link>
                            </div>
                        ) : (
                            <div className="lg:grid lg:grid-cols-12 lg:gap-8 animate-fade-in">
                                {/* Cart Items */}
                                <div className="lg:col-span-8">
                                    <div className="bg-white rounded-2xl shadow-sm overflow-hidden mb-6">
                                        <ul className="divide-y divide-gray-100">
                                            {cart!.items.map((item) => (
                                                <li key={item.id} className="p-6 flex flex-col sm:flex-row items-center gap-6 hover:bg-gray-50 transition">
                                                    <div className="w-24 h-24 bg-gray-100 rounded-lg overflow-hidden shrink-0 border border-gray-200">
                                                        <img
                                                            src={item.image_path ? (item.image_path.startsWith('http') || item.image_path.startsWith('/') ? item.image_path : `/uploads/${item.image_path}`) : 'https://via.placeholder.com/200'}
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

                                {/* Summary & Voucher */}
                                <div className="lg:col-span-4">
                                    <div className="bg-white rounded-2xl shadow-sm p-6 mb-6">
                                        <h2 className="text-lg font-bold text-gray-900 mb-4 flex items-center gap-2">
                                            <Tag size={20} className="text-brand-600" />
                                            Khuyến mãi / Voucher
                                        </h2>
                                        <div className="flex gap-2">
                                            <input 
                                                type="text" 
                                                value={voucherCode}
                                                onChange={(e) => setVoucherCode(e.target.value)}
                                                placeholder="VD: GIAM10K, FREESHIP" 
                                                className="flex-1 px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 uppercase text-sm"
                                            />
                                            <button 
                                                onClick={handleApplyVoucher}
                                                className="px-4 py-2 bg-gray-900 text-white rounded-xl font-bold hover:bg-gray-800 text-sm"
                                            >
                                                Áp dụng
                                            </button>
                                        </div>
                                        {appliedVoucher && (
                                            <div className="mt-3 text-sm text-green-600 font-medium flex items-center justify-between">
                                                <span>✓ Đã áp dụng: {appliedVoucher.code}</span>
                                                <span>- {formatPrice(appliedVoucher.discount)}</span>
                                            </div>
                                        )}
                                    </div>

                                    <div className="bg-white rounded-2xl shadow-sm p-6 sticky top-24">
                                        <h2 className="text-lg font-bold text-gray-900 mb-6">Tổng đơn hàng</h2>
                                        <div className="space-y-4 mb-6">
                                            <div className="flex justify-between text-gray-600">
                                                <span>Tạm tính</span>
                                                <span className="font-medium">{formatPrice(subtotal)}</span>
                                            </div>
                                            {appliedVoucher && (
                                                <div className="flex justify-between text-green-600">
                                                    <span>Giảm giá ({appliedVoucher.code})</span>
                                                    <span className="font-medium">- {formatPrice(appliedVoucher.discount)}</span>
                                                </div>
                                            )}
                                            <div className="border-t border-gray-100 pt-4 flex justify-between text-lg font-bold text-gray-900">
                                                <span>Tổng cộng</span>
                                                <span className="text-brand-600 text-2xl">{formatPrice(total)}</span>
                                            </div>
                                        </div>

                                        <button
                                            onClick={() => navigate('/checkout')}
                                            className="w-full bg-brand-600 text-white font-bold py-4 rounded-xl hover:bg-brand-700 transition shadow-lg flex items-center justify-center gap-2 shadow-brand-600/30"
                                        >
                                            Xác nhận đặt hàng <ArrowRight size={20} />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        )
                    )}

                    {/* HISTORY TAB */}
                    {activeTab === 'history' && (
                        <div className="animate-fade-in">
                            {loadingOrders ? (
                                <div className="text-center py-20 text-gray-500">Đang tải lịch sử đơn hàng...</div>
                            ) : orders.length === 0 ? (
                                <div className="text-center py-20 bg-white rounded-2xl shadow-sm">
                                    <Clock size={64} className="mx-auto text-gray-300 mb-4" />
                                    <p className="text-xl text-gray-500">Bạn chưa có đơn hàng nào.</p>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    {orders.map((order: any) => (
                                        <div key={order.id} className="bg-white rounded-2xl shadow-sm p-6 border border-gray-100">
                                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4 pb-4 border-b border-gray-50">
                                                <div>
                                                    <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Mã đơn hàng</span>
                                                    <h3 className="font-bold text-gray-900 text-lg">#{order.id.toString().padStart(5, '0')}</h3>
                                                </div>
                                                <div className="flex flex-col sm:items-end">
                                                    <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Trạng thái</span>
                                                    <span className={`px-3 py-1 rounded-full text-sm font-bold mt-1 inline-block ${
                                                        order.status === 'pending' ? 'bg-yellow-100 text-yellow-700' :
                                                        order.status === 'processing' ? 'bg-blue-100 text-blue-700' :
                                                        order.status === 'completed' ? 'bg-green-100 text-green-700' :
                                                        'bg-gray-100 text-gray-700'
                                                    }`}>
                                                        {order.status === 'pending' ? 'Chờ xác nhận' :
                                                         order.status === 'processing' ? 'Đang giao' :
                                                         order.status === 'completed' ? 'Thành công' : 'Thất bại'}
                                                    </span>
                                                </div>
                                            </div>
                                            
                                            <div className="flex items-center justify-between">
                                                <div className="flex items-center gap-2 text-gray-600">
                                                    <Package size={20} />
                                                    <span>{order.total_items} sản phẩm</span>
                                                </div>
                                                <div className="text-right">
                                                    <span className="text-sm text-gray-500">Tổng tiền:</span>
                                                    <span className="ml-2 font-bold text-brand-600 text-xl">{formatPrice(order.total_amount)}</span>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    )}
                    
                </div>
            </div>
        </Layout>
    );
}
