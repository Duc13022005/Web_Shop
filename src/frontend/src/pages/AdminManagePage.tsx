import React, { useState, useEffect, useCallback } from 'react';
import { Layout } from '../components/layout/Layout';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { LayoutDashboard, Users, PackageSearch, PackagePlus, Edit, Trash2, X, Check } from 'lucide-react';
import {
    PieChart, Pie, Cell, ResponsiveContainer, Tooltip,
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend
} from 'recharts';
import { client } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';
import { toast } from 'react-hot-toast';

const PIE_COLORS = ['#0ea5e9', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'];
const ROLES = ['Thu ngân', 'Vệ sinh', 'Shipper'];

const formatPrice = (price: number) =>
    new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price || 0);

// ─── Small Components ─────────────────────────────────────────────────────────

const StatCard = ({ label, value, sub }: { label: string; value: string | number; sub?: string }) => (
    <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
        <div className="text-gray-500 text-sm font-medium mb-1">{label}</div>
        <div className="text-3xl font-bold text-gray-900">{value}</div>
        {sub && <div className="text-xs text-gray-400 mt-1">{sub}</div>}
    </div>
);

const RoleBadge = ({ role }: { role: string }) => {
    const color = role === 'Thu ngân' ? 'bg-blue-100 text-blue-700'
        : role === 'Shipper' ? 'bg-orange-100 text-orange-700'
        : 'bg-green-100 text-green-700';
    return <span className={`px-3 py-1 rounded-full text-xs font-bold ${color}`}>{role}</span>;
};

// ─── Modals ───────────────────────────────────────────────────────────────────

interface EmpForm { id?: number; full_name: string; email: string; phone: string; role: string; salary: number; }
interface ProdForm { id?: number; sku: string; name: string; base_price: number; sale_price: number; unit: string; is_active: boolean; }

const BLANK_EMP: EmpForm = { full_name: '', email: '', phone: '', role: 'Thu ngân', salary: 0 };
const BLANK_PROD: ProdForm = { sku: '', name: '', base_price: 0, sale_price: 0, unit: 'cái', is_active: true };

function EmpModal({ form, onChange, onSave, onClose }: {
    form: EmpForm; onChange: (f: EmpForm) => void; onSave: () => void; onClose: () => void;
}) {
    return (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
            <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-8">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-bold">{form.id ? 'Sửa nhân viên' : 'Thêm nhân viên'}</h2>
                    <button onClick={onClose}><X size={20} /></button>
                </div>
                <div className="grid grid-cols-2 gap-4">
                    <div className="col-span-2">
                        <label className="block text-sm font-medium mb-1">Họ và tên *</label>
                        <input required value={form.full_name} onChange={e => onChange({ ...form, full_name: e.target.value })} className="w-full border px-3 py-2 rounded-lg" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Email *</label>
                        <input required type="email" value={form.email} onChange={e => onChange({ ...form, email: e.target.value })} className="w-full border px-3 py-2 rounded-lg" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">SĐT</label>
                        <input value={form.phone} onChange={e => onChange({ ...form, phone: e.target.value })} className="w-full border px-3 py-2 rounded-lg" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Chức vụ</label>
                        <select value={form.role} onChange={e => onChange({ ...form, role: e.target.value })} className="w-full border px-3 py-2 rounded-lg">
                            {ROLES.map(r => <option key={r}>{r}</option>)}
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Lương (VNĐ)</label>
                        <input type="number" value={form.salary} onChange={e => onChange({ ...form, salary: +e.target.value })} className="w-full border px-3 py-2 rounded-lg" />
                    </div>
                </div>
                <div className="mt-6 flex gap-3 justify-end">
                    <button onClick={onClose} className="px-5 py-2 rounded-lg bg-gray-100 text-gray-700 font-medium">Hủy</button>
                    <button onClick={onSave} className="px-5 py-2 rounded-lg bg-brand-600 text-white font-medium hover:bg-brand-700">Lưu</button>
                </div>
            </div>
        </div>
    );
}

