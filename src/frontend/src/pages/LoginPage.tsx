import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Layout } from '../components/layout/Layout';
import { useAuth } from '../context/AuthContext';
import { client } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setIsLoading(true);

        try {
            // 1. Login to get token
            const payload = { email, password };
            console.log("🚀 SENDING LOGIN KEYLOAD:", payload); // DEBUG

            const response: any = await client.post(API_ENDPOINTS.AUTH.LOGIN, payload);
            console.log("✅ LOGIN SUCCESS RESPONSE:", response); // DEBUG

            const { tokens, user } = response;
            const { access_token } = tokens;

            // 2. Update Context directly (no need for separate /me call)
            // The response already contains the full user object
            login(access_token, user);

            // 5. Redirect
            navigate('/');
        } catch (err: any) {
            console.error(err);
            setError('Email hoặc mật khẩu không chính xác');
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
                <div className="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12 xl:p-24 bg-white">
                    <div className="w-full max-w-md space-y-8">
                        <div>
                            <h2 className="text-3xl font-extrabold text-gray-900 mb-2">
                                Đăng Nhập Tài Khoản
                            </h2>
                            <p className="text-sm text-gray-600">
                                Vui lòng đăng nhập để tiếp tục
                            </p>
                        </div>
                        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
                            {error && (
                                <div className="bg-red-50 text-red-500 p-3 rounded-lg text-sm text-center border border-red-100">
                                    {error}
                                </div>
                            )}
                            <div className="space-y-4">
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                                    <input
                                        type="email"
                                        required
                                        className="appearance-none block w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-shadow bg-gray-50 focus:bg-white"
                                        placeholder="Nhập email của bạn"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Mật khẩu</label>
                                    <input
                                        type="password"
                                        required
                                        className="appearance-none block w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-shadow bg-gray-50 focus:bg-white"
                                        placeholder="Nhập mật khẩu"
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                    />
                                </div>
                            </div>

                            <div>
                                <button
                                    type="submit"
                                    disabled={isLoading}
                                    className="group relative w-full flex justify-center py-3.5 px-4 border border-transparent text-sm font-bold rounded-xl text-white bg-brand-600 hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-brand-500 disabled:opacity-50 transition duration-200 shadow-lg shadow-brand-500/30"
                                >
                                    {isLoading ? 'Đang xử lý...' : 'Đăng Nhập'}
                                </button>
                            </div>

                            <div className="text-center text-sm pt-4 border-t border-gray-100 mt-6">
                                <span className="text-gray-600">Bạn chưa có tài khoản? </span>
                                <Link to="/register" className="font-bold text-brand-600 hover:text-brand-700 transition">
                                    Đăng ký ngay
                                </Link>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </Layout>
    );
}
