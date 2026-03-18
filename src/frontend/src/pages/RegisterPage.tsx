import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Layout } from '../components/layout/Layout';
import { client } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';

export default function RegisterPage() {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: '',
    });
    const [agreed, setAgreed] = useState(false);
    const [error, setError] = useState('');
    const [successMsg, setSuccessMsg] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const navigate = useNavigate();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccessMsg('');

        if (!agreed) {
            setError('Bạn phải đồng ý với Điều khoản và Điều kiện để tiếp tục.');
            return;
        }

        if (formData.password !== formData.confirmPassword) {
            setError('Mật khẩu không khớp!');
            return;
        }

        if (formData.password.length < 6) {
            setError('Mật khẩu phải chứa ít nhất 6 ký tự.');
            return;
        }

        setIsLoading(true);

        try {
            const payload = {
                email: formData.email,
                password: formData.password,
                full_name: `${formData.firstName} ${formData.lastName}`.trim(),
                phone: formData.phone || undefined,
            };

            await client.post(API_ENDPOINTS.AUTH.REGISTER, payload);
            
            setSuccessMsg('Đăng ký thành công! Đang chuyển hướng đến trang đăng nhập...');
            setTimeout(() => {
                navigate('/login');
            }, 2000);

        } catch (err: any) {
            console.error('Registration failed:', err);
            // Check if error is email exists
            if (err.response?.status === 409 || err.response?.data?.detail?.includes('Email already')) {
                setError('Email này đã được sử dụng. Vui lòng chọn email khác.');
            } else {
                setError('Có lỗi xảy ra trong quá trình đăng ký. Vui lòng thử lại sau.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Layout>
            <div className="min-h-[calc(100vh-64px)] flex bg-white">
                {/* Left Side - Image Background */}
                <div className="hidden lg:flex lg:w-1/2 relative bg-gray-900">
                    <img 
                        src="https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=1000&auto=format&fit=crop" 
                        alt="Groceries" 
                        className="absolute inset-0 w-full h-full object-cover opacity-80"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
                    <div className="relative z-10 flex flex-col justify-end p-12 text-white h-full">
                        <h1 className="text-4xl xl:text-5xl font-extrabold mb-4 leading-tight">
                            Chào mừng đến với <br />7coMART
                        </h1>
                        <p className="text-lg opacity-90 max-w-md">
                            Tìm kiếm nhu cầu thực phẩm hằng ngày của bạn với giá rẻ, đầy đủ, tiện lợi và giao hàng siêu tốc.
                        </p>
                    </div>
                </div>

                {/* Right Side - Form */}
                <div className="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12 xl:p-24 bg-white overflow-y-auto">
                    <div className="w-full max-w-lg space-y-8">
                        <div>
                            <h2 className="text-3xl font-extrabold text-gray-900 mb-2">
                                Đăng Ký Tài Khoản
                            </h2>
                            <p className="text-sm text-gray-600">
                                Hãy điền thông tin bên dưới để tạo tài khoản mới
                            </p>
                        </div>
                        
                        <form className="mt-8 space-y-5" onSubmit={handleSubmit}>
                            {error && (
                                <div className="bg-red-50 text-red-600 p-4 rounded-xl text-sm text-center border border-red-100 font-medium">
                                    {error}
                                </div>
                            )}
                            {successMsg && (
                                <div className="bg-green-50 text-green-700 p-4 rounded-xl text-sm text-center border border-green-200 font-medium">
                                    {successMsg}
                                </div>
                            )}

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Họ</label>
                                    <input
                                        type="text"
                                        name="firstName"
                                        required
                                        className="appearance-none block w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-shadow bg-gray-50 focus:bg-white text-sm"
                                        placeholder="VD: Nguyễn"
                                        value={formData.firstName}
                                        onChange={handleChange}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Tên</label>
                                    <input
                                        type="text"
                                        name="lastName"
                                        required
                                        className="appearance-none block w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-shadow bg-gray-50 focus:bg-white text-sm"
                                        placeholder="VD: Văn A"
                                        value={formData.lastName}
                                        onChange={handleChange}
                                    />
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                                <input
                                    type="email"
                                    name="email"
                                    required
                                    className="appearance-none block w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-shadow bg-gray-50 focus:bg-white text-sm"
                                    placeholder="Nhập email của bạn"
                                    value={formData.email}
                                    onChange={handleChange}
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Số điện thoại</label>
                                <input
                                    type="tel"
                                    name="phone"
                                    required
                                    className="appearance-none block w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-shadow bg-gray-50 focus:bg-white text-sm"
                                    placeholder="Nhập số điện thoại"
                                    value={formData.phone}
                                    onChange={handleChange}
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Mật khẩu</label>
                                <input
                                    type="password"
                                    name="password"
                                    required
                                    className="appearance-none block w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-shadow bg-gray-50 focus:bg-white text-sm"
                                    placeholder="Nhập mật khẩu (Tối thiểu 6 ký tự)"
                                    value={formData.password}
                                    onChange={handleChange}
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1">Nhập lại mật khẩu</label>
                                <input
                                    type="password"
                                    name="confirmPassword"
                                    required
                                    className="appearance-none block w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-shadow bg-gray-50 focus:bg-white text-sm"
                                    placeholder="Xác nhận lại mật khẩu"
                                    value={formData.confirmPassword}
                                    onChange={handleChange}
                                />
                            </div>

                            <div className="flex items-center mt-4">
                                <input
                                    id="terms"
                                    name="terms"
                                    type="checkbox"
                                    className="h-4 w-4 text-brand-600 focus:ring-brand-500 border-gray-300 rounded cursor-pointer"
                                    checked={agreed}
                                    onChange={(e) => setAgreed(e.target.checked)}
                                />
                                <label htmlFor="terms" className="ml-2 block text-sm text-gray-700 cursor-pointer">
                                    Tôi đồng ý với các <span className="text-brand-600 font-medium hover:underline">Điều khoản và Chính sách</span> của 7coMART
                                </label>
                            </div>

                            <div className="pt-2">
                                <button
                                    type="submit"
                                    disabled={isLoading}
                                    className="group relative w-full flex justify-center py-3.5 px-4 border border-transparent text-sm font-bold rounded-xl text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 disabled:opacity-50 transition duration-200 shadow-lg shadow-brand-500/30"
                                >
                                    {isLoading ? 'Đang đăng ký...' : 'Đăng Ký'}
                                </button>
                            </div>

                            <div className="text-center text-sm pt-4 border-t border-gray-100 mt-6">
                                <span className="text-gray-600">Đã có tài khoản? </span>
                                <Link to="/login" className="font-bold text-brand-600 hover:text-brand-700 transition">
                                    Đăng nhập
                                </Link>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </Layout>
    );
}
