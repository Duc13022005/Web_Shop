-- =====================================================
-- QUICK COMMERCE - CỬA HÀNG TIỆN LỢI
-- Mock Data - Vietnamese Data
-- =====================================================

-- =====================================================
-- USERS (6 users: 2 admin, 2 staff, 2 customers)
-- Password: "password123" (hashed with bcrypt)
-- =====================================================

INSERT INTO users (email, password_hash, full_name, phone, address, role) VALUES
-- Admins
('admin@shop.vn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOSp6.xvEPNhKJBH9WgOqVTZpxNvh6Eme', 'Nguyễn Văn Admin', '0901234567', '123 Đường Lê Lợi, Quận 1, TP.HCM', 'admin'),
('manager@shop.vn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOSp6.xvEPNhKJBH9WgOqVTZpxNvh6Eme', 'Trần Thị Quản Lý', '0901234568', '456 Đường Nguyễn Huệ, Quận 1, TP.HCM', 'admin'),

-- Staff
('staff1@shop.vn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOSp6.xvEPNhKJBH9WgOqVTZpxNvh6Eme', 'Lê Văn Nhân Viên', '0912345678', '789 Đường Hai Bà Trưng, Quận 3, TP.HCM', 'staff'),
('staff2@shop.vn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOSp6.xvEPNhKJBH9WgOqVTZpxNvh6Eme', 'Phạm Thị Bán Hàng', '0912345679', '321 Đường Võ Văn Tần, Quận 3, TP.HCM', 'staff'),

-- Customers
('khach1@gmail.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOSp6.xvEPNhKJBH9WgOqVTZpxNvh6Eme', 'Hoàng Văn Khách', '0923456789', '100 Đường Cách Mạng Tháng 8, Quận 10, TP.HCM', 'customer'),
('khach2@gmail.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOSp6.xvEPNhKJBH9WgOqVTZpxNvh6Eme', 'Vũ Thị Mua Hàng', '0923456790', '200 Đường 3/2, Quận 10, TP.HCM', 'customer');

-- =====================================================
-- CATEGORIES (10 danh mục)
-- =====================================================

INSERT INTO categories (name, slug, description, sort_order) VALUES
('Đồ uống', 'do-uong', 'Nước ngọt, nước suối, trà, cà phê, nước ép trái cây', 1),
('Bánh kẹo', 'banh-keo', 'Bánh ngọt, kẹo, snack, chocolate', 2),
('Mì & Thực phẩm ăn liền', 'mi-an-lien', 'Mì gói, cháo gói, phở gói, bún gói', 3),
('Sữa & Sản phẩm từ sữa', 'sua', 'Sữa tươi, sữa chua, phô mai, bơ', 4),
('Đồ đông lạnh', 'dong-lanh', 'Kem, thực phẩm đông lạnh, đá viên', 5),
('Gia vị & Nước chấm', 'gia-vi', 'Nước mắm, tương ớt, dầu ăn, muối, đường', 6),
('Chăm sóc cá nhân', 'cham-soc-ca-nhan', 'Dầu gội, sữa tắm, kem đánh răng, giấy vệ sinh', 7),
('Đồ gia dụng', 'gia-dung', 'Nước rửa chén, bột giặt, túi rác', 8),
('Rượu bia', 'ruou-bia', 'Bia, rượu vang, rượu mạnh (Hạn chế độ tuổi 18+)', 9),
('Thuốc lá', 'thuoc-la', 'Thuốc lá các loại (Hạn chế độ tuổi 18+)', 10);

-- =====================================================
-- PRODUCTS (65 sản phẩm)
-- =====================================================

-- Category 1: Đồ uống (15 sản phẩm)
INSERT INTO products (sku, name, description, category_id, base_price, sale_price, unit, is_age_restricted, min_age) VALUES
('DRINK001', 'Coca-Cola lon 330ml', 'Nước ngọt có ga Coca-Cola lon 330ml', 1, 12000, 10000, 'lon', FALSE, 0),
('DRINK002', 'Pepsi lon 330ml', 'Nước ngọt có ga Pepsi lon 330ml', 1, 12000, 10000, 'lon', FALSE, 0),
('DRINK003', 'Trà xanh 0 độ chai 500ml', 'Trà xanh không đường 0 độ chai 500ml', 1, 15000, NULL, 'chai', FALSE, 0),
('DRINK004', 'Nước suối Lavie 500ml', 'Nước khoáng thiên nhiên Lavie 500ml', 1, 8000, 7000, 'chai', FALSE, 0),
('DRINK005', 'Nước cam ép Teppy 1L', 'Nước cam ép nguyên chất Teppy 1 lít', 1, 35000, 32000, 'chai', FALSE, 0),
('DRINK006', 'Cà phê lon Highlands 235ml', 'Cà phê sữa đá Highlands Coffee lon 235ml', 1, 18000, NULL, 'lon', FALSE, 0),
('DRINK007', 'Red Bull 250ml', 'Nước tăng lực Red Bull lon 250ml', 1, 22000, 20000, 'lon', FALSE, 0),
('DRINK008', 'Sting dâu 330ml', 'Nước tăng lực Sting hương dâu lon 330ml', 1, 12000, NULL, 'lon', FALSE, 0),
('DRINK009', 'Trà đào Fuze Tea 500ml', 'Trà đào Fuze Tea chai 500ml', 1, 15000, NULL, 'chai', FALSE, 0),
('DRINK010', 'Nước dừa Cocoxim 330ml', 'Nước dừa tươi Cocoxim hộp 330ml', 1, 20000, 18000, 'hộp', FALSE, 0),
('DRINK011', 'Aquafina 500ml', 'Nước tinh khiết Aquafina 500ml', 1, 7000, NULL, 'chai', FALSE, 0),
('DRINK012', 'C2 chanh 455ml', 'Trà xanh C2 hương chanh chai 455ml', 1, 12000, NULL, 'chai', FALSE, 0),
('DRINK013', 'Nước yến Sante 240ml', 'Nước yến sào Sante lon 240ml', 1, 25000, 23000, 'lon', FALSE, 0),
('DRINK014', 'Revive chai 500ml', 'Nước uống bổ sung ion Revive 500ml', 1, 15000, NULL, 'chai', FALSE, 0),
('DRINK015', 'Fanta cam 330ml', 'Nước ngọt có ga Fanta hương cam lon 330ml', 1, 12000, 10000, 'lon', FALSE, 0);

