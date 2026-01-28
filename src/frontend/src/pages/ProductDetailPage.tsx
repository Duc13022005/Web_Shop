
import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { ShoppingCart, Minus, Plus, Heart, Share2, ArrowLeft, ChevronLeft, ChevronRight } from 'lucide-react';
import { Layout } from '../components/layout/Layout';
import { productService, Product } from '../services/productService';
import { cartService } from '../services/cartService';
import { useAuth } from '../context/AuthContext';
import { useCart } from '../context/CartContext';
import { toast } from 'react-hot-toast';

export default function ProductDetailPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const { isAuthenticated } = useAuth();
    const { refreshCart } = useCart();

    const [product, setProduct] = useState<Product | null>(null);
    const [loading, setLoading] = useState(true);
    const [quantity, setQuantity] = useState(1);
    const [selectedImage, setSelectedImage] = useState<string>('');
    const [activeTab, setActiveTab] = useState<'desc' | 'specs'>('desc');

    useEffect(() => {
        const fetchProduct = async () => {
            if (!id) return;
            try {
                const data = await productService.getById(id);
                setProduct(data);
                if (data.images && data.images.length > 0) {
                    setSelectedImage(data.images[0]);
                } else if (data.image_path) {
                    setSelectedImage(data.image_path);
                }
            } catch (error) {
                console.error("Failed to fetch product", error);
                toast.error("Không tìm thấy sản phẩm");
            } finally {
                setLoading(false);
            }
        };
        fetchProduct();
    }, [id]);

    const handleAddToCart = async () => {
        if (!isAuthenticated) {
            toast.error("Vui lòng đăng nhập để mua hàng");
            navigate('/login');
            return;
        }
        if (!product) return;

        try {
            await cartService.addToCart(product.id, quantity);
            toast.success("Đã thêm vào giỏ hàng!");
            refreshCart();
        } catch (error) {
            console.error("Add to cart error", error);
            toast.error("Có lỗi xảy ra khi thêm vào giỏ hàng");
        }
    };

    if (loading) {
        return (
            <Layout>
                <div className="flex justify-center items-center h-screen bg-gray-50">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-600"></div>
                </div>
            </Layout>
        );
    }

    if (!product) {
        return (
            <Layout>
                <div className="text-center py-20">Không tìm thấy sản phẩm</div>
            </Layout>
        );
    }

    const formatPrice = (price: number) => {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price);
    };

    const images = product.images && product.images.length > 0 ? product.images : (product.image_path ? [product.image_path] : ['https://via.placeholder.com/400']);

    return (
        <Layout>
            <div className="bg-gray-50 py-10 min-h-screen">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <Link to="/products" className="inline-flex items-center gap-2 text-gray-500 hover:text-brand-600 mb-6 font-medium transition">
                        <ArrowLeft size={18} /> Quay lại danh sách
                    </Link>

                    <div className="bg-white rounded-2xl shadow-sm overflow-hidden mb-10">
                        <div className="lg:flex">
                            {/* Left: Image Gallery */}
                            <div className="lg:w-1/2 p-6 sm:p-10">
                                <div className="relative aspect-square bg-gray-100 rounded-xl overflow-hidden mb-4 group border border-gray-100">
                                    <img
                                        src={selectedImage || 'https://via.placeholder.com/400'}
                                        alt={product.name}
                                        className="w-full h-full object-contain p-4 group-hover:scale-105 transition duration-500"
                                    />
                                    {images.length > 1 && (
                                        <>
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    const idx = images.indexOf(selectedImage);
                                                    const prevIdx = idx === 0 ? images.length - 1 : idx - 1;
                                                    setSelectedImage(images[prevIdx]);
                                                }}
                                                className="absolute left-4 top-1/2 -translate-y-1/2 bg-white/80 p-2 rounded-full shadow-sm hover:bg-white text-gray-700 transition opacity-0 group-hover:opacity-100"
                                            >
                                                <ChevronLeft size={24} />
                                            </button>
                                            <button
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    const idx = images.indexOf(selectedImage);
                                                    const nextIdx = idx === images.length - 1 ? 0 : idx + 1;
                                                    setSelectedImage(images[nextIdx]);
                                                }}
                                                className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/80 p-2 rounded-full shadow-sm hover:bg-white text-gray-700 transition opacity-0 group-hover:opacity-100"
                                            >
                                                <ChevronRight size={24} />
                                            </button>
                                        </>
                                    )}
                                </div>

                                {/* Thumbnails */}
                                {images.length > 1 && (
                                    <div className="flex gap-4 overflow-x-auto pb-2 scrollbar-hide">
                                        {images.map((img, idx) => (
                                            <button
                                                key={idx}
                                                onClick={() => setSelectedImage(img)}
                                                className={`flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-all ${selectedImage === img ? 'border-brand-600 opacity-100 ring-2 ring-brand-200' : 'border-gray-200 opacity-70 hover:opacity-100'}`}
                                            >
                                                <img src={img} alt="" className="w-full h-full object-cover" />
                                            </button>
                                        ))}
                                    </div>
                                )}
                            </div>

                            {/* Right: Product Info */}
                            <div className="lg:w-1/2 p-6 sm:p-10 lg:border-l border-gray-100">
                                <div className="flex justify-between items-start">
                                    <span className="bg-brand-50 text-brand-700 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide">
                                        {product.category_name || 'Sản phẩm'}
                                    </span>
                                    <div className="flex gap-2">
                                        <button className="p-2 text-gray-400 hover:text-red-500 rounded-full hover:bg-red-50 transition-colors">
                                            <Heart size={20} />
                                        </button>
                                        <button className="p-2 text-gray-400 hover:text-blue-500 rounded-full hover:bg-blue-50 transition-colors">
                                            <Share2 size={20} />
                                        </button>
                                    </div>
                                </div>

                                <h1 className="text-3xl font-bold text-gray-900 mt-4 mb-2">{product.name}</h1>
                                <p className="text-gray-500 text-sm mb-6">Mã SP: {product.sku}</p>

                                <div className="flex items-baseline gap-4 mb-8">
                                    <span className="text-4xl font-bold text-brand-600">
                                        {formatPrice(product.current_price)}
                                    </span>
                                    {product.sale_price && product.base_price > product.sale_price && (
                                        <span className="text-xl text-gray-400 line-through">
                                            {formatPrice(product.base_price)}
                                        </span>
                                    )}
                                </div>

                                <div className="prose prose-sm text-gray-600 mb-8 max-w-none">
                                    <p>{product.description}</p>
                                </div>

                                {/* Actions */}
                                <div className="border-t border-gray-100 pt-8 mt-auto">
                                    <div className="flex items-center justify-between mb-4">
                                        <span className="font-semibold text-gray-900">Số lượng</span>
                                        <span className={`text-sm font-medium ${product.available_stock > 0 ? 'text-green-600' : 'text-red-600'}`}>
                                            {product.available_stock > 0 ? `Còn hàng (${product.available_stock})` : 'Hết hàng'}
                                        </span>
                                    </div>
                                    <div className="flex flex-col sm:flex-row gap-4">
                                        <div className="flex items-center border-2 border-gray-200 rounded-xl w-fit">
                                            <button
                                                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                                                className="p-3 text-gray-600 hover:text-brand-600 transition"
                                                disabled={product.available_stock === 0}
                                            >
                                                <Minus size={20} />
                                            </button>
                                            <span className="w-12 text-center font-bold text-lg text-gray-900">{quantity}</span>
                                            <button
                                                onClick={() => setQuantity(Math.min(product.available_stock, quantity + 1))}
                                                className="p-3 text-gray-600 hover:text-brand-600 transition"
                                                disabled={product.available_stock === 0 || quantity >= product.available_stock}
                                            >
                                                <Plus size={20} />
                                            </button>
                                        </div>
                                        <button
                                            onClick={handleAddToCart}
                                            disabled={product.available_stock === 0}
                                            className="flex-1 bg-brand-600 text-white font-bold py-3 px-8 rounded-xl hover:bg-brand-700 transition-all flex items-center justify-center gap-2 shadow-lg shadow-brand-600/30 disabled:opacity-50 disabled:cursor-not-allowed"
                                        >
                                            <ShoppingCart size={20} />
                                            Thêm vào giỏ - {formatPrice(product.current_price * quantity)}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Tabs Section */}
                    <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
                        <div className="flex border-b border-gray-100">
                            <button
                                className={`flex-1 py-4 text-center font-semibold text-lg transition-colors relative ${activeTab === 'desc' ? 'text-brand-600 bg-brand-50/50' : 'text-gray-500 hover:text-gray-800'}`}
                                onClick={() => setActiveTab('desc')}
                            >
                                Mô tả chi tiết
                                {activeTab === 'desc' && <span className="absolute bottom-0 left-0 w-full h-0.5 bg-brand-600"></span>}
                            </button>
                            <button
                                className={`flex-1 py-4 text-center font-semibold text-lg transition-colors relative ${activeTab === 'specs' ? 'text-brand-600 bg-brand-50/50' : 'text-gray-500 hover:text-gray-800'}`}
                                onClick={() => setActiveTab('specs')}
                            >
                                Thông số sản phẩm
                                {activeTab === 'specs' && <span className="absolute bottom-0 left-0 w-full h-0.5 bg-brand-600"></span>}
                            </button>
                        </div>
                        <div className="p-8">
                            {activeTab === 'desc' ? (
                                <div className="prose max-w-none text-gray-600">
                                    <p>{product.description}</p>
                                </div>
                            ) : (
                                <div>
                                    {product.specifications && Object.keys(product.specifications).length > 0 ? (
                                        <div className="grid sm:grid-cols-2 gap-x-12 gap-y-4">
                                            {Object.entries(product.specifications).map(([key, value]) => (
                                                <div key={key} className="flex justify-between border-b border-gray-100 pb-2">
                                                    <span className="text-gray-500 font-medium capitalize">{key.replace(/_/g, ' ')}</span>
                                                    <span className="text-gray-900 font-semibold">{String(value)}</span>
                                                </div>
                                            ))}
                                        </div>
                                    ) : (
                                        <p className="text-gray-500 italic text-center">Chưa có thông số kỹ thuật.</p>
                                    )}
                                </div>
                            )}
                        </div>
                    </div>

                </div>
            </div>
        </Layout>
    );
}
