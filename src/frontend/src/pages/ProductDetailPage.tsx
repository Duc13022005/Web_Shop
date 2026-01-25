
import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Star, Minus, Plus, ShoppingCart, ArrowLeft, Heart, Share2 } from 'lucide-react';
import { Layout } from '../components/layout/Layout';
import { client } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';

interface ProductDetail {
    id: number;
    name: string;
    description: string;
    price: number;
    images?: string[];
    category_name: string;
    available_stock: number;
    sku: string;
}

export default function ProductDetailPage() {
    const { id } = useParams();
    const [product, setProduct] = useState<ProductDetail | null>(null);
    const [quantity, setQuantity] = useState(1);
    const [activeTab, setActiveTab] = useState<'desc' | 'reviews'>('desc');
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchProduct = async () => {
            if (!id) return;
            try {
                // @ts-ignore
                const data: any = await client.get(API_ENDPOINTS.PRODUCTS.DETAIL(Number(id)));
                setProduct(data);
            } catch (err) {
                console.error(err);
                setError('Failed to load product');
            } finally {
                setIsLoading(false);
            }
        };
        fetchProduct();
    }, [id]);

    if (isLoading) return <Layout><div className="p-20 text-center">Loading...</div></Layout>;
    if (error || !product) return <Layout><div className="p-20 text-center text-red-500">{error || 'Product not found'}</div></Layout>;

    // Use fetched images or fallback
    const mainImage = product.images && product.images.length > 0
        ? product.images[0]
        : 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=800&q=80';

    return (
        <Layout>
            <div className="max-w-7xl mx-auto px-4 py-8">
                <Link to="/products" className="inline-flex items-center gap-2 text-gray-500 hover:text-brand-600 mb-6 font-medium transition">
                    <ArrowLeft size={18} /> Back to Catalog
                </Link>

                {/* Product Main Section */}
                <div className="grid md:grid-cols-2 gap-10 bg-white p-6 md:p-10 rounded-2xl shadow-sm mb-12">
                    {/* Left: Images */}
                    <div className="space-y-4">
                        <div className="aspect-square bg-gray-50 rounded-xl overflow-hidden border border-gray-100">
                            <img src={mainImage} alt={product.name} className="w-full h-full object-cover hover:scale-105 transition duration-500" />
                        </div>
                        {/* Thumbnails (mock logic for now if only 1 image) */}
                        <div className="grid grid-cols-4 gap-4">
                            {product.images && product.images.length > 1 ? (
                                product.images.map((img, i) => (
                                    <div key={i} className="aspect-square rounded-lg border-2 border-transparent hover:border-gray-200 cursor-pointer overflow-hidden">
                                        <img src={img} alt="Thumbnail" className="w-full h-full object-cover" />
                                    </div>
                                ))
                            ) : (
                                [1, 2, 3].map((_, i) => (
                                    <div key={i} className={`aspect-square rounded-lg border-2 cursor-pointer overflow-hidden ${i === 0 ? 'border-brand-500' : 'border-transparent hover:border-gray-200'}`}>
                                        <img src={mainImage} alt="Thumbnail" className="w-full h-full object-cover" />
                                    </div>
                                ))
                            )}
                        </div>
                    </div>

                    {/* Right: Info */}
                    <div className="flex flex-col">
                        <div className="flex items-center justify-between mb-2">
                            <span className="bg-brand-50 text-brand-700 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide">
                                {product.category_name}
                            </span>
                            <div className="flex gap-2 text-gray-400">
                                <button className="hover:text-red-500 transition"><Heart size={20} /></button>
                                <button className="hover:text-blue-500 transition"><Share2 size={20} /></button>
                            </div>
                        </div>

                        <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 mb-4">{product.name}</h1>
                        <p className="text-sm text-gray-500 mb-2">SKU: {product.sku}</p>

                        <div className="flex items-center gap-4 mb-6">
                            <div className="flex items-center text-yellow-400 gap-1">
                                <Star size={18} fill="currentColor" />
                                <Star size={18} fill="currentColor" />
                                <Star size={18} fill="currentColor" />
                                <Star size={18} fill="currentColor" />
                                <Star size={18} className="text-gray-300" />
                            </div>
                            <span className="text-sm text-gray-500 font-medium">(0 reviews)</span>
                            <span className="w-1 h-1 bg-gray-300 rounded-full"></span>
                            {product.available_stock > 0 ? (
                                <span className="text-green-600 font-medium text-sm">In Stock ({product.available_stock})</span>
                            ) : (
                                <span className="text-red-600 font-medium text-sm">Out of Stock</span>
                            )}
                        </div>

                        <div className="text-4xl font-bold text-brand-600 mb-6">${product.price}</div>

                        <p className="text-gray-600 leading-relaxed mb-8 border-t border-b border-gray-100 py-6">
                            {product.description || "No description available."}
                        </p>

                        {/* Action Buttons */}
                        <div className="flex flex-col sm:flex-row gap-4 mt-auto">
                            <div className="flex items-center border-2 border-gray-200 rounded-xl overflow-hidden w-fit">
                                <button
                                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                                    className="p-3 hover:bg-gray-100 text-gray-600 transition"
                                    disabled={product.available_stock === 0}
                                >
                                    <Minus size={20} />
                                </button>
                                <span className="w-12 text-center font-bold text-lg">{quantity}</span>
                                <button
                                    onClick={() => setQuantity(Math.min(product.available_stock, quantity + 1))}
                                    className="p-3 hover:bg-gray-100 text-gray-600 transition"
                                    disabled={product.available_stock === 0 || quantity >= product.available_stock}
                                >
                                    <Plus size={20} />
                                </button>
                            </div>

                            <button
                                className="flex-1 bg-gray-900 text-white font-bold py-3 px-8 rounded-xl hover:bg-brand-600 transition-colors shadow-lg flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed"
                                disabled={product.available_stock === 0}
                            >
                                <ShoppingCart size={20} />
                                {product.available_stock > 0 ? `Add to Cart - $${(product.price * quantity).toFixed(2)}` : 'Out of Stock'}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Tabs: Description & Reviews */}
                <div className="bg-white rounded-2xl p-8 shadow-sm">
                    <div className="flex gap-8 border-b border-gray-100 mb-6">
                        <button
                            className={`pb-4 font-bold text-lg relative ${activeTab === 'desc' ? 'text-brand-600' : 'text-gray-500 hover:text-gray-800'}`}
                            onClick={() => setActiveTab('desc')}
                        >
                            Description
                            {activeTab === 'desc' && <span className="absolute bottom-0 left-0 w-full h-0.5 bg-brand-600"></span>}
                        </button>
                        <button
                            className={`pb-4 font-bold text-lg relative ${activeTab === 'reviews' ? 'text-brand-600' : 'text-gray-500 hover:text-gray-800'}`}
                            onClick={() => setActiveTab('reviews')}
                        >
                            Reviews
                            {activeTab === 'reviews' && <span className="absolute bottom-0 left-0 w-full h-0.5 bg-brand-600"></span>}
                        </button>
                    </div>

                    <div className="text-gray-600 leading-relaxed">
                        {activeTab === 'desc' ? (
                            <div>
                                <p className="mb-4">
                                    {product.description}
                                </p>
                            </div>
                        ) : (
                            <div className="space-y-6">
                                <p className="text-gray-500 italic">No reviews yet.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </Layout>
    );
}