-- Category 2: Bánh kẹo (10 sản phẩm)
INSERT INTO products (sku, name, description, category_id, base_price, sale_price, unit, is_age_restricted, min_age) VALUES
('SNACK001', 'Bánh Oreo hộp 133g', 'Bánh quy Oreo kem sữa hộp 133g', 2, 28000, 25000, 'hộp', FALSE, 0),
('SNACK002', 'Chocopie hộp 6 cái', 'Bánh Chocopie Orion hộp 6 cái', 2, 38000, 35000, 'hộp', FALSE, 0),
('SNACK003', 'Bánh mì sandwich Kinh Đô', 'Bánh mì sandwich đóng gói Kinh Đô', 2, 15000, NULL, 'gói', FALSE, 0),
('SNACK004', 'Kẹo cao su Doublemint', 'Kẹo cao su Doublemint vị bạc hà thanh 5 viên', 2, 8000, NULL, 'thanh', FALSE, 0),
('SNACK005', 'Snack khoai tây Pringles 110g', 'Snack khoai tây Pringles Original 110g', 2, 55000, 50000, 'hộp', FALSE, 0),
('SNACK006', 'Bánh quy AFC 200g', 'Bánh quy mặn AFC gói 200g', 2, 25000, NULL, 'gói', FALSE, 0),
('SNACK007', 'Chocolate KitKat 2 fingers', 'Chocolate KitKat 2 thanh', 2, 15000, NULL, 'thanh', FALSE, 0),
('SNACK008', 'Oishi snack tôm 42g', 'Snack tôm cay Oishi gói 42g', 2, 10000, NULL, 'gói', FALSE, 0),
('SNACK009', 'Bánh Cosy Marie 432g', 'Bánh quy ngọt Cosy Marie hộp 432g', 2, 45000, 42000, 'hộp', FALSE, 0),
('SNACK010', 'Kẹo sữa Alpenliebe', 'Kẹo sữa Alpenliebe gói 40 viên', 2, 25000, NULL, 'gói', FALSE, 0);

-- Category 3: Mì & Thực phẩm ăn liền (8 sản phẩm)
INSERT INTO products (sku, name, description, category_id, base_price, sale_price, unit, is_age_restricted, min_age) VALUES
('NOODLE001', 'Mì Hảo Hảo tôm chua cay', 'Mì ăn liền Hảo Hảo vị tôm chua cay gói 75g', 3, 5000, 4500, 'gói', FALSE, 0),
('NOODLE002', 'Mì Omachi xốt Spaghetti', 'Mì khoai tây Omachi xốt Spaghetti gói 91g', 3, 8000, NULL, 'gói', FALSE, 0),
('NOODLE003', 'Phở bò Vifon', 'Phở bò ăn liền Vifon gói 65g', 3, 7000, NULL, 'gói', FALSE, 0),
('NOODLE004', 'Cháo gà Cháo Tươi', 'Cháo gà ăn liền Cháo Tươi gói 50g', 3, 12000, 10000, 'gói', FALSE, 0),
('NOODLE005', 'Mì 3 Miền tôm chua cay', 'Mì ăn liền 3 Miền vị tôm chua cay', 3, 4000, NULL, 'gói', FALSE, 0),
('NOODLE006', 'Mì Kokomi đại hương vị gà', 'Mì Kokomi đại gói lớn vị gà 90g', 3, 6000, NULL, 'gói', FALSE, 0),
('NOODLE007', 'Bún bò Huế Vifon', 'Bún bò Huế ăn liền Vifon gói 65g', 3, 7000, NULL, 'gói', FALSE, 0),
('NOODLE008', 'Mì ly Modern 65g', 'Mì ly Modern hương vị bò 65g', 3, 15000, 13000, 'ly', FALSE, 0);

