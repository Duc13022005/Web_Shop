import React, { useState } from 'react';
import { User, MapPin, CreditCard, Lock, Bell, ChevronRight, LogOut } from 'lucide-react';
import { Layout } from '../components/layout/Layout';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { client } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';

type TabType = 'personal' | 'address' | 'payment' | 'security' | 'notifications';

export default function UserProfilePage() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState<TabType>('personal');

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const renderTabContent = () => {
        switch (activeTab) {
            case 'personal':
                return <PersonalInfoTab user={user} />;
            case 'address':
                return <AddressTab />;
            case 'payment':
                return <PaymentTab />;
            case 'security':
                return <SecurityTab />;
            case 'notifications':
                return <NotificationTab />;
            default:
                return <PersonalInfoTab user={user} />;
        }
    };

    // If not authenticated (will be handled by protected route usually, but for safety)
    if (!user) {
        return (
            <Layout>
                <div className="min-h-screen flex items-center justify-center">
                    <p className="text-gray-500">Vui lòng đăng nhập để xem thông tin.</p>
                </div>
            </Layout>
        );
    }

    return (
        <Layout>
            <div className="bg-gray-50 min-h-[calc(100vh-64px)] py-8">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex flex-col md:flex-row gap-8">
                        {/* Sidebar */}
                        <div className="w-full md:w-80 shrink-0">
                            {/* User Summary Card */}
                            <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center gap-4 mb-6">
                                <div className="w-16 h-16 rounded-full bg-brand-100 border-2 border-brand-200 flex items-center justify-center text-brand-600 overflow-hidden shrink-0">
                                    {user.avatar ? (
                                        <img src={user.avatar} alt="avatar" className="w-full h-full object-cover" />
                                    ) : (
                                        <User size={32} />
                                    )}
                                </div>
                                <div>
                                    <h3 className="font-bold text-gray-900 text-lg">
                                        {user.full_name || user.email.split('@')[0]}
                                    </h3>
                                    <p className="text-sm text-gray-500 truncate">{user.email}</p>
                                </div>
                            </div>

                            {/* Menu Navigation */}
                            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                                <div className="p-4 bg-gray-50/50 border-b border-gray-100">
                                    <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider">Tài Khoản</h4>
                                </div>
                                <div className="p-2 space-y-1">
                                    <MenuButton 
                                        icon={User} 
                                        label="Thông tin cá nhân" 
                                        isActive={activeTab === 'personal'} 
                                        onClick={() => setActiveTab('personal')} 
                                    />
                                    <MenuButton 
                                        icon={MapPin} 
                                        label="Địa chỉ giao hàng" 
                                        isActive={activeTab === 'address'} 
                                        onClick={() => setActiveTab('address')} 
                                    />
                                </div>

                                <div className="p-4 bg-gray-50/50 border-y border-gray-100 mt-2">
                                    <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider">Thanh Toán & Cài Đặt</h4>
                                </div>
                                <div className="p-2 space-y-1">
                                    <MenuButton 
                                        icon={CreditCard} 
                                        label="Phương thức thanh toán" 
                                        isActive={activeTab === 'payment'} 
                                        onClick={() => setActiveTab('payment')} 
                                    />
                                    <MenuButton 
                                        icon={Lock} 
                                        label="Thay đổi mật khẩu" 
                                        isActive={activeTab === 'security'} 
                                        onClick={() => setActiveTab('security')} 
                                    />
                                    <MenuButton 
                                        icon={Bell} 
                                        label="Cài đặt thông báo" 
                                        isActive={activeTab === 'notifications'} 
                                        onClick={() => setActiveTab('notifications')} 
                                    />
                                </div>
                                
                                <div className="p-2 border-t border-gray-100 mt-2">
                                    <button 
                                        onClick={handleLogout}
                                        className="w-full flex items-center gap-3 px-4 py-3 text-sm font-medium text-red-600 rounded-xl hover:bg-red-50 transition"
                                    >
                                        <LogOut size={18} />
                                        Đăng xuất
                                    </button>
                                </div>
                            </div>
                        </div>

                        {/* Main Content Area */}
                        <div className="flex-1">
                            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8 min-h-[600px]">
                                {renderTabContent()}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
}

// ---- Sub Components ----

function MenuButton({ icon: Icon, label, isActive, onClick }: any) {
    return (
        <button
            onClick={onClick}
            className={`w-full flex items-center justify-between px-4 py-3 text-sm font-medium rounded-xl transition ${
                isActive 
                    ? 'bg-brand-50 text-brand-700' 
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            }`}
        >
            <div className="flex items-center gap-3">
                <Icon size={18} className={isActive ? 'text-brand-600' : 'text-gray-400'} />
                {label}
            </div>
            {isActive && <ChevronRight size={16} className="text-brand-600" />}
        </button>
    );
}

