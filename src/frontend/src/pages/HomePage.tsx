import { useEffect, useState } from 'react';
import { ArrowRight, Truck, Shield, Clock, Phone } from 'lucide-react';
import { Layout } from '../components/layout/Layout';
import { ProductCard } from '../components/common/ProductCard';
import { getProducts, getCategories, Product } from '../api/products';
import { Link } from 'react-router-dom';

export default function HomePage() {
    const [products, setProducts] = useState<Product[]>([]);
    const [categories, setCategories] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [productsData, categoriesData] = await Promise.all([
                    getProducts(),
                    getCategories()
                ]);
                setProducts(productsData.slice(0, 10)); // Top 10 featured
                if (Array.isArray(categoriesData)) {
                    setCategories(categoriesData);
                }
            } catch (error) {
                console.error("Failed to fetch home data:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    return (
        <Layout>
            {/* 1. Hero Section */}
            <section className="bg-gradient-to-r from-brand-50 to-white relative overflow-hidden">
                <div className="max-w-7xl mx-auto px-4 py-12 md:py-20 flex flex-col md:flex-row items-center">
                    <div className="md:w-1/2 z-10">
                        <span className="bg-brand-100 text-brand-700 px-4 py-1 rounded-full text-sm font-bold tracking-wide mb-4 inline-block">
                            MIỄN PHÍ VẬN CHUYỂN ĐƠN TỪ 500K
                        </span>
                        <h1 className="text-4xl md:text-6xl font-extrabold text-gray-900 leading-tight mb-6">
                            Thực Phẩm Tươi, <br />
                            <span className="text-brand-500">Giao Siêu Tốc.</span>
                        </h1>
                        <p className="text-lg text-gray-600 mb-8 max-w-lg leading-relaxed">
                            Mang thực phẩm chất lượng tốt nhất đến cửa nhà bạn chỉ trong ít phút.
                            Rau củ, trái cây, thịt cá tươi ngon từ nhà cung cấp uy tín.
                        </p>
                        <div className="flex gap-4">
                            <Link to="/products" className="bg-brand-600 hover:bg-brand-700 text-white px-8 py-3.5 rounded-full font-bold text-lg transition shadow-lg hover:shadow-brand-500/30 flex items-center gap-2">
                                Mua Ngay <ArrowRight size={20} />
                            </Link>
                            <button className="text-gray-600 hover:text-brand-600 font-semibold px-6 py-3.5 rounded-full border border-gray-200 hover:border-brand-200 transition bg-white">
                                Xem Deal Hot
                            </button>
                        </div>
                    </div>

                    {/* Hero Image / Illustration */}
                    <div className="md:w-1/2 mt-10 md:mt-0 relative">
                        <div className="relative z-10 animate-float">
                            <img
                                src="https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=800&auto=format&fit=crop"
                                alt="Grocery Basket"
                                className="rounded-2xl shadow-2xl object-cover w-full max-w-lg mx-auto transform hover:rotate-2 transition duration-500"
                            />
                        </div>
                        {/* Decorative Blobs */}
                        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[120%] h-[120%] bg-brand-200/20 rounded-full filter blur-3xl -z-0"></div>
                    </div>
                </div>
            </section>

            {/* Features Bar */}
            <section className="bg-white border-b border-gray-100">
                <div className="max-w-7xl mx-auto px-4 py-8">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        {[
                            { icon: Truck, title: "Miễn Phí Vận Chuyển", desc: "Cho đơn hàng từ 500k" },
                            { icon: Clock, title: "Giao Hàng Nhanh", desc: "Giao trong 30 phút" },
                            { icon: Shield, title: "Thanh Toán An Toàn", desc: "Bảo mật 100%" },
                            { icon: Phone, title: "Hỗ Trợ 24/7", desc: "Tư vấn tận tâm" },
                        ].map((feature, idx) => (
                            <div key={idx} className="flex items-center gap-4 p-4 rounded-lg hover:bg-gray-50 transition border border-transparent hover:border-gray-100">
                                <div className="w-12 h-12 bg-brand-50 text-brand-600 rounded-full flex items-center justify-center shrink-0">
                                    <feature.icon size={24} />
                                </div>
                                <div>
                                    <h4 className="font-bold text-gray-900">{feature.title}</h4>
                                    <p className="text-xs text-gray-500">{feature.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* 2. Categories Rail */}
            <section className="py-12 bg-gray-50">
                <div className="max-w-7xl mx-auto px-4">
                    <div className="flex items-center justify-between mb-8">
                        <h2 className="text-2xl font-bold text-gray-900">Danh Mục Phổ Biến</h2>
                        <Link to="/products" className="text-brand-600 font-semibold hover:underline flex items-center gap-1">
                            Xem Tất Cả <ArrowRight size={16} />
                        </Link>
                    </div>

                    <div className="flex gap-6 overflow-x-auto pb-4 scrollbar-hide">
                        {categories.map((cat) => (
                            <Link key={cat.id} to={`/products?category=${cat.slug}`} className="flex flex-col items-center gap-3 group min-w-[100px] cursor-pointer">
                                <div className="w-24 h-24 rounded-full overflow-hidden border-2 border-white shadow-md group-hover:border-brand-500 transition-all duration-300 bg-white flex items-center justify-center">
                                    <span className="text-2xl font-bold text-brand-500">{cat.name[0]}</span>
                                </div>
                                <span className="font-medium text-gray-700 group-hover:text-brand-600 transition text-center whitespace-nowrap">{cat.name}</span>
                            </Link>
                        ))}
                    </div>
                </div>
            </section>

            {/* 3. Featured Products Grid */}
            <section className="py-12 bg-white">
                <div className="max-w-7xl mx-auto px-4">
                    <div className="flex items-center justify-between mb-8">
                        <h2 className="text-3xl font-bold text-gray-900">Sản Phẩm Nổi Bật</h2>
                        <div className="flex gap-2">
                            <button className="px-4 py-2 rounded-full bg-brand-600 text-white text-sm font-medium">Tất cả</button>
                            <button className="px-4 py-2 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200 text-sm font-medium transition">Rau củ</button>
                            <button className="px-4 py-2 rounded-full bg-gray-100 text-gray-600 hover:bg-gray-200 text-sm font-medium transition">Trái cây</button>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
                        {loading ? (
                            Array(5).fill(0).map((_, i) => (
                                <div key={i} className="h-80 bg-gray-100 rounded-xl animate-pulse"></div>
                            ))
                        ) : (
                            products.map((product) => (
                                <ProductCard
                                    key={product.id}
                                    id={product.id}
                                    name={product.name}
                                    category="Sản phẩm"
                                    price={product.base_price || 0}
                                    originalPrice={product.sale_price || undefined}
                                    image={product.image_url || 'https://placehold.co/400'}
                                    rating={5.0}
                                    reviews={0}
                                    unit="đ"
                                />
                            ))
                        )}
                    </div>

                    <div className="mt-12 text-center">
                        <Link to="/products" className="inline-block px-8 py-3 bg-gray-900 text-white font-bold rounded-lg hover:bg-gray-800 transition shadow-lg">
                            Xem Thêm Sản Phẩm
                        </Link>
                    </div>
                </div>
            </section>

            {/* 4. Promo Banners */}
            <section className="py-12 bg-gray-50">
                <div className="max-w-7xl mx-auto px-4">
                    <div className="grid md:grid-cols-2 gap-8">
                        <div className="bg-orange-100 rounded-2xl p-8 flex items-center justify-between relative overflow-hidden group hover:shadow-xl transition duration-300">
                            <div className="z-10 relative max-w-[60%]">
                                <span className="text-orange-600 font-bold tracking-wider text-xs uppercase mb-2 block">Ưu Đãi Có Hạn</span>
                                <h3 className="text-3xl font-extrabold text-gray-900 mb-4">Trái Cây <br />Giảm Sốc - 30%</h3>
                                <button className="bg-gray-900 text-white px-6 py-2 rounded-lg text-sm font-bold hover:bg-orange-600 transition">Mua Ngay</button>
                            </div>
                            <img src="https://images.unsplash.com/photo-1610832958506-aa56368176cf?auto=format&fit=crop&q=80&w=300" className="absolute right-0 bottom-0 top-0 object-contain h-full w-1/2 group-hover:scale-110 transition duration-500" alt="Fruit" />
                        </div>

                        <div className="bg-green-100 rounded-2xl p-8 flex items-center justify-between relative overflow-hidden group hover:shadow-xl transition duration-300">
                            <div className="z-10 relative max-w-[60%]">
                                <span className="text-green-600 font-bold tracking-wider text-xs uppercase mb-2 block">Hàng Mới Về</span>
                                <h3 className="text-3xl font-extrabold text-gray-900 mb-4">Rau Củ <br />Hữu Cơ Sạch</h3>
                                <button className="bg-gray-900 text-white px-6 py-2 rounded-lg text-sm font-bold hover:bg-green-600 transition">Khám Phá</button>
                            </div>
                            <img src="https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&q=80&w=300" className="absolute right-0 bottom-0 top-0 object-contain h-full w-1/2 group-hover:scale-110 transition duration-500" alt="Veg" />
                        </div>
                    </div>
                </div>
            </section>
        </Layout>
    );
}
