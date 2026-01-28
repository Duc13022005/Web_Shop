import React from 'react';
import { Star, Plus, ShoppingCart } from 'lucide-react';
import { Link } from 'react-router-dom';

interface ProductProps {
    id: number;
    name: string;
    category: string;
    price: number;
    originalPrice?: number;
    image: string;
    rating: number;
    reviews: number;
    unit: string;
}

export const ProductCard: React.FC<ProductProps> = ({
    id, name, category, price, originalPrice, image, rating, unit
}) => {
    return (
        <div className="group bg-white rounded-xl border border-gray-100 hover:shadow-lg transition-all duration-300 overflow-hidden flex flex-col h-full">
            {/* Image Container */}
            <Link to={`/products/${id}`} className="block relative h-48 overflow-hidden bg-gray-50">
                <img
                    src={image}
                    alt={name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                {originalPrice && (
                    <span className="absolute top-2 left-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full">
                        -{Math.round(((originalPrice - price) / originalPrice) * 100)}%
                    </span>
                )}
                <button className="absolute bottom-2 right-2 bg-white/90 p-2 rounded-full shadow-sm hover:bg-brand-500 hover:text-white transition opacity-0 group-hover:opacity-100 translate-y-2 group-hover:translate-y-0 duration-300">
                    <Plus size={20} />
                </button>
            </Link>

            {/* Content */}
            <div className="p-4 flex flex-col flex-grow">
                <div className="text-xs text-brand-600 font-medium mb-1 uppercase tracking-wider">{category}</div>
                <Link to={`/products/${id}`}>
                    <h3 className="font-bold text-gray-800 mb-1 line-clamp-2 min-h-[48px] cursor-pointer hover:text-brand-600 transition">
                        {name}
                    </h3>
                </Link>

                <div className="flex items-center gap-1 mb-3">
                    <Star size={14} className="fill-yellow-400 text-yellow-400" />
                    <span className="text-sm text-gray-500 font-medium">{rating}</span>
                    <span className="text-xs text-gray-400">({unit})</span>
                </div>

                <div className="mt-auto flex items-center justify-between">
                    <div className="flex flex-col">
                        <span className="text-lg font-bold text-gray-900">${price.toLocaleString('vi-VN')}</span>
                        {originalPrice && (
                            <span className="text-xs text-gray-400 line-through">${originalPrice.toLocaleString('vi-VN')}</span>
                        )}
                    </div>
                    <button className="bg-gray-100 hover:bg-brand-600 hover:text-white text-gray-700 px-3 py-2 rounded-lg transition-colors flex items-center gap-2 text-sm font-medium group/btn">
                        Add
                        <ShoppingCart size={16} className="group-hover/btn:fill-white" />
                    </button>
                </div>
            </div>
        </div>
    );
};