function PersonalInfoTab({ user }: any) {
    const [isEditing, setIsEditing] = useState(false);
    
    // Derived defaults or actual data
    const firstName = user?.full_name ? user.full_name.split(' ').slice(0, -1).join(' ') : '';
    const lastName = user?.full_name ? user.full_name.split(' ').slice(-1).join(' ') : '';

    return (
        <div className="animate-fade-in">
            <div className="flex items-center justify-between mb-8">
                <h2 className="text-2xl font-bold text-gray-900">Thông tin cá nhân</h2>
                <button 
                    onClick={() => setIsEditing(!isEditing)}
                    className="flex items-center gap-2 text-sm font-bold text-brand-600 hover:text-brand-700 bg-brand-50 hover:bg-brand-100 px-4 py-2 rounded-full transition"
                >
                    {isEditing ? 'Hủy' : 'Chỉnh sửa'}
                </button>
            </div>

            <form className="max-w-2xl space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Họ</label>
                        <input
                            type="text"
                            defaultValue={firstName || 'Người dùng'}
                            disabled={!isEditing}
                            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-brand-500 focus:outline-none disabled:bg-gray-50 disabled:text-gray-500 transition"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">Tên</label>
                        <input
                            type="text"
                            defaultValue={lastName || ''}
                            disabled={!isEditing}
                            className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-brand-500 focus:outline-none disabled:bg-gray-50 disabled:text-gray-500 transition"
                        />
                    </div>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                    <input
                        type="email"
                        defaultValue={user?.email || ''}
                        disabled={true} // Email usually requires special flow to change
                        className="w-full px-4 py-3 rounded-xl border border-gray-200 bg-gray-50 text-gray-500 focus:outline-none"
                    />
                    <p className="mt-1 text-xs text-gray-500">Email không thể thay đổi trực tiếp.</p>
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Số điện thoại</label>
                    <input
                        type="tel"
                        defaultValue={user?.phone || ''}
                        disabled={!isEditing}
                        className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-brand-500 focus:outline-none disabled:bg-gray-50 disabled:text-gray-500 transition"
                    />
                </div>

                {isEditing && (
                    <div className="pt-4 flex justify-end">
                        <button
                            type="button"
                            onClick={() => setIsEditing(false)}
                            className="bg-brand-600 hover:bg-brand-700 text-white font-bold py-3 px-8 rounded-xl transition shadow-lg shadow-brand-500/30"
                        >
                            Lưu Thông Tin
                        </button>
                    </div>
                )}
            </form>
        </div>
    );
}

