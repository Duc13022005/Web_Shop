# Chương 4: KẾT QUẢ NGHIÊN CỨU VÀ ĐÁNH GIÁ

## 4.1 Kết quả đạt được

### Kiến thức 
- Nhóm đã làm quen và áp dụng thành công các mô hình kiến trúc Client-Server hiện đại.
- Hiểu biết sâu sắc về thiết kế Cơ sở dữ liệu, tối ưu hóa truy vấn SQL trên PostgreSQL.
- Biết cách thức xây dựng API chuẩn RESTful với framework FastAPI.
- Vận dụng linh hoạt thư viện React và Tailwind CSS để thiết kế website thương mại thân thiện người dùng.
- Hiểu và áp dụng các kỹ thuật thử nghiệm BVA, EP vào thực tiễn thiết kế Testcase.

### Sản phẩm 
Hệ thống **Web_Shop - Cửa hàng trực tuyến** đã cơ bản hoạt động ổn định với các luồng nghiệp vụ: Xác thực - Xem sản phẩm - Duyệt giỏ hàng - Lên đơn hàng - Quản trị kho.

**Tự đánh giá (bảng đánh giá ISO 25010)**

| Đặc trưng | Tiêu chí | Thang điểm | Điểm chấm |
|---|---|---|---|
| Tính chức năng | Các tính năng cốt lõi (Cart, Checkout) | 10 | 8.5 |
| Độ tin cậy | Giảm thiểu crash và sai sót số liệu tính toán | 10 | 9.0 |
| Hiệu suất | Thời gian tải trang hiển thị danh sách sản phẩm | 10 | 9.5 |
| Khả năng sử dụng | Giao diện trực quan dễ thao tác | 10 | 8.5 |
| **Tổng điểm** | | **40** | **35.5 / 40** |

*(Ghi chú: Đánh giá ngoài (bảng đánh giá ISO 916 (25010)) sẽ chờ ý kiến từ giáo viên hướng dẫn)*

## 4.2 Ưu điểm và nhược điểm

**Ưu điểm**
- Sử dụng Stack công nghệ hiện đại, khả năng mở rộng (Scale-up) tốt.
- Tách biệt rõ ràng vòng đời của 1 Order và nghiệp vụ kho hàng.
- UI đáp ứng thân thiện (Responsive) và chạy nhanh trên cả di động và PC.
- Cấu trúc thư mục Code gọn gàng, chia Component hợp lý.

**Nhược điểm**
- Vì thời gian có hạn nên chức năng thanh toán trực tuyến qua các ví điện tử (Momo/VNPay) chưa được tích hợp thực tiễn, mà mới chỉ dừng ở mức lưu trữ dữ liệu Enum.
- Vì kiến thức còn hạn chế nên chưa ứng dụng được AI Gợi ý sản phẩm cho trang chủ.
- Vì điều kiện đầu tư còn hạn hẹp nên chưa triển khai (Deploy) sản phẩm được lên các máy chủ cấu hình mạnh chạy thực tế (Production Domain), hiện tại mới đóng gói chạy Docker Container nội bộ.

## 4.3 Công việc tương lai
- Trong tương lai, nếu có thêm thời gian, em sẽ tìm hiểu và tích hợp chức năng Thanh toán Online qua trung gian VNPAY/Momo để hỗ trợ hình thức mua hàng không tiền mặt.
- Em sẽ tìm hiểu thêm công nghệ Recommender System (Machine Learning) để có thể bổ sung thêm các chức năng gợi ý hàng hóa dựa trên hành vi mua hàng cũ của user, giúp cá nhân hóa cho khách hàng.
- Nếu tìm được nguồn đầu tư dự án sẽ phát triển thêm chức năng Ứng dụng điện thoại riêng (Mobile App viết bằng React Native) thay vì chỉ truy cập từ nền tảng web.