function ProdModal({ form, onChange, onSave, onClose }: {
    form: ProdForm; onChange: (f: ProdForm) => void; onSave: () => void; onClose: () => void;
}) {
    return (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
            <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg p-8">
                <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-bold">{form.id ? 'Sửa sản phẩm' : 'Thêm sản phẩm'}</h2>
                    <button onClick={onClose}><X size={20} /></button>
                </div>
                <div className="grid grid-cols-2 gap-4">
                    <div className="col-span-2">
                        <label className="block text-sm font-medium mb-1">Tên sản phẩm *</label>
                        <input required value={form.name} onChange={e => onChange({ ...form, name: e.target.value })} className="w-full border px-3 py-2 rounded-lg" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Mã SKU</label>
                        <input value={form.sku} onChange={e => onChange({ ...form, sku: e.target.value })} placeholder="Tự động nếu để trống" className="w-full border px-3 py-2 rounded-lg" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Đơn vị</label>
                        <input value={form.unit} onChange={e => onChange({ ...form, unit: e.target.value })} className="w-full border px-3 py-2 rounded-lg" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Giá gốc *</label>
                        <input type="number" value={form.base_price} onChange={e => onChange({ ...form, base_price: +e.target.value })} className="w-full border px-3 py-2 rounded-lg" />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Giá bán</label>
                        <input type="number" value={form.sale_price} onChange={e => onChange({ ...form, sale_price: +e.target.value })} className="w-full border px-3 py-2 rounded-lg" />
                    </div>
                    <div className="col-span-2 flex items-center gap-2">
                        <input type="checkbox" id="is_active" checked={form.is_active} onChange={e => onChange({ ...form, is_active: e.target.checked })} className="h-4 w-4 rounded" />
                        <label htmlFor="is_active" className="text-sm font-medium">Đang kinh doanh</label>
                    </div>
                </div>
                <div className="mt-6 flex gap-3 justify-end">
                    <button onClick={onClose} className="px-5 py-2 rounded-lg bg-gray-100 text-gray-700 font-medium">Hủy</button>
                    <button onClick={onSave} className="px-5 py-2 rounded-lg bg-brand-600 text-white font-medium hover:bg-brand-700">Lưu</button>
                </div>
            </div>
        </div>
    );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function AdminManagePage() {
    const { user, isAuthenticated } = useAuth();
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState<'dashboard' | 'hr' | 'inventory'>('dashboard');

    // Data
    const [stats, setStats] = useState<any>(null);
    const [employees, setEmployees] = useState<any[]>([]);
    const [products, setProducts] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    // Modals
    const [empModal, setEmpModal] = useState<EmpForm | null>(null);
    const [prodModal, setProdModal] = useState<ProdForm | null>(null);

    useEffect(() => {
        if (!isAuthenticated || user?.role !== 'admin') navigate('/');
    }, [isAuthenticated, user, navigate]);

    const fetchStats = useCallback(async () => {
        setLoading(true);
        try {
            const res = await client.get(API_ENDPOINTS.ADMIN.DASHBOARD);
            setStats(res);
        } catch (err) {
            console.error('Dashboard fetch error:', err);
            toast.error('Không thể tải dashboard');
        }
        finally { setLoading(false); }
    }, []);

    const fetchEmployees = useCallback(async () => {
        setLoading(true);
        try {
            const res = await client.get(API_ENDPOINTS.ADMIN.EMPLOYEES);
            setEmployees(Array.isArray(res) ? res : []);
        } catch (err) {
            console.error('Employees fetch error:', err);
            toast.error('Không thể tải nhân sự');
        }
        finally { setLoading(false); }
    }, []);

    const fetchProducts = useCallback(async () => {
        setLoading(true);
        try {
            const res = await client.get(API_ENDPOINTS.ADMIN.PRODUCTS);
            setProducts(Array.isArray(res) ? res : []);
        } catch (err) {
            console.error('Products fetch error:', err);
            toast.error('Không thể tải kho hàng');
        }
        finally { setLoading(false); }
    }, []);

    useEffect(() => {
        if (activeTab === 'dashboard') fetchStats();
        else if (activeTab === 'hr') fetchEmployees();
        else if (activeTab === 'inventory') fetchProducts();
    }, [activeTab, fetchStats, fetchEmployees, fetchProducts]);

    // ── Employee actions ──────────────────────────────────────────────────────

    const saveEmployee = async () => {
        if (!empModal) return;
        if (!empModal.full_name || !empModal.email) { toast.error('Vui lòng điền đủ thông tin'); return; }
        try {
            if (empModal.id) {
                await client.put(`${API_ENDPOINTS.ADMIN.EMPLOYEES}/${empModal.id}`, empModal);
                toast.success('Cập nhật thành công!');
            } else {
                await client.post(API_ENDPOINTS.ADMIN.EMPLOYEES, empModal);
                toast.success('Thêm nhân viên thành công!');
            }
            setEmpModal(null);
            fetchEmployees();
        } catch { toast.error('Có lỗi xảy ra'); }
    };

    const deleteEmployee = async (id: number) => {
        if (!confirm('Xóa nhân viên này?')) return;
        try {
            await client.delete(`${API_ENDPOINTS.ADMIN.EMPLOYEES}/${id}`);
            toast.success('Đã xóa nhân viên');
            fetchEmployees();
        } catch { toast.error('Không thể xóa'); }
    };

    // ── Product actions ───────────────────────────────────────────────────────

    const saveProduct = async () => {
        if (!prodModal) return;
        if (!prodModal.name || !prodModal.base_price) { toast.error('Tên và giá gốc là bắt buộc'); return; }
        try {
            if (prodModal.id) {
                await client.put(`${API_ENDPOINTS.ADMIN.PRODUCTS}/${prodModal.id}`, prodModal);
                toast.success('Cập nhật sản phẩm thành công!');
            } else {
                await client.post(API_ENDPOINTS.ADMIN.PRODUCTS, prodModal);
                toast.success('Thêm sản phẩm thành công!');
            }
            setProdModal(null);
            fetchProducts();
        } catch { toast.error('Có lỗi xảy ra'); }
    };

    const deleteProduct = async (id: number) => {
        if (!confirm('Xóa sản phẩm này?')) return;
        try {
            await client.delete(`${API_ENDPOINTS.ADMIN.PRODUCTS}/${id}`);
            toast.success('Đã xóa sản phẩm');
            fetchProducts();
        } catch { toast.error('Không thể xóa'); }
    };

    const SidebarBtn = ({ tab, icon, label }: { tab: typeof activeTab; icon: React.ReactNode; label: string }) => (
        <button
            onClick={() => setActiveTab(tab)}
            className={`flex items-center gap-3 w-full px-4 py-3 rounded-xl transition font-medium text-sm ${activeTab === tab ? 'bg-brand-50 text-brand-600' : 'text-gray-600 hover:bg-gray-50'}`}
        >
            {icon}<span>{label}</span>
        </button>
    );

    return (
        <Layout>
            {empModal && <EmpModal form={empModal} onChange={setEmpModal} onSave={saveEmployee} onClose={() => setEmpModal(null)} />}
            {prodModal && <ProdModal form={prodModal} onChange={setProdModal} onSave={saveProduct} onClose={() => setProdModal(null)} />}

            <div className="max-w-7xl mx-auto px-4 py-8 flex gap-6 min-h-[calc(100vh-64px)]">
                {/* Sidebar */}
                <div className="w-56 shrink-0 bg-white rounded-2xl shadow-sm border border-gray-100 p-4 h-fit sticky top-24">
                    <h2 className="text-lg font-bold text-gray-900 mb-5 px-2">Admin Panel</h2>
                    <nav className="flex flex-col gap-1">
                        <SidebarBtn tab="dashboard" icon={<LayoutDashboard size={18} />} label="Dashboard" />
                        <SidebarBtn tab="hr" icon={<Users size={18} />} label="Nhân sự" />
                        <SidebarBtn tab="inventory" icon={<PackageSearch size={18} />} label="Kho Hàng" />
                    </nav>
                </div>

                {/* Content */}
                <div className="flex-1 min-w-0">
                    {loading && (
                        <div className="flex items-center justify-center h-64 text-gray-400">
                            <div className="text-center"><div className="w-8 h-8 border-4 border-brand-200 border-t-brand-600 rounded-full animate-spin mx-auto mb-3"></div>Đang tải...</div>
                        </div>
                    )}

                    {/* ── Dashboard ── */}
                    {!loading && activeTab === 'dashboard' && (
                        <div className="space-y-6">
                            <h1 className="text-2xl font-bold text-gray-900">Tổng quan hệ thống</h1>

                            {stats ? (
                                <>
                                    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                                        <StatCard label="Tổng sản phẩm" value={stats.total_products} />
                                        <StatCard label="Người dùng" value={stats.total_users} />
                                        <StatCard label="Đơn hàng" value={stats.total_orders} />
                                        <StatCard label="Doanh thu" value={formatPrice(stats.total_revenue)} sub="Tổng tất cả đơn" />
                                    </div>

                                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                        {/* Pie chart */}
                                        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                                            <h3 className="font-semibold text-gray-800 mb-4">Tỉ trọng danh mục</h3>
                                            {stats.category_distribution?.length > 0 ? (
                                                <ResponsiveContainer width="100%" height={280}>
                                                    <PieChart>
                                                        <Pie data={stats.category_distribution} cx="50%" cy="50%" innerRadius={55} outerRadius={90} paddingAngle={4} dataKey="value">
                                                            {stats.category_distribution.map((_: any, i: number) => (
                                                                <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
                                                            ))}
                                                        </Pie>
                                                        <Tooltip formatter={(v: any) => [`${v} SP`, '']} />
                                                        <Legend />
                                                    </PieChart>
                                                </ResponsiveContainer>
                                            ) : <p className="text-gray-400 text-sm text-center py-12">Chưa có dữ liệu danh mục</p>}
                                        </div>

                                        {/* Bar chart monthly */}
                                        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm">
                                            <h3 className="font-semibold text-gray-800 mb-4">Đơn hàng theo tháng ({new Date().getFullYear()})</h3>
                                            {stats.monthly_data?.length > 0 ? (
                                                <ResponsiveContainer width="100%" height={280}>
                                                    <BarChart data={stats.monthly_data}>
                                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#F3F4F6" />
                                                        <XAxis dataKey="name" axisLine={false} tickLine={false} />
                                                        <YAxis axisLine={false} tickLine={false} />
                                                        <Tooltip />
                                                        <Bar dataKey="orders" name="Đơn hàng" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
                                                    </BarChart>
                                                </ResponsiveContainer>
                                            ) : <p className="text-gray-400 text-sm text-center py-12">Chưa có đơn hàng trong năm nay</p>}
                                        </div>
                                    </div>
                                </>
                            ) : (
                                <div className="bg-white rounded-2xl border p-12 text-center text-gray-400">Không thể tải dữ liệu dashboard. <button onClick={fetchStats} className="text-brand-600 underline">Thử lại</button></div>
                            )}
                        </div>
                    )}

                    {/* ── HR Tab ── */}
                    {!loading && activeTab === 'hr' && (
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <h1 className="text-2xl font-bold text-gray-900">Quản lý Nhân Sự</h1>
                                <button onClick={() => setEmpModal({ ...BLANK_EMP })} className="flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 rounded-xl font-medium shadow transition">
                                    <Users size={18} /> Thêm nhân viên
                                </button>
                            </div>

                            <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
                                <table className="w-full text-left text-sm">
                                    <thead className="bg-gray-50 border-b border-gray-200 text-gray-500 font-semibold text-xs uppercase tracking-wide">
                                        <tr>
                                            <th className="px-5 py-3">Họ và tên</th>
                                            <th className="px-5 py-3">Chức vụ</th>
                                            <th className="px-5 py-3">Liên hệ</th>
                                            <th className="px-5 py-3">Lương</th>
                                            <th className="px-5 py-3">T.Thái</th>
                                            <th className="px-5 py-3 text-right">Hành động</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-gray-100">
                                        {employees.length === 0 && (
                                            <tr><td colSpan={6} className="px-5 py-10 text-center text-gray-400">Chưa có nhân viên. Nhấn "Thêm nhân viên" để bắt đầu.</td></tr>
                                        )}
                                        {employees.map(emp => (
                                            <tr key={emp.id} className="hover:bg-gray-50 transition">
                                                <td className="px-5 py-4 font-medium text-gray-900">{emp.full_name}</td>
                                                <td className="px-5 py-4"><RoleBadge role={emp.role} /></td>
                                                <td className="px-5 py-4">
                                                    <div className="text-gray-700">{emp.email}</div>
                                                    <div className="text-gray-400 text-xs">{emp.phone}</div>
                                                </td>
                                                <td className="px-5 py-4 font-medium">{formatPrice(emp.salary)}</td>
                                                <td className="px-5 py-4">
                                                    {emp.is_active
                                                        ? <span className="flex items-center gap-1 text-green-600 text-xs font-semibold"><Check size={12} />Hoạt động</span>
                                                        : <span className="text-red-500 text-xs font-semibold">Nghỉ</span>}
                                                </td>
                                                <td className="px-5 py-4 text-right space-x-1">
                                                    <button onClick={() => setEmpModal({ ...emp })} className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition"><Edit size={15} /></button>
                                                    <button onClick={() => deleteEmployee(emp.id)} className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"><Trash2 size={15} /></button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )}

                    {/* ── Inventory Tab ── */}
                    {!loading && activeTab === 'inventory' && (
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <h1 className="text-2xl font-bold text-gray-900">Quản lý Kho Hàng</h1>
                                <button onClick={() => setProdModal({ ...BLANK_PROD })} className="flex items-center gap-2 bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 rounded-xl font-medium shadow transition">
                                    <PackagePlus size={18} /> Thêm sản phẩm
                                </button>
                            </div>

                            <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm">
                                <table className="w-full text-left text-sm">
                                    <thead className="bg-gray-50 border-b border-gray-200 text-gray-500 font-semibold text-xs uppercase tracking-wide">
                                        <tr>
                                            <th className="px-5 py-3">SKU</th>
                                            <th className="px-5 py-3">Tên sản phẩm</th>
                                            <th className="px-5 py-3">Giá gốc</th>
                                            <th className="px-5 py-3">Giá bán</th>
                                            <th className="px-5 py-3">T.Thái</th>
                                            <th className="px-5 py-3 text-right">Hành động</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-gray-100">
                                        {products.length === 0 && (
                                            <tr><td colSpan={6} className="px-5 py-10 text-center text-gray-400">Chưa có sản phẩm. Nhấn "Thêm sản phẩm" để thêm mới.</td></tr>
                                        )}
                                        {products.map(p => (
                                            <tr key={p.id} className="hover:bg-gray-50 transition">
                                                <td className="px-5 py-4 font-mono text-gray-400 text-xs">{p.sku}</td>
                                                <td className="px-5 py-4 font-medium text-gray-900 max-w-xs truncate">{p.name}</td>
                                                <td className="px-5 py-4 text-gray-500">{formatPrice(p.base_price)}/{p.unit}</td>
                                                <td className="px-5 py-4 font-semibold text-brand-600">{formatPrice(p.sale_price || p.base_price)}</td>
                                                <td className="px-5 py-4">
                                                    <span className={`px-2 py-1 rounded-full text-xs font-bold ${p.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                                                        {p.is_active ? 'Đang bán' : 'Ngừng bán'}
                                                    </span>
                                                </td>
                                                <td className="px-5 py-4 text-right space-x-1">
                                                    <button onClick={() => setProdModal({ ...p, sale_price: p.sale_price || 0 })} className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition"><Edit size={15} /></button>
                                                    <button onClick={() => deleteProduct(p.id)} className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"><Trash2 size={15} /></button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </Layout>
    );
}
