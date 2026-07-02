# Chương 3: HOẠCH ĐỊNH QUẢN LÝ CHẤT LƯỢNG

## 3.1 Xác định mục tiêu chất lượng
Mục tiêu chất lượng của hệ thống Cửa hàng trực tuyến là đảm bảo một hệ phần mềm ổn định, đáp ứng tốt nhu cầu mua sắm trực tuyến với độ tin cậy và hiệu năng cao.

### 3.1.1 Đảm bảo yêu cầu khách hàng
- Cung cấp tính năng xem sản phẩm, giỏ hàng, đặt hàng hoạt động trơn tru 24/7.
- Giao diện thân thiện, dễ sử dụng cho mọi lứa tuổi khách hàng (UX/UI nhất quán).
- Thông tin giá và số lượng tồn kho được đồng bộ hoàn toàn chính xác giữa CSDL (PostgreSQL) và bộ nhớ đệm (Redis).

### 3.1.2 Giảm thiểu lỗi và chi phí
- Áp dụng các bài kiểm thử sớm (Early Testing) và sử dụng TypeScript, Pydantic để bắt các lỗi thuộc về sai kiểu dữ liệu ngay từ lúc code.
- Áp dụng mô hình CI/CD để giảm thiểu lỗi khi triển khai (Deploy) phần mềm.
- Tiết kiệm chi phí bảo trì do hệ thống dùng kiến trúc tách biệt rõ ràng Frontend - Backend.

## 3.2 Xây dựng quy trình quản lý chất lượng

### 3.2.1 Xác định các giai đoạn kiểm thử
Quá trình kiểm thử phần mềm được chia thành các giai đoạn:
1. **Kiểm thử đơn vị (Unit Testing)**: Khi nhà phát triển (Dev) hoàn thiện một API hoặc Component UI độc lập.
2. **Kiểm thử tích hợp (Integration Testing)**: Khi ráp nối Frontend gọi dữ liệu từ API Backend.
3. **Kiểm thử hệ thống (System Testing)**: Khi toàn bộ chức năng (Ví dụ: Từ lúc thêm vào giỏ hàng đến lúc thanh toán xong) được hình thành.
4. **Kiểm thử chấp nhận (Acceptance Testing)**: Người kiểm thử (QA/QC) dùng thử và báo lỗi.

### 3.2.2 Lựa chọn công cụ kiểm thử tự động
- **Giới thiệu về công cụ**: Nhóm lựa chọn **Postman** để kiểm thử API tự động (Hộp đen) và **Pytest** để kiểm thử mã nguồn Backend (Hộp trắng/đơn vị).
- **Triển khai sử dụng công cụ trên phần mềm của nhóm mình**: 
  - Khởi tạo thư mục `tests` chứa các hàm kiểm thử `pytest`.
  - Thiết lập Runner chạy các lệnh test độc lập không làm dơ DB chính (Dùng DB SQLite Test).

## 3.3 Lập kế hoạch kiểm thử

### 3.3.1 Phương pháp kiểm thử
- **Phương pháp: Thủ công và Tự động**
  - **Thủ công**: 
    - Giai đoạn: Xuyên suốt quá trình phát triển UI Frontend và giai đoạn Acceptance Testing cuối cùng.
    - Cái gì: Giao diện người dùng, màu sắc, hiệu ứng (Hover, click, routing), luồng nghiệm vụ phức tạp theo tư duy của khách hàng khó tính.
  - **Tự động**: 
    - Giai đoạn: Thực thi tích hợp CI/CD trước khi xuất bản bản cập nhật mới.
    - Cái gì: Các lỗi Logic, tính toán tiền bạc, Unit test API Đăng nhập, API xem giỏ hàng và đặt hàng.

### 3.3.2 Lập báo cáo kiểm thử
- Báo cáo số ca (Testcases) pass/fail sẽ được quản lý bằng bảng tính Excel hoặc Google Sheets (Có thể tham khảo bảng Testcase Chức năng Giỏ hàng ở Chương 2.6).
