
import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Filter, ChevronDown, Check } from 'lucide-react';
import { Layout } from '../components/layout/Layout';
import { ProductCard } from '../components/common/ProductCard';
import { client } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';

interface Category {
    id: number;
    name: string;
    description: string;
}

interface Product {
    id: number;
    name: string;
    price: number;
    images?: string[];
    description: string;
    category?: Category;
    category_name?: string;
    is_active: boolean;
}

export default function CatalogPage() {
    const [products, setProducts] = useState<Product[]>([]);
    const [categories, setCategories] = useState<Category[]>([]);
    const [selectedCategoryId, setSelectedCategoryId] = useState<number | null>(null);
    const [priceRange, setPriceRange] = useState<number>(1000000); // Default to 1M VND
    const [isMobileFilterOpen, setIsMobileFilterOpen] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    const [searchParams] = useSearchParams();
    const categoryQuery = searchParams.get('category');
    const searchQuery = searchParams.get('search');

    // Fetch Categories
    useEffect(() => {
        const fetchCategories = async () => {
            try {
                // @ts-ignore
                const res: any = await client.get(API_ENDPOINTS.PRODUCTS.CATEGORIES);
                setCategories(res.items || []);
            } catch (err) {
                console.error("Failed to fetch categories", err);
            }
        };
        fetchCategories();
    }, []);

    // Effect to update selected category based on URL query and loaded categories
    useEffect(() => {
        if (categories.length > 0 && categoryQuery && categoryQuery !== 'Tất cả') {
            const found = categories.find(c => 
                c.name.toLowerCase() === categoryQuery.toLowerCase() || 
                (c as any).slug?.toLowerCase() === categoryQuery.toLowerCase()
            );
            if (found) {
                setSelectedCategoryId(found.id);
            } else {
                setSelectedCategoryId(null);
            }
        } else if (categoryQuery === 'Tất cả' || categoryQuery === 'Tất cả sản phẩm') {
            setSelectedCategoryId(null);
        }
    }, [categories, categoryQuery]);

    // Fetch Products (with filters)
    useEffect(() => {
        const fetchProducts = async () => {
            setIsLoading(true);
            try {
                const params: any = { size: 100 }; // Fetch up to 100 for now
                if (selectedCategoryId) {
                    params.category_id = selectedCategoryId;
                }
                if (searchQuery) {
                    params.search = searchQuery;
                }
                // Optional: Server side price filtering
                // params.max_price = priceRange; 

                // @ts-ignore
                const res: any = await client.get(API_ENDPOINTS.PRODUCTS.LIST, { params });
                console.log("📦 CATALOG API RESPONSE:", res); // DEBUG

                // If using server side filtering, we use res.items.
                // If client side filtering for price (smoother slider), we filter here.
                // Mapping: Backend (current_price) -> Frontend (price)
                let items = (res.items || []).map((p: any) => ({
                    ...p,
                    price: Number(p.current_price || p.base_price || 0),
                    images: p.image_path
                        ? [p.image_path.startsWith('http') || p.image_path.startsWith('/')
                            ? p.image_path
                            : `/uploads/${p.image_path}`]
                        : []
                }));

                // Client-side Price Filter
                items = items.filter((p: any) => p.price <= priceRange);

                // Client-side Search Filter (in case backend ignores search param)
                if (searchQuery) {
                    const term = searchQuery.toLowerCase();
                    items = items.filter((p: any) => 
                        p.name.toLowerCase().includes(term) || 
                        (p.description && p.description.toLowerCase().includes(term))
                    );
                }

                setProducts(items);
            } catch (err) {
                console.error("Failed to fetch products", err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchProducts();
    }, [selectedCategoryId, priceRange, searchQuery]); // Re-fetch or re-filter when these change

    const FilterContent = () => (
        <div className="space-y-8">
            {/* Categories Filter */}
            <div>
                <h3 className="font-bold text-gray-900 mb-4 flex items-center justify-between">
                    Danh Mục
                    <ChevronDown size={16} />
                </h3>
                <ul className="space-y-3">
                    <li
                        className={`cursor-pointer flex items-center gap-3 text-sm ${!selectedCategoryId ? 'font-bold text-brand-600' : 'text-gray-600'}`}
                        onClick={() => setSelectedCategoryId(null)}
                    >
                        <div className={`w-5 h-5 rounded border flex items-center justify-center ${!selectedCategoryId ? 'bg-brand-600 border-brand-600 text-white' : 'border-gray-300'}`}>
                            {!selectedCategoryId && <Check size={12} />}
                        </div>
                        Tất cả sản phẩm
                    </li>
                    {categories.map(cat => (
                        <li
                            key={cat.id}
                            className={`cursor-pointer flex items-center gap-3 text-sm ${selectedCategoryId === cat.id ? 'font-bold text-brand-600' : 'text-gray-600'}`}
                            onClick={() => setSelectedCategoryId(cat.id)}
                        >
                            <div className={`w-5 h-5 rounded border flex items-center justify-center ${selectedCategoryId === cat.id ? 'bg-brand-600 border-brand-600 text-white' : 'border-gray-300'}`}>
                                {selectedCategoryId === cat.id && <Check size={12} />}
                            </div>
                            {cat.name}
                        </li>
                    ))}
                </ul>
            </div>

            {/* Price Range Filter */}
            <div>
                <h3 className="font-bold text-gray-900 mb-4">Khoảng Giá</h3>
                <input
                    type="range"
                    min="0"
                    max="1000000" // Increased max price for VND
                    step="10000"
                    value={priceRange}
                    onChange={(e) => setPriceRange(Number(e.target.value))}
                    className="w-full accent-brand-600 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="flex justify-between text-sm text-gray-600 mt-2 font-medium">
                    <span>0đ</span>
                    <span className="text-brand-600 font-bold">Max: {priceRange.toLocaleString('vi-VN')}đ</span>
                </div>
            </div>
        </div>
    );

    return (
        <Layout>
            <div className="bg-gray-50 min-h-screen py-8">
                <div className="max-w-7xl mx-auto px-4">

                    {/* Header & Mobile Filter Toggle */}
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">Danh Sách Sản Phẩm</h1>
                            <p className="text-gray-500 mt-1">
                                {isLoading ? 'Đang tải...' : `Hiển thị ${products.length} kết quả`}
                            </p>
                        </div>
                        <button
                            className="md:hidden flex items-center gap-2 bg-white px-4 py-2 rounded-lg border border-gray-200 shadow-sm font-medium text-gray-700"
                            onClick={() => setIsMobileFilterOpen(true)}
                        >
                            <Filter size={18} /> Bộ lọc
                        </button>
                    </div>

                    <div className="flex gap-8">
                        {/* Sidebar (Desktop) */}
                        <aside className="hidden md:block w-64 shrink-0">
                            <div className="bg-white p-6 rounded-xl shadow-sm sticky top-24">
                                <FilterContent />
                            </div>
                        </aside>

                        {/* Product Grid */}
                        <div className="flex-grow">
                            {isLoading ? (
                                <div className="text-center py-20">Đang tải sản phẩm...</div>
                            ) : products.length > 0 ? (
                                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                                    {products.map(product => (
                                        <ProductCard
                                            key={product.id}
                                            // Spread product props, mapping API fields to Card props if needed
                                            id={product.id}
                                            name={product.name}
                                            price={product.price}
                                            // Handle image array (take first 1) from API
                                            image={product.images && product.images.length > 0 ? product.images[0] : 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=500&q=60'}
                                            category={product.category_name || 'Chung'}
                                            rating={4.5} // Dummy rating for now
                                            reviews={0}
                                            unit="đ"
                                        />
                                    ))}
                                </div>
                            ) : (
                                <div className="text-center py-20 bg-white rounded-xl shadow-sm">
                                    <p className="text-gray-500 text-lg">Không tìm thấy sản phẩm nào phù hợp.</p>
                                    <button
                                        onClick={() => { setSelectedCategoryId(null); setPriceRange(1000000); }}
                                        className="mt-4 text-brand-600 font-bold hover:underline"
                                    >
                                        Xóa bộ lọc
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* Mobile Sidebar Modal */}
            {isMobileFilterOpen && (
                <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/50 backdrop-blur-sm sm:p-4">
                    <div className="bg-white w-full sm:max-w-md h-[80vh] sm:h-auto rounded-t-2xl sm:rounded-2xl flex flex-col overflow-hidden">
                        <div className="p-4 border-b flex items-center justify-between">
                            <h2 className="text-lg font-bold">Filters</h2>
                            <button onClick={() => setIsMobileFilterOpen(false)} className="text-gray-500">Close</button>
                        </div>
                        <div className="p-6 overflow-y-auto">
                            <FilterContent />
                        </div>
                        <div className="p-4 border-t bg-gray-50">
                            <button
                                onClick={() => setIsMobileFilterOpen(false)}
                                className="w-full bg-brand-600 text-white font-bold py-3 rounded-xl"
                            >
                                Show Results
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </Layout>
    );
}