-- Category 4: Sữa & Sản phẩm từ sữa (8 sản phẩm)
INSERT INTO products (sku, name, description, category_id, base_price, sale_price, unit, is_age_restricted, min_age) VALUES
('MILK001', 'Sữa tươi Vinamilk 180ml', 'Sữa tươi tiệt trùng Vinamilk có đường 180ml', 4, 8000, NULL, 'hộp', FALSE, 0),
('MILK002', 'Sữa TH True Milk 180ml', 'Sữa tươi tiệt trùng TH có đường 180ml', 4, 9000, 8500, 'hộp', FALSE, 0),
('MILK003', 'Sữa chua ăn Vinamilk', 'Sữa chua ăn Vinamilk có đường hộp 100g', 4, 7000, NULL, 'hộp', FALSE, 0),
('MILK004', 'Sữa đặc Ông Thọ 380g', 'Sữa đặc có đường Ông Thọ lon 380g', 4, 28000, 25000, 'lon', FALSE, 0),
('MILK005', 'Phô mai con bò cười 8 miếng', 'Phô mai Con Bò Cười hộp 8 miếng', 4, 35000, NULL, 'hộp', FALSE, 0),
('MILK006', 'Sữa chua uống Yakult', 'Sữa chua uống lên men Yakult lốc 5 chai', 4, 28000, 26000, 'lốc', FALSE, 0),
('MILK007', 'Sữa hạt óc chó TH 180ml', 'Sữa hạt óc chó TH True Nut 180ml', 4, 12000, NULL, 'hộp', FALSE, 0),
('MILK008', 'Bơ thực vật Meizan 200g', 'Bơ thực vật Meizan hộp 200g', 4, 25000, NULL, 'hộp', FALSE, 0);

-- Category 5: Đồ đông lạnh (6 sản phẩm)
INSERT INTO products (sku, name, description, category_id, base_price, sale_price, unit, is_age_restricted, min_age) VALUES
('FROZEN001', 'Kem que Merino 55g', 'Kem que Merino vanilla chocolate 55g', 5, 12000, 10000, 'que', FALSE, 0),
('FROZEN002', 'Kem hộp Celano 450ml', 'Kem hộp Celano vị vanilla 450ml', 5, 65000, 60000, 'hộp', FALSE, 0),
('FROZEN003', 'Xúc xích đông lạnh CP 500g', 'Xúc xích tiệt trùng CP gói 500g', 5, 55000, NULL, 'gói', FALSE, 0),
('FROZEN004', 'Há cảo Bibigo 400g', 'Há cảo nhân thịt Bibigo gói 400g', 5, 75000, 70000, 'gói', FALSE, 0),
('FROZEN005', 'Đá viên túi 2kg', 'Đá viên tinh khiết túi 2kg', 5, 15000, NULL, 'túi', FALSE, 0),
('FROZEN006', 'Kem Cornetto 120ml', 'Kem ốc quế Cornetto chocolate 120ml', 5, 20000, 18000, 'cây', FALSE, 0);

-- Category 6: Gia vị & Nước chấm (8 sản phẩm)
INSERT INTO products (sku, name, description, category_id, base_price, sale_price, unit, is_age_restricted, min_age) VALUES
('SPICE001', 'Nước mắm Nam Ngư 500ml', 'Nước mắm Nam Ngư chai 500ml', 6, 32000, 30000, 'chai', FALSE, 0),
('SPICE002', 'Tương ớt Chinsu 250g', 'Tương ớt Chinsu chai 250g', 6, 18000, NULL, 'chai', FALSE, 0),
('SPICE003', 'Dầu ăn Neptune 1L', 'Dầu ăn Neptune Gold chai 1 lít', 6, 55000, 52000, 'chai', FALSE, 0),
('SPICE004', 'Muối I-ốt Bạc Liêu 500g', 'Muối I-ốt Bạc Liêu gói 500g', 6, 8000, NULL, 'gói', FALSE, 0),
('SPICE005', 'Đường trắng Biên Hòa 1kg', 'Đường cát trắng Biên Hòa gói 1kg', 6, 25000, 23000, 'gói', FALSE, 0),
('SPICE006', 'Hạt nêm Knorr 400g', 'Hạt nêm Knorr từ thịt heo gói 400g', 6, 42000, 40000, 'gói', FALSE, 0),
('SPICE007', 'Nước tương Maggi 300ml', 'Nước tương đậu nành Maggi chai 300ml', 6, 22000, NULL, 'chai', FALSE, 0),
('SPICE008', 'Bột ngọt Ajinomoto 454g', 'Bột ngọt Ajinomoto gói 454g', 6, 35000, 33000, 'gói', FALSE, 0);

-- Category 7: Chăm sóc cá nhân (8 sản phẩm)
INSERT INTO products (sku, name, description, category_id, base_price, sale_price, unit, is_age_restricted, min_age) VALUES
('CARE001', 'Dầu gội Clear 650g', 'Dầu gội Clear Men Deep Cleanse 650g', 7, 125000, 115000, 'chai', FALSE, 0),
('CARE002', 'Sữa tắm Lifebuoy 500g', 'Sữa tắm kháng khuẩn Lifebuoy 500g', 7, 85000, 80000, 'chai', FALSE, 0),
('CARE003', 'Kem đánh răng PS 180g', 'Kem đánh răng P/S bảo vệ 123 180g', 7, 35000, NULL, 'tuýp', FALSE, 0),
('CARE004', 'Giấy vệ sinh Pulppy 6 cuộn', 'Giấy vệ sinh Pulppy lốc 6 cuộn', 7, 45000, 42000, 'lốc', FALSE, 0),
('CARE005', 'Bàn chải Colgate', 'Bàn chải đánh răng Colgate Slim Soft', 7, 25000, NULL, 'cái', FALSE, 0),
('CARE006', 'Khăn giấy Kleenex 100 tờ', 'Khăn giấy Kleenex hộp 100 tờ', 7, 35000, NULL, 'hộp', FALSE, 0),
('CARE007', 'Lăn khử mùi Nivea 50ml', 'Lăn khử mùi Nivea Men 50ml', 7, 65000, 60000, 'chai', FALSE, 0),
('CARE008', 'Dầu xả Sunsilk 320g', 'Dầu xả Sunsilk mềm mượt diệu kỳ 320g', 7, 75000, 70000, 'chai', FALSE, 0);

