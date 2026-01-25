import { useState } from 'react';
import { Menu, Search, ShoppingCart, Heart, User, X } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const Header = () => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const { user, isAuthenticated, logout } = useAuth();

    return (
        <header className="bg-white shadow-sm sticky top-0 z-50">
            {/* Top Bar */}
            <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-4">

                {/* Mobile Menu Button + Logo */}
                <div className="flex items-center gap-2 md:gap-8">
                    <button
                        className="md:hidden p-2 hover:bg-gray-100 rounded-md"
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                    >
                        {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
                    </button>

                    <Link to="/" className="text-2xl font-bold text-brand-600 tracking-tight shrink-0">
                        7co<span className="text-gray-900">MART</span>
                    </Link>

                    {/* Desktop Nav Links */}
                    <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-600">
                        <Link to="/" className="hover:text-brand-600 transition">Trang Chủ</Link>
                        <Link to="/products" className="hover:text-brand-600 transition">Sản Phẩm</Link>
                        <Link to="/about" className="hover:text-brand-600 transition">Giới Thiệu</Link>
                        <Link to="/contact" className="hover:text-brand-600 transition">Liên Hệ</Link>
                    </nav>
                </div>

                {/* Search Bar (Desktop) */}
                <div className="hidden md:flex flex-1 max-w-xl mx-auto relative">
                    <input
                        type="text"
                        placeholder="Tìm kiếm rau củ, thịt, cá..."
                        className="w-full pl-4 pr-10 py-2.5 rounded-full border border-gray-200 bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-brand-500 transition shadow-sm"
                    />
                    <button className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-brand-600">
                        <Search size={20} />
                    </button>
                </div>

                {/* User Actions */}
                <div className="flex items-center gap-2 md:gap-4">
                    {isAuthenticated ? (
                        <div className="hidden md:flex items-center gap-2 hover:bg-gray-50 px-3 py-2 rounded-full transition text-sm font-medium text-gray-700 cursor-pointer group relative">
                            <User size={20} />
                            <span className="hidden lg:block">{user?.full_name || user?.email}</span>

                            {/* Dropdown for Logout */}
                            <div className="absolute top-full right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 border border-gray-100 hidden group-hover:block">
                                <button
                                    onClick={logout}
                                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                                >
                                    Đăng xuất
                                </button>
                            </div>
                        </div>
                    ) : (
                        <Link to="/login" className="hidden md:flex items-center gap-2 hover:bg-gray-50 px-3 py-2 rounded-full transition text-sm font-medium text-gray-700">
                            <User size={20} />
                            <span className="hidden lg:block">Đăng Nhập</span>
                        </Link>
                    )}

                    <button className="p-2 hover:bg-gray-100 rounded-full relative text-gray-600 hover:text-brand-600 transition">
                        <Heart size={22} />
                    </button>

                    <button className="p-2 hover:bg-gray-100 rounded-full relative text-gray-600 hover:text-brand-600 transition flex items-center gap-2">
                        <div className="relative">
                            <ShoppingCart size={22} />
                            <span className="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center">
                                0
                            </span>
                        </div>
                        <span className="hidden lg:block font-medium text-sm">0đ</span>
                    </button>
                </div>
            </div>

            {/* Mobile Search & Menu (Collapsible) */}
            <div className={`md:hidden border-t border-gray-100 overflow-hidden transition-all duration-300 ${isMenuOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'}`}>
                <div className="p-4 space-y-4">
                    {/* Mobile Search */}
                    <div className="relative">
                        <input
                            type="text"
                            placeholder="Tìm kiếm..."
                            className="w-full pl-4 pr-10 py-2 rounded-lg border border-gray-200 bg-gray-50 focus:outline-none focus:ring-2 focus:ring-brand-500"
                        />
                        <button className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                            <Search size={18} />
                        </button>
                    </div>

                    {/* Mobile Nav Links */}
                    <nav className="flex flex-col space-y-3 font-medium text-gray-700">
                        <Link to="/" className="flex items-center gap-2 py-2 border-b border-gray-50" onClick={() => setIsMenuOpen(false)}>
                            Trang Chủ
                        </Link>
                        <Link to="/products" className="flex items-center gap-2 py-2 border-b border-gray-50" onClick={() => setIsMenuOpen(false)}>
                            Sản Phẩm
                        </Link>
                        <Link to="/about" className="flex items-center gap-2 py-2 border-b border-gray-50" onClick={() => setIsMenuOpen(false)}>
                            Giới Thiệu
                        </Link>
                        <div className="pt-2">
                            <div className="pt-2">
                                {isAuthenticated ? (
                                    <button
                                        onClick={() => { logout(); setIsMenuOpen(false); }}
                                        className="w-full text-center bg-red-50 text-red-700 font-semibold py-2 rounded-lg"
                                    >
                                        Đăng Xuất ({user?.email})
                                    </button>
                                ) : (
                                    <Link to="/login"
                                        onClick={() => setIsMenuOpen(false)}
                                        className="block w-full text-center bg-brand-50 text-brand-700 font-semibold py-2 rounded-lg"
                                    >
                                        Đăng Nhập / Đăng Ký
                                    </Link>
                                )}
                            </div>
                        </div>
                    </nav>
                </div>
            </div>

            {/* Category Navigation (Secondary Row - Desktop Only) */}
            <div className="hidden md:block border-t border-gray-100 py-3 bg-gray-50/50">
                <div className="max-w-7xl mx-auto px-4 flex gap-8 overflow-x-auto text-sm font-medium text-gray-600 scrollbar-hide">
                    {['Tất cả', 'Rau củ', 'Thịt & Cá', 'Trứng & Sữa', 'Bánh kẹo', 'Đồ uống', 'Đồ đông lạnh', 'Ăn vặt', 'Chăm sóc cá nhân'].map((cat) => (
                        <Link
                            key={cat}
                            to={`/products?category=${cat}`}
                            className="whitespace-nowrap hover:text-brand-600 transition relative group"
                        >
                            {cat}
                            <span className="absolute -bottom-3 left-0 w-0 h-0.5 bg-brand-500 transition-all duration-300 group-hover:w-full"></span>
                        </Link>
                    ))}
                </div>
            </div>
        </header>
    );
};
