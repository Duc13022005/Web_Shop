
import { Facebook, Instagram, Twitter } from 'lucide-react';

export const Footer = () => {
    return (
        <footer className="bg-gray-900 text-white pt-12 pb-8">
            <div className="max-w-7xl mx-auto px-4">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                    <div>
                        <h3 className="text-xl font-bold text-brand-500 mb-4">7coMART</h3>
                        <p className="text-gray-400 text-sm leading-relaxed">
                            Thực phẩm tươi ngon, giao hàng siêu tốc. 7coMART mang đến chất lượng tốt nhất ngay trước cửa nhà bạn.
                        </p>
                    </div>

                    <div>
                        <h4 className="font-semibold mb-4 text-gray-200">Về Chúng Tôi</h4>
                        <ul className="space-y-2 text-gray-400 text-sm">
                            <li><a href="#" className="hover:text-brand-400 transition">Câu Chuyện</a></li>
                            <li><a href="#" className="hover:text-brand-400 transition">Tuyển Dụng</a></li>
                            <li><a href="#" className="hover:text-brand-400 transition">Blog</a></li>
                            <li><a href="#" className="hover:text-brand-400 transition">Điều Khoản</a></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-semibold mb-4 text-gray-200">Danh Mục</h4>
                        <ul className="space-y-2 text-gray-400 text-sm">
                            <li><a href="#" className="hover:text-brand-400 transition">Rau Củ Quả</a></li>
                            <li><a href="#" className="hover:text-brand-400 transition">Trứng & Sữa</a></li>
                            <li><a href="#" className="hover:text-brand-400 transition">Thịt & Hải Sản</a></li>
                            <li><a href="#" className="hover:text-brand-400 transition">Bánh Mì</a></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-semibold mb-4 text-gray-200">Kết Nối</h4>
                        <div className="flex space-x-4 mb-4">
                            <a href="#" className="text-gray-400 hover:text-brand-500 transition"><Facebook size={20} /></a>
                            <a href="#" className="text-gray-400 hover:text-brand-500 transition"><Instagram size={20} /></a>
                            <a href="#" className="text-gray-400 hover:text-brand-500 transition"><Twitter size={20} /></a>
                        </div>
                        <p className="text-gray-400 text-sm mb-2">Đăng ký nhận tin</p>
                        <div className="flex">
                            <input
                                type="email"
                                placeholder="Email của bạn"
                                className="bg-gray-800 text-white px-4 py-2 rounded-l-md w-full focus:outline-none focus:ring-1 focus:ring-brand-500 text-sm border-none"
                            />
                            <button className="bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 rounded-r-md transition text-sm font-medium">
                                Đăng ký
                            </button>
                        </div>
                    </div>
                </div>

                <div className="border-t border-gray-800 pt-8 text-center text-gray-500 text-sm">
                    © {new Date().getFullYear()} 7coMART. All rights reserved.
                </div>
            </div>
        </footer>
    );
};
