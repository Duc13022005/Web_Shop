import React, { useState } from 'react';
import { Layout } from '../components/layout/Layout';
import { contactService, ContactFormData } from '../services/contactService';
import heroImage from '../assets/images/contact-hero.jpg';
import { Mail, Phone, ShoppingBag, Loader2 } from 'lucide-react';

const ContactPage: React.FC = () => {
    const [formData, setFormData] = useState<ContactFormData>({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        message: ''
    });

    const [isLoading, setIsLoading] = useState(false);
    const [submitStatus, setSubmitStatus] = useState<{ type: 'success' | 'error', message: string } | null>(null);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setSubmitStatus(null);
        console.log('📝 [ContactPage] Form submitting...', formData);

        try {
            const response = await contactService.sendContactForm(formData);

            if (response.success) {
                setSubmitStatus({
                    type: 'success',
                    message: response.message || 'Gửi thành công! Chúng tôi sẽ liên hệ lại sớm.'
                });
                // Reset form
                setFormData({
                    first_name: '',
                    last_name: '',
                    email: '',
                    phone: '',
                    message: ''
                });
            }
        } catch (error) {
            console.error('❌ [ContactPage] Submission failed:', error);
            setSubmitStatus({
                type: 'error',
                message: 'Có lỗi xảy ra. Vui lòng thử lại sau.'
            });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Layout>
            <div className="min-h-screen bg-white">
                <div className="flex flex-col md:flex-row min-h-[calc(100vh-64px)]">

                    {/* Left Side - Image */}
                    <div className="w-full md:w-1/2 relative min-h-[300px] md:min-h-auto order-1 md:order-1">
                        <img
                            src={heroImage}
                            alt="Contact Us"
                            className="absolute inset-0 w-full h-full object-cover"
                        />
                        <div className="absolute inset-0 bg-black/20 md:bg-transparent" /> {/* Overlay for mobile text readiness if needed */}
                    </div>

                    {/* Right Side - Form */}
                    <div className="w-full md:w-1/2 p-8 md:p-16 lg:p-24 flex flex-col justify-center order-2 md:order-2">

                        <div className="max-w-lg mx-auto w-full">
                            <h2 className="text-4xl font-bold text-gray-900 mb-2">Contact Us</h2>
                            <p className="text-gray-500 mb-8">
                                Email, call, or complete the form to learn how QuickMart can solve your messaging problem.
                            </p>

                            <div className="space-y-4 mb-10 text-gray-600">
                                <p className="flex items-center gap-3">
                                    <Mail size={18} className="text-gray-400" />
                                    support@shop.vn
                                </p>
                                <p className="flex items-center gap-3">
                                    <Phone size={18} className="text-gray-400" />
                                    (024) 1234-5678
                                </p>
                                <p className="flex items-center gap-3">
                                    <ShoppingBag size={18} className="text-gray-400" />
                                    <a href="#" className="underline hover:text-brand-600">Customer Support</a>
                                </p>
                            </div>

                            <div className="mb-8">
                                <h3 className="text-2xl font-bold text-gray-900 mb-1">Get in Touch</h3>
                                <p className="text-gray-500 text-sm">you can reach us anytime</p>
                            </div>

                            <form onSubmit={handleSubmit} className="space-y-5">
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <input
                                            type="text"
                                            name="first_name"
                                            placeholder="First Name"
                                            value={formData.first_name}
                                            onChange={handleChange}
                                            required
                                            className="w-full bg-gray-50 border border-transparent focus:bg-white focus:border-brand-500 focus:ring-2 focus:ring-brand-200 rounded-xl px-4 py-3 outline-none transition-all placeholder-gray-400"
                                        />
                                    </div>
                                    <div>
                                        <input
                                            type="text"
                                            name="last_name"
                                            placeholder="Last Name"
                                            value={formData.last_name}
                                            onChange={handleChange}
                                            required
                                            className="w-full bg-gray-50 border border-transparent focus:bg-white focus:border-brand-500 focus:ring-2 focus:ring-brand-200 rounded-xl px-4 py-3 outline-none transition-all placeholder-gray-400"
                                        />
                                    </div>
                                </div>

                                <div>
                                    <input
                                        type="email"
                                        name="email"
                                        placeholder="Your email"
                                        value={formData.email}
                                        onChange={handleChange}
                                        required
                                        className="w-full bg-gray-50 border border-transparent focus:bg-white focus:border-brand-500 focus:ring-2 focus:ring-brand-200 rounded-xl px-4 py-3 outline-none transition-all placeholder-gray-400"
                                    />
                                </div>

                                <div>
                                    <div className="flex bg-gray-50 rounded-xl border border-transparent focus-within:bg-white focus-within:border-brand-500 focus-within:ring-2 focus-within:ring-brand-200 transition-all">
                                        <div className="flex items-center pl-4 pr-2 border-r border-gray-200">
                                            <span className="text-gray-500 text-sm">+84</span>
                                        </div>
                                        <input
                                            type="tel"
                                            name="phone"
                                            placeholder="Phone number"
                                            value={formData.phone}
                                            onChange={handleChange}
                                            className="w-full bg-transparent border-none rounded-r-xl px-4 py-3 outline-none placeholder-gray-400"
                                        />
                                    </div>
                                </div>

                                <div>
                                    <textarea
                                        name="message"
                                        rows={4}
                                        placeholder="How can we help?"
                                        value={formData.message}
                                        onChange={handleChange}
                                        required
                                        className="w-full bg-gray-50 border border-transparent focus:bg-white focus:border-brand-500 focus:ring-2 focus:ring-brand-200 rounded-xl px-4 py-3 outline-none transition-all placeholder-gray-400 resize-none"
                                    />
                                </div>

                                {submitStatus && (
                                    <div className={`p-4 rounded-xl text-sm font-medium ${submitStatus.type === 'success'
                                            ? 'bg-green-50 text-green-700 border border-green-200'
                                            : 'bg-red-50 text-red-700 border border-red-200'
                                        }`}>
                                        {submitStatus.message}
                                    </div>
                                )}

                                <button
                                    type="submit"
                                    disabled={isLoading}
                                    className="w-full bg-black hover:bg-gray-800 text-white font-bold py-4 rounded-xl shadow-lg hover:shadow-xl transition-all disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                                >
                                    {isLoading ? (
                                        <>
                                            <Loader2 size={20} className="animate-spin" />
                                            Sending...
                                        </>
                                    ) : (
                                        'Submit Message'
                                    )}
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default ContactPage;