-- Category 8: Đồ gia dụng (6 sản phẩm)
INSERT INTO products (sku, name, description, category_id, base_price, sale_price, unit, is_age_restricted, min_age) VALUES
('HOME001', 'Nước rửa chén Sunlight 750g', 'Nước rửa chén Sunlight chanh 750g', 8, 42000, 40000, 'chai', FALSE, 0),
('HOME002', 'Bột giặt OMO 800g', 'Bột giặt OMO Matic túi 800g', 8, 55000, 52000, 'túi', FALSE, 0),
('HOME003', 'Túi rác tự hủy 25 cái', 'Túi rác tự hủy sinh học gói 25 cái', 8, 25000, NULL, 'gói', FALSE, 0),
('HOME004', 'Nước lau sàn Sunlight 1L', 'Nước lau sàn Sunlight hương hoa 1 lít', 8, 45000, 42000, 'chai', FALSE, 0),
('HOME005', 'Pin Energizer AA 4 viên', 'Pin kiềm Energizer AA vỉ 4 viên', 8, 65000, 60000, 'vỉ', FALSE, 0),
('HOME006', 'Giấy bạc nhôm Bách Hóa Xanh', 'Giấy bạc nhôm cuộn 5m', 8, 20000, NULL, 'cuộn', FALSE, 0);

-- Category 9: Rượu bia (Hạn chế 18+) (5 sản phẩm)
INSERT INTO products (sku, name, description, category_id, base_price, sale_price, unit, is_age_restricted, min_age) VALUES
('ALCOHOL001', 'Bia Heineken lon 330ml', 'Bia Heineken lon 330ml', 9, 18000, 16000, 'lon', TRUE, 18),
('ALCOHOL002', 'Bia Tiger lon 330ml', 'Bia Tiger lon 330ml', 9, 15000, 14000, 'lon', TRUE, 18),
('ALCOHOL003', 'Bia Saigon Special 330ml', 'Bia Sài Gòn Special lon 330ml', 9, 14000, NULL, 'lon', TRUE, 18),
('ALCOHOL004', 'Soju Jinro 360ml', 'Rượu Soju Jinro vị Original 360ml', 9, 85000, 80000, 'chai', TRUE, 18),
('ALCOHOL005', 'Bia 333 lon 330ml', 'Bia 333 lon 330ml', 9, 12000, 11000, 'lon', TRUE, 18);

-- Category 10: Thuốc lá (Hạn chế 18+) (4 sản phẩm)
INSERT INTO products (sku, name, description, category_id, base_price, sale_price, unit, is_age_restricted, min_age) VALUES
('TOBACCO001', 'Thuốc lá 555 Gold', 'Thuốc lá 555 State Express Gold bao 20 điếu', 10, 28000, NULL, 'bao', TRUE, 18),
('TOBACCO002', 'Thuốc lá Vinataba', 'Thuốc lá Vinataba bao 20 điếu', 10, 18000, NULL, 'bao', TRUE, 18),
('TOBACCO003', 'Thuốc lá Marlboro đỏ', 'Thuốc lá Marlboro Red bao 20 điếu', 10, 32000, NULL, 'bao', TRUE, 18),
('TOBACCO004', 'Thuốc lá Thăng Long', 'Thuốc lá Thăng Long bao 20 điếu', 10, 15000, NULL, 'bao', TRUE, 18);

-- =====================================================
-- INVENTORY BATCHES (120+ lô hàng)
-- Mỗi sản phẩm có 1-3 lô với expiry_date khác nhau
-- =====================================================

-- Helper function for generating batch data
-- Note: Expiry dates range from 1 month to 1 year from now