function SecurityTab() {
    const { logout } = useAuth();
    const navigate = useNavigate();
    const [currentPassword, setCurrentPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [successMsg, setSuccessMsg] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccessMsg('');

        if (newPassword !== confirmPassword) {
            setError('Mật khẩu mới không khớp!');
            return;
        }

        if (newPassword.length < 6) {
            setError('Mật khẩu mới phải dài ít nhất 6 ký tự.');
            return;
        }

        setIsLoading(true);
        try {
            await client.put(API_ENDPOINTS.AUTH.CHANGE_PASSWORD, {
                current_password: currentPassword,
                new_password: newPassword,
            });
            
            setSuccessMsg('Đổi mật khẩu thành công! Vui lòng đăng nhập lại.');
            setTimeout(() => {
                logout();
                navigate('/login');
            }, 2500);

        } catch (err: any) {
            console.error(err);
            if (err.response?.status === 400 || err.response?.data?.detail) {
                setError(err.response?.data?.detail || 'Mật khẩu hiện tại không chính xác.');
            } else {
                setError('Có lỗi xảy ra. Vui lòng thử lại sau.');
            }
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="animate-fade-in">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Thay đổi mật khẩu</h2>
            <p className="text-gray-500 mb-8">Nhập mật khẩu hiện tại và mật khẩu mới để thay đổi.</p>

            <form className="max-w-2xl space-y-6" onSubmit={handleSubmit}>
                {error && (
                    <div className="bg-red-50 text-red-600 p-4 rounded-xl text-sm border border-red-100 font-medium">
                        {error}
                    </div>
                )}
                {successMsg && (
                    <div className="bg-green-50 text-green-700 p-4 rounded-xl text-sm border border-green-200 font-medium">
                        {successMsg}
                    </div>
                )}

                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Mật khẩu hiện tại</label>
                    <input
                        type="password"
                        required
                        placeholder="Nhập mật khẩu hiện tại"
                        value={currentPassword}
                        onChange={(e) => setCurrentPassword(e.target.value)}
                        className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-brand-500 focus:outline-none transition"
                    />
                </div>
                
                <div className="pt-4 border-t border-gray-100">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Mật khẩu mới</label>
                    <input
                        type="password"
                        required
                        placeholder="Nhập mật khẩu mới"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-brand-500 focus:outline-none transition"
                    />
                </div>

                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Nhập lại mật khẩu mới</label>
                    <input
                        type="password"
                        required
                        placeholder="Xác nhận mật khẩu mới"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-brand-500 focus:outline-none transition"
                    />
                </div>

                <div className="pt-4">
                    <button
                        type="submit"
                        disabled={isLoading}
                        className="bg-brand-600 hover:bg-brand-700 text-white font-bold py-3 px-8 rounded-xl transition shadow-lg shadow-brand-500/30 disabled:opacity-50"
                    >
                        {isLoading ? 'Đang lưu...' : 'Lưu Mật Khẩu'}
                    </button>
                </div>
            </form>
        </div>
    );
}

function AddressTab() {
    return (
        <div className="animate-fade-in">
            <div className="flex items-center justify-between mb-8">
                <h2 className="text-2xl font-bold text-gray-900">Địa chỉ giao hàng</h2>
                <button className="text-sm font-bold text-brand-600 hover:text-brand-700 bg-brand-50 hover:bg-brand-100 px-4 py-2 rounded-full transition">
                    + Thêm địa chỉ mới
                </button>
            </div>

            <div className="space-y-4">
                {/* Default Address */}
                <div className="border border-brand-200 bg-brand-50/30 rounded-2xl p-6 relative overflow-hidden">
                    <div className="absolute top-0 right-0 bg-brand-500 text-white text-xs font-bold px-3 py-1 rounded-bl-lg">
                        Mặc định
                    </div>
                    <div className="flex items-start gap-4">
                        <div className="w-10 h-10 rounded-full bg-brand-100 text-brand-600 flex items-center justify-center shrink-0">
                            <MapPin size={20} />
                        </div>
                        <div>
                            <div className="flex items-center gap-2 mb-1">
                                <h4 className="font-bold text-gray-900">Nhà riêng</h4>
                                <span className="text-gray-400">|</span>
                                <span className="font-medium text-gray-900">Nguyễn Văn A</span>
                                <span className="text-gray-400">|</span>
                                <span className="text-gray-600">0901234567</span>
                            </div>
                            <p className="text-gray-600 text-sm mb-3">
                                123 Đường Điện Biên Phủ, Phường 15, Quận Bình Thạnh, TP. Hồ Chí Minh
                            </p>
                            <div className="flex gap-4 text-sm font-medium">
                                <button className="text-brand-600 hover:underline">Sửa</button>
                                <button className="text-gray-400 hover:text-gray-700 hover:underline">Xóa</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

function PaymentTab() {
    return (
        <div className="animate-fade-in">
            <div className="flex items-center justify-between mb-8">
                <div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-2">Phương thức thanh toán</h2>
                    <p className="text-gray-500 text-sm">Quản lý các thẻ và liên kết ngân hàng của bạn</p>
                </div>
                <button className="text-sm font-bold text-brand-600 hover:text-brand-700 bg-brand-50 hover:bg-brand-100 px-4 py-2 rounded-full transition">
                    + Liên kết ngân hàng
                </button>
            </div>

            <div className="max-w-md">
                <div className="border border-gray-200 rounded-2xl p-6 relative bg-gradient-to-br from-gray-900 to-gray-800 text-white shadow-xl mb-6">
                    <div className="absolute top-4 right-6 font-bold italic text-xl">VISA</div>
                    <div className="mb-8 mt-2">
                        <div className="w-10 h-8 bg-yellow-400/80 rounded mb-2"></div>
                    </div>
                    <div className="font-mono text-xl tracking-widest mb-2">
                        **** **** **** 1234
                    </div>
                    <div className="flex justify-between items-center text-sm text-gray-300">
                        <span>NGUYEN VAN A</span>
                        <span>12/28</span>
                    </div>
                </div>
                <div className="flex justify-end">
                    <button className="text-red-500 text-sm font-medium hover:underline">
                        Hủy liên kết thẻ này
                    </button>
                </div>
            </div>
        </div>
    );
}

function NotificationTab() {
    return (
        <div className="animate-fade-in">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Cài đặt thông báo</h2>
            
            <div className="space-y-6 max-w-2xl">
                <div className="flex items-center justify-between p-4 border border-gray-100 rounded-xl bg-gray-50/50">
                    <div>
                        <h4 className="font-bold text-gray-900">Cập nhật đơn hàng</h4>
                        <p className="text-sm text-gray-500">Nhận thông báo khi đơn hàng được xác nhận, đang giao, và hoàn thành</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" className="sr-only peer" defaultChecked />
                        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-brand-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-brand-600"></div>
                    </label>
                </div>

                <div className="flex items-center justify-between p-4 border border-gray-100 rounded-xl bg-gray-50/50">
                    <div>
                        <h4 className="font-bold text-gray-900">Khuyến mãi & Deal Hot</h4>
                        <p className="text-sm text-gray-500">Cập nhật các chương trình giảm giá và ưu đãi độc quyền dành cho bạn</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                        <input type="checkbox" className="sr-only peer" defaultChecked />
                        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-brand-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-brand-600"></div>
                    </label>
                </div>
            </div>
        </div>
    );
}
