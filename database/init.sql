-- =====================================================
-- QUICK COMMERCE - CỬA HÀNG TIỆN LỢI
-- Database Schema Initialization
-- =====================================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "unaccent";

-- =====================================================
-- ENUM TYPES
-- =====================================================

-- User roles
CREATE TYPE user_role AS ENUM ('customer', 'staff', 'admin');

-- Order status
CREATE TYPE order_status AS ENUM (
    'pending',      -- Chờ xác nhận
    'confirmed',    -- Đã xác nhận
    'picking',      -- Đang soạn hàng
    'delivering',   -- Đang giao
    'completed',    -- Hoàn thành
    'cancelled'     -- Đã hủy
);

-- Payment methods
CREATE TYPE payment_method AS ENUM ('cod', 'momo', 'vnpay', 'bank_transfer');

-- Payment status
CREATE TYPE payment_status AS ENUM ('pending', 'paid', 'failed', 'refunded');

-- =====================================================
-- TABLES
-- =====================================================

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    role user_role DEFAULT 'customer',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    image_path VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    base_price DECIMAL(12, 2) NOT NULL CHECK (base_price >= 0),
    sale_price DECIMAL(12, 2) CHECK (sale_price >= 0),
    unit VARCHAR(50) DEFAULT 'cái',  -- cái, chai, hộp, kg, gói...
    image_path VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    is_age_restricted BOOLEAN DEFAULT FALSE,
    min_age INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Inventory Batches table (Quản lý lô hàng - FEFO)
CREATE TABLE inventory_batches (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    batch_code VARCHAR(50) NOT NULL,
    expiry_date DATE,
    quantity_on_hand INTEGER NOT NULL DEFAULT 0 CHECK (quantity_on_hand >= 0),
    quantity_reserved INTEGER NOT NULL DEFAULT 0 CHECK (quantity_reserved >= 0),
    cost_price DECIMAL(12, 2) CHECK (cost_price >= 0),
    received_date DATE DEFAULT CURRENT_DATE,
    location VARCHAR(100),  -- Vị trí trong kho: "Kệ A1", "Tủ lạnh 1"
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, batch_code)
);

-- Orders table
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    status order_status DEFAULT 'pending',
    subtotal DECIMAL(12, 2) NOT NULL DEFAULT 0,
    delivery_fee DECIMAL(12, 2) NOT NULL DEFAULT 0,
    discount_amount DECIMAL(12, 2) NOT NULL DEFAULT 0,
    total_amount DECIMAL(12, 2) NOT NULL DEFAULT 0,
    delivery_address TEXT,
    customer_phone VARCHAR(20),
    customer_name VARCHAR(100),
    notes TEXT,
    payment_method payment_method DEFAULT 'cod',
    payment_status payment_status DEFAULT 'pending',
    is_age_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Order Items table
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    batch_id INTEGER REFERENCES inventory_batches(id) ON DELETE SET NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_purchase DECIMAL(12, 2) NOT NULL,  -- Snapshot giá tại thời điểm mua
    subtotal DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Shopping Carts table
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Cart Items table
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    added_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cart_id, product_id)
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Users indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(is_active);

-- Categories indexes
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_active ON categories(is_active);
CREATE INDEX idx_categories_sort ON categories(sort_order);

-- Products indexes
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_products_age_restricted ON products(is_age_restricted);
CREATE INDEX idx_products_name_search ON products USING gin(to_tsvector('simple', name));

-- Inventory indexes
CREATE INDEX idx_inventory_product ON inventory_batches(product_id);
CREATE INDEX idx_inventory_expiry ON inventory_batches(expiry_date);
CREATE INDEX idx_inventory_available ON inventory_batches(product_id, expiry_date) 
    WHERE quantity_on_hand > quantity_reserved;

-- Orders indexes
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_at DESC);
CREATE INDEX idx_orders_payment ON orders(payment_status);

-- Order items indexes
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);

-- Cart indexes
CREATE INDEX idx_cart_items_cart ON cart_items(cart_id);
CREATE INDEX idx_cart_items_product ON cart_items(product_id);

-- =====================================================
-- FUNCTIONS & TRIGGERS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_orders_updated_at
    BEFORE UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_carts_updated_at
    BEFORE UPDATE ON carts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to calculate available stock
CREATE OR REPLACE FUNCTION get_available_stock(p_product_id INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN COALESCE(
        (SELECT SUM(quantity_on_hand - quantity_reserved)
         FROM inventory_batches
         WHERE product_id = p_product_id
           AND (expiry_date IS NULL OR expiry_date > CURRENT_DATE)),
        0
    );
END;
$$ LANGUAGE plpgsql;

-- Function to get product price (sale_price or base_price)
CREATE OR REPLACE FUNCTION get_product_price(p_product_id INTEGER)
RETURNS DECIMAL AS $$
BEGIN
    RETURN (
        SELECT COALESCE(sale_price, base_price)
        FROM products
        WHERE id = p_product_id
    );
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- VIEWS
-- =====================================================

-- View: Products with stock info
CREATE OR REPLACE VIEW v_products_with_stock AS
SELECT 
    p.*,
    c.name AS category_name,
    c.slug AS category_slug,
    COALESCE(get_available_stock(p.id), 0) AS available_stock,
    COALESCE(p.sale_price, p.base_price) AS current_price,
    (SELECT MIN(expiry_date) 
     FROM inventory_batches ib 
     WHERE ib.product_id = p.id 
       AND ib.quantity_on_hand > ib.quantity_reserved
       AND (ib.expiry_date IS NULL OR ib.expiry_date > CURRENT_DATE)
    ) AS nearest_expiry
FROM products p
LEFT JOIN categories c ON p.category_id = c.id;

-- View: Order summary
CREATE OR REPLACE VIEW v_order_summary AS
SELECT 
    o.*,
    u.full_name AS user_name,
    u.email AS user_email,
    COUNT(oi.id) AS total_items,
    SUM(oi.quantity) AS total_quantity
FROM orders o
LEFT JOIN users u ON o.user_id = u.id
LEFT JOIN order_items oi ON o.id = oi.order_id
GROUP BY o.id, u.full_name, u.email;

-- =====================================================
-- SCHEMA COMPLETE
-- =====================================================

-- Output success message
DO $$
BEGIN
    RAISE NOTICE '✅ Database schema created successfully!';
    RAISE NOTICE '   - Users table';
    RAISE NOTICE '   - Categories table';
    RAISE NOTICE '   - Products table';
    RAISE NOTICE '   - Inventory Batches table';
    RAISE NOTICE '   - Orders table';
    RAISE NOTICE '   - Order Items table';
    RAISE NOTICE '   - Carts table';
    RAISE NOTICE '   - Cart Items table';
    RAISE NOTICE '   - Views & Functions created';
END $$;