-- Đồ uống batches
INSERT INTO inventory_batches (product_id, batch_code, expiry_date, quantity_on_hand, cost_price, location) VALUES
-- Coca-Cola
(1, 'DRINK001-2024-001', CURRENT_DATE + INTERVAL '6 months', 100, 8000, 'Kệ A1'),
(1, 'DRINK001-2024-002', CURRENT_DATE + INTERVAL '8 months', 80, 8000, 'Kệ A1'),
-- Pepsi
(2, 'DRINK002-2024-001', CURRENT_DATE + INTERVAL '6 months', 90, 8000, 'Kệ A1'),
(2, 'DRINK002-2024-002', CURRENT_DATE + INTERVAL '9 months', 60, 8000, 'Kệ A2'),
-- Trà xanh 0 độ
(3, 'DRINK003-2024-001', CURRENT_DATE + INTERVAL '4 months', 50, 10000, 'Kệ A2'),
(3, 'DRINK003-2024-002', CURRENT_DATE + INTERVAL '7 months', 70, 10000, 'Kệ A2'),
-- Lavie
(4, 'DRINK004-2024-001', CURRENT_DATE + INTERVAL '12 months', 200, 5000, 'Kệ A3'),
-- Teppy
(5, 'DRINK005-2024-001', CURRENT_DATE + INTERVAL '3 months', 30, 25000, 'Tủ lạnh 1'),
-- Highlands Coffee
(6, 'DRINK006-2024-001', CURRENT_DATE + INTERVAL '8 months', 60, 12000, 'Kệ A3'),
-- Red Bull
(7, 'DRINK007-2024-001', CURRENT_DATE + INTERVAL '10 months', 80, 15000, 'Kệ A4'),
-- Sting
(8, 'DRINK008-2024-001', CURRENT_DATE + INTERVAL '6 months', 100, 8000, 'Kệ A4'),
-- Fuze Tea
(9, 'DRINK009-2024-001', CURRENT_DATE + INTERVAL '5 months', 45, 10000, 'Kệ A5'),
-- Cocoxim
(10, 'DRINK010-2024-001', CURRENT_DATE + INTERVAL '4 months', 40, 14000, 'Tủ lạnh 1'),
-- Aquafina
(11, 'DRINK011-2024-001', CURRENT_DATE + INTERVAL '12 months', 150, 4500, 'Kệ A3'),
-- C2
(12, 'DRINK012-2024-001', CURRENT_DATE + INTERVAL '6 months', 70, 8000, 'Kệ A5'),
-- Nước yến
(13, 'DRINK013-2024-001', CURRENT_DATE + INTERVAL '8 months', 35, 18000, 'Kệ A6'),
-- Revive
(14, 'DRINK014-2024-001', CURRENT_DATE + INTERVAL '6 months', 55, 10000, 'Kệ A5'),
-- Fanta
(15, 'DRINK015-2024-001', CURRENT_DATE + INTERVAL '7 months', 85, 8000, 'Kệ A1');

-- Bánh kẹo batches
INSERT INTO inventory_batches (product_id, batch_code, expiry_date, quantity_on_hand, cost_price, location) VALUES
-- Oreo
(16, 'SNACK001-2024-001', CURRENT_DATE + INTERVAL '9 months', 40, 20000, 'Kệ B1'),
(16, 'SNACK001-2024-002', CURRENT_DATE + INTERVAL '11 months', 30, 20000, 'Kệ B1'),
-- Chocopie
(17, 'SNACK002-2024-001', CURRENT_DATE + INTERVAL '6 months', 50, 28000, 'Kệ B1'),
-- Bánh mì sandwich
(18, 'SNACK003-2024-001', CURRENT_DATE + INTERVAL '7 days', 20, 10000, 'Kệ B2'),
(18, 'SNACK003-2024-002', CURRENT_DATE + INTERVAL '10 days', 15, 10000, 'Kệ B2'),
-- Doublemint
(19, 'SNACK004-2024-001', CURRENT_DATE + INTERVAL '18 months', 100, 5000, 'Kệ B3'),
-- Pringles
(20, 'SNACK005-2024-001', CURRENT_DATE + INTERVAL '12 months', 25, 40000, 'Kệ B1'),
-- AFC
(21, 'SNACK006-2024-001', CURRENT_DATE + INTERVAL '10 months', 45, 18000, 'Kệ B2'),
-- KitKat
(22, 'SNACK007-2024-001', CURRENT_DATE + INTERVAL '8 months', 60, 10000, 'Kệ B3'),
-- Oishi
(23, 'SNACK008-2024-001', CURRENT_DATE + INTERVAL '6 months', 80, 7000, 'Kệ B4'),
-- Cosy
(24, 'SNACK009-2024-001', CURRENT_DATE + INTERVAL '9 months', 30, 35000, 'Kệ B2'),
-- Alpenliebe
(25, 'SNACK010-2024-001', CURRENT_DATE + INTERVAL '12 months', 70, 18000, 'Kệ B3');

-- Mì ăn liền batches
INSERT INTO inventory_batches (product_id, batch_code, expiry_date, quantity_on_hand, cost_price, location) VALUES
-- Hảo Hảo
(26, 'NOODLE001-2024-001', CURRENT_DATE + INTERVAL '6 months', 200, 3500, 'Kệ C1'),
(26, 'NOODLE001-2024-002', CURRENT_DATE + INTERVAL '8 months', 150, 3500, 'Kệ C1'),
-- Omachi
(27, 'NOODLE002-2024-001', CURRENT_DATE + INTERVAL '7 months', 120, 6000, 'Kệ C1'),
-- Phở Vifon
(28, 'NOODLE003-2024-001', CURRENT_DATE + INTERVAL '6 months', 80, 5000, 'Kệ C2'),
-- Cháo Tươi
(29, 'NOODLE004-2024-001', CURRENT_DATE + INTERVAL '5 months', 50, 8000, 'Kệ C2'),
-- 3 Miền
(30, 'NOODLE005-2024-001', CURRENT_DATE + INTERVAL '6 months', 180, 3000, 'Kệ C3'),
-- Kokomi
(31, 'NOODLE006-2024-001', CURRENT_DATE + INTERVAL '6 months', 100, 4500, 'Kệ C3'),
-- Bún bò Huế
(32, 'NOODLE007-2024-001', CURRENT_DATE + INTERVAL '6 months', 70, 5000, 'Kệ C2'),
-- Mì ly Modern
(33, 'NOODLE008-2024-001', CURRENT_DATE + INTERVAL '7 months', 40, 10000, 'Kệ C4');

-- Sữa batches
INSERT INTO inventory_batches (product_id, batch_code, expiry_date, quantity_on_hand, cost_price, location) VALUES
-- Vinamilk
(34, 'MILK001-2024-001', CURRENT_DATE + INTERVAL '2 months', 100, 6000, 'Tủ lạnh 2'),
(34, 'MILK001-2024-002', CURRENT_DATE + INTERVAL '3 months', 80, 6000, 'Tủ lạnh 2'),
-- TH True Milk
(35, 'MILK002-2024-001', CURRENT_DATE + INTERVAL '2 months', 90, 7000, 'Tủ lạnh 2'),
-- Sữa chua Vinamilk
(36, 'MILK003-2024-001', CURRENT_DATE + INTERVAL '1 month', 60, 5000, 'Tủ lạnh 2'),
(36, 'MILK003-2024-002', CURRENT_DATE + INTERVAL '45 days', 40, 5000, 'Tủ lạnh 2'),
-- Sữa đặc Ông Thọ
(37, 'MILK004-2024-001', CURRENT_DATE + INTERVAL '18 months', 50, 20000, 'Kệ D1'),
-- Phô mai con bò cười
(38, 'MILK005-2024-001', CURRENT_DATE + INTERVAL '4 months', 30, 25000, 'Tủ lạnh 2'),
-- Yakult
(39, 'MILK006-2024-001', CURRENT_DATE + INTERVAL '30 days', 40, 20000, 'Tủ lạnh 2'),
-- TH True Nut
(40, 'MILK007-2024-001', CURRENT_DATE + INTERVAL '3 months', 50, 9000, 'Tủ lạnh 2'),
-- Bơ Meizan
(41, 'MILK008-2024-001', CURRENT_DATE + INTERVAL '6 months', 25, 18000, 'Tủ lạnh 2');

-- Đồ đông lạnh batches
INSERT INTO inventory_batches (product_id, batch_code, expiry_date, quantity_on_hand, cost_price, location) VALUES
-- Kem Merino
(42, 'FROZEN001-2024-001', CURRENT_DATE + INTERVAL '6 months', 80, 8000, 'Tủ đông 1'),
-- Kem Celano
(43, 'FROZEN002-2024-001', CURRENT_DATE + INTERVAL '8 months', 20, 50000, 'Tủ đông 1'),
-- Xúc xích CP
(44, 'FROZEN003-2024-001', CURRENT_DATE + INTERVAL '4 months', 30, 42000, 'Tủ đông 2'),
-- Há cảo Bibigo
(45, 'FROZEN004-2024-001', CURRENT_DATE + INTERVAL '6 months', 25, 58000, 'Tủ đông 2'),
-- Đá viên
(46, 'FROZEN005-2024-001', CURRENT_DATE + INTERVAL '12 months', 50, 10000, 'Tủ đông 1'),
-- Cornetto
(47, 'FROZEN006-2024-001', CURRENT_DATE + INTERVAL '6 months', 60, 14000, 'Tủ đông 1');

-- Gia vị batches
INSERT INTO inventory_batches (product_id, batch_code, expiry_date, quantity_on_hand, cost_price, location) VALUES
-- Nước mắm Nam Ngư
(48, 'SPICE001-2024-001', CURRENT_DATE + INTERVAL '18 months', 50, 24000, 'Kệ E1'),
-- Tương ớt Chinsu
(49, 'SPICE002-2024-001', CURRENT_DATE + INTERVAL '12 months', 60, 13000, 'Kệ E1'),
-- Dầu ăn Neptune
(50, 'SPICE003-2024-001', CURRENT_DATE + INTERVAL '12 months', 40, 42000, 'Kệ E2'),
-- Muối
(51, 'SPICE004-2024-001', CURRENT_DATE + INTERVAL '24 months', 100, 5000, 'Kệ E3'),
-- Đường
(52, 'SPICE005-2024-001', CURRENT_DATE + INTERVAL '24 months', 80, 18000, 'Kệ E3'),
-- Hạt nêm Knorr
(53, 'SPICE006-2024-001', CURRENT_DATE + INTERVAL '18 months', 45, 32000, 'Kệ E2'),
-- Nước tương Maggi
(54, 'SPICE007-2024-001', CURRENT_DATE + INTERVAL '18 months', 55, 16000, 'Kệ E1'),
-- Bột ngọt
(55, 'SPICE008-2024-001', CURRENT_DATE + INTERVAL '24 months', 70, 28000, 'Kệ E3');

-- Chăm sóc cá nhân batches
INSERT INTO inventory_batches (product_id, batch_code, expiry_date, quantity_on_hand, cost_price, location) VALUES
-- Dầu gội Clear
(56, 'CARE001-2024-001', CURRENT_DATE + INTERVAL '24 months', 25, 95000, 'Kệ F1'),
-- Sữa tắm Lifebuoy
(57, 'CARE002-2024-001', CURRENT_DATE + INTERVAL '24 months', 30, 65000, 'Kệ F1'),
-- Kem đánh răng PS
(58, 'CARE003-2024-001', CURRENT_DATE + INTERVAL '24 months', 50, 25000, 'Kệ F2'),
-- Giấy vệ sinh
(59, 'CARE004-2024-001', CURRENT_DATE + INTERVAL '36 months', 40, 35000, 'Kệ F3'),
-- Bàn chải Colgate
(60, 'CARE005-2024-001', CURRENT_DATE + INTERVAL '36 months', 60, 18000, 'Kệ F2'),
-- Khăn giấy Kleenex
(61, 'CARE006-2024-001', CURRENT_DATE + INTERVAL '36 months', 45, 28000, 'Kệ F3'),
-- Lăn khử mùi Nivea
(62, 'CARE007-2024-001', CURRENT_DATE + INTERVAL '24 months', 35, 50000, 'Kệ F1'),
-- Dầu xả Sunsilk
(63, 'CARE008-2024-001', CURRENT_DATE + INTERVAL '24 months', 28, 58000, 'Kệ F1');

-- Đồ gia dụng batches
INSERT INTO inventory_batches (product_id, batch_code, expiry_date, quantity_on_hand, cost_price, location) VALUES
-- Nước rửa chén Sunlight
(64, 'HOME001-2024-001', CURRENT_DATE + INTERVAL '24 months', 40, 32000, 'Kệ G1'),
-- Bột giặt OMO
(65, 'HOME002-2024-001', CURRENT_DATE + INTERVAL '24 months', 35, 42000, 'Kệ G1'),
-- Túi rác
(66, 'HOME003-2024-001', CURRENT_DATE + INTERVAL '36 months', 60, 18000, 'Kệ G2'),
-- Nước lau sàn
(67, 'HOME004-2024-001', CURRENT_DATE + INTERVAL '24 months', 30, 35000, 'Kệ G1'),
-- Pin Energizer
(68, 'HOME005-2024-001', CURRENT_DATE + INTERVAL '60 months', 50, 50000, 'Kệ G3'),
-- Giấy bạc nhôm
(69, 'HOME006-2024-001', CURRENT_DATE + INTERVAL '36 months', 40, 15000, 'Kệ G2');

-- Rượu bia batches
INSERT INTO inventory_batches (product_id, batch_code, expiry_date, quantity_on_hand, cost_price, location) VALUES
-- Heineken
(70, 'ALCOHOL001-2024-001', CURRENT_DATE + INTERVAL '9 months', 100, 12000, 'Tủ lạnh 3'),
(70, 'ALCOHOL001-2024-002', CURRENT_DATE + INTERVAL '12 months', 80, 12000, 'Kho B'),
-- Tiger
(71, 'ALCOHOL002-2024-001', CURRENT_DATE + INTERVAL '9 months', 120, 10000, 'Tủ lạnh 3'),
-- Saigon Special
(72, 'ALCOHOL003-2024-001', CURRENT_DATE + INTERVAL '9 months', 100, 10000, 'Tủ lạnh 3'),
-- Soju Jinro
(73, 'ALCOHOL004-2024-001', CURRENT_DATE + INTERVAL '24 months', 40, 65000, 'Kệ H1'),
-- Bia 333
(74, 'ALCOHOL005-2024-001', CURRENT_DATE + INTERVAL '9 months', 90, 8000, 'Tủ lạnh 3');

-- Thuốc lá batches
INSERT INTO inventory_batches (product_id, batch_code, expiry_date, quantity_on_hand, cost_price, location) VALUES
-- 555 Gold
(75, 'TOBACCO001-2024-001', CURRENT_DATE + INTERVAL '18 months', 50, 22000, 'Quầy thu ngân'),
-- Vinataba
(76, 'TOBACCO002-2024-001', CURRENT_DATE + INTERVAL '18 months', 60, 14000, 'Quầy thu ngân'),
-- Marlboro
(77, 'TOBACCO003-2024-001', CURRENT_DATE + INTERVAL '18 months', 40, 25000, 'Quầy thu ngân'),
-- Thăng Long
(78, 'TOBACCO004-2024-001', CURRENT_DATE + INTERVAL '18 months', 70, 12000, 'Quầy thu ngân');

-- =====================================================
-- SAMPLE ORDERS (5 đơn hàng mẫu)
-- =====================================================

-- Order 1: Khách hàng đặt đồ uống
INSERT INTO orders (user_id, status, subtotal, delivery_fee, total_amount, delivery_address, customer_phone, customer_name, notes, payment_method, payment_status)
VALUES (5, 'completed', 66000, 15000, 81000, '100 Đường Cách Mạng Tháng 8, Quận 10, TP.HCM', '0923456789', 'Hoàng Văn Khách', 'Giao giờ hành chính', 'cod', 'paid');

INSERT INTO order_items (order_id, product_id, batch_id, quantity, price_at_purchase, subtotal) VALUES
(1, 1, 1, 3, 10000, 30000),  -- 3 lon Coca
(1, 7, 10, 2, 18000, 36000); -- 2 lon Red Bull

-- Order 2: Khách hàng đặt mì + sữa
INSERT INTO orders (user_id, status, subtotal, delivery_fee, total_amount, delivery_address, customer_phone, customer_name, payment_method, payment_status)
VALUES (6, 'delivering', 85500, 15000, 100500, '200 Đường 3/2, Quận 10, TP.HCM', '0923456790', 'Vũ Thị Mua Hàng', 'momo', 'paid');

INSERT INTO order_items (order_id, product_id, batch_id, quantity, price_at_purchase, subtotal) VALUES
(2, 26, 31, 10, 4500, 45000),  -- 10 gói Hảo Hảo
(2, 34, 41, 5, 8000, 40000);   -- 5 hộp sữa Vinamilk

-- Order 3: Đơn hàng có sản phẩm hạn chế tuổi
INSERT INTO orders (user_id, status, subtotal, delivery_fee, total_amount, delivery_address, customer_phone, customer_name, payment_method, payment_status, is_age_verified)
VALUES (5, 'confirmed', 128000, 15000, 143000, '100 Đường Cách Mạng Tháng 8, Quận 10, TP.HCM', '0923456789', 'Hoàng Văn Khách', 'vnpay', 'paid', TRUE);

INSERT INTO order_items (order_id, product_id, batch_id, quantity, price_at_purchase, subtotal) VALUES
(3, 70, 81, 4, 16000, 64000),  -- 4 lon Heineken
(3, 71, 83, 4, 14000, 56000),  -- 4 lon Tiger
(3, 23, 28, 1, 8000, 8000);    -- 1 gói snack Oishi

-- Order 4: Đơn hàng đang soạn
INSERT INTO orders (user_id, status, subtotal, delivery_fee, total_amount, delivery_address, customer_phone, customer_name, payment_method, payment_status)
VALUES (6, 'picking', 165000, 20000, 185000, '200 Đường 3/2, Quận 10, TP.HCM', '0923456790', 'Vũ Thị Mua Hàng', 'cod', 'pending');

INSERT INTO order_items (order_id, product_id, batch_id, quantity, price_at_purchase, subtotal) VALUES
(4, 56, 66, 1, 115000, 115000), -- 1 chai dầu gội Clear
(4, 59, 69, 1, 42000, 42000),   -- 1 lốc giấy vệ sinh
(4, 19, 24, 1, 8000, 8000);     -- 1 thanh kẹo cao su

-- Order 5: Đơn hàng chờ xác nhận
INSERT INTO orders (user_id, status, subtotal, delivery_fee, total_amount, delivery_address, customer_phone, customer_name, notes, payment_method, payment_status)
VALUES (5, 'pending', 205000, 15000, 220000, '100 Đường Cách Mạng Tháng 8, Quận 10, TP.HCM', '0923456789', 'Hoàng Văn Khách', 'Gọi điện trước khi giao', 'bank_transfer', 'pending');

INSERT INTO order_items (order_id, product_id, batch_id, quantity, price_at_purchase, subtotal) VALUES
(5, 50, 62, 2, 52000, 104000),  -- 2 chai dầu ăn Neptune
(5, 48, 60, 2, 30000, 60000),   -- 2 chai nước mắm
(5, 53, 64, 1, 40000, 40000);   -- 1 gói hạt nêm Knorr

-- =====================================================
-- SAMPLE CARTS (Giỏ hàng cho customers)
-- =====================================================

-- Cart for customer 1
INSERT INTO carts (user_id) VALUES (5);

INSERT INTO cart_items (cart_id, product_id, quantity) VALUES
(1, 1, 6),   -- 6 lon Coca
(1, 17, 2), -- 2 hộp Chocopie
(1, 34, 3); -- 3 hộp sữa Vinamilk

-- Cart for customer 2
INSERT INTO carts (user_id) VALUES (6);

INSERT INTO cart_items (cart_id, product_id, quantity) VALUES
(2, 42, 4),  -- 4 que kem
(2, 26, 5); -- 5 gói mì Hảo Hảo

-- =====================================================
-- DATA SUMMARY
-- =====================================================

DO $$
DECLARE
    user_count INTEGER;
    category_count INTEGER;
    product_count INTEGER;
    batch_count INTEGER;
    order_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO user_count FROM users;
    SELECT COUNT(*) INTO category_count FROM categories;
    SELECT COUNT(*) INTO product_count FROM products;
    SELECT COUNT(*) INTO batch_count FROM inventory_batches;
    SELECT COUNT(*) INTO order_count FROM orders;
    
    RAISE NOTICE '✅ Mock data inserted successfully!';
    RAISE NOTICE '   - Users: %', user_count;
    RAISE NOTICE '   - Categories: %', category_count;
    RAISE NOTICE '   - Products: %', product_count;
    RAISE NOTICE '   - Inventory Batches: %', batch_count;
    RAISE NOTICE '   - Orders: %', order_count;
    RAISE NOTICE '';
    RAISE NOTICE '📝 Test accounts:';
    RAISE NOTICE '   - Admin: admin@shop.vn / password123';
    RAISE NOTICE '   - Staff: staff1@shop.vn / password123';
    RAISE NOTICE '   - Customer: khach1@gmail.com / password123';
END $$;
