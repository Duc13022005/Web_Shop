# Design Spec: Kiểm thử Mantis cho Website Cửa hàng Tiện lợi 7coMART

**Ngày thiết kế**: 2026-05-31
**Tác giả**: Antigravity (Advanced Agentic Coding - Google DeepMind)
**Trạng thái**: Đã phê duyệt bởi Người dùng

---

## 1. Tổng quan Dự án & Yêu cầu
Mục tiêu là chuyển đổi toàn bộ báo cáo bài tập lớn từ đề tài cũ (Khai phá dữ liệu năng suất cây trồng) sang đề tài mới: **"Kiểm thử Mantis cho Website Cửa hàng Tiện lợi"** (dựa trên mã nguồn web 7coMART có sẵn).
Báo cáo gồm 5 chương chính, tuân thủ nghiêm ngặt định dạng LaTeX của Trường Đại học Đại Nam (DNU) và tích hợp các kiến thức kiểm thử hộp đen nâng cao, quản lý lỗi bằng công cụ Mantis Bug Tracker, kiểm thử hồi quy và các độ đo chất lượng.

---

## 2. Kiến trúc & Cấu trúc Chương Báo cáo

### CHƯƠNG 1: TỔNG QUAN VỀ DỰ ÁN VÀ CƠ SỞ LÝ THUYẾT
*   **1.1. Giới thiệu dự án 7coMART**: 
    *   Bối cảnh Quick Commerce.
    *   Kiến trúc: React TypeScript (Frontend), Python FastAPI (Backend), PostgreSQL + Redis (Database/Cache/Locking), Docker Compose.
    *   Luồng nghiệp vụ cốt lõi: Xác thực, Tìm kiếm & Lọc Catalog, Giỏ hàng, Đặt hàng theo hạn sử dụng (FEFO) và Pessimistic Locking.
*   **1.2. Tổng quan về Kiểm thử phần mềm**:
    *   Mục tiêu kiểm thử.
    *   Diễn giải thực tế 7 nguyên tắc kiểm thử phần mềm áp dụng trực tiếp cho 7coMART.
    *   Phân biệt Kiểm thử chức năng và Phi chức năng trong ngữ cảnh Web Shop.
*   **1.3. Tổng quan về công cụ Mantis Bug Tracker**:
    *   Giới thiệu MantisBT và vai trò quản lý vòng đời lỗi.

### CHƯƠNG 2: LẬP KẾ HOẠCH VÀ THIẾT KẾ KỊCH BẢN KIỂM THỬ
*   **2.1. Phạm vi kiểm thử (Theo Sprint)**:
    *   **Sprint 1**: Xác thực (Auth) & Tìm kiếm/Lọc sản phẩm (Search/Filter).
    *   **Sprint 2**: Giỏ hàng (Cart) & Đặt hàng/Thanh toán (Order/Checkout).
*   **2.2. Áp dụng kỹ thuật kiểm thử Hộp đen (Black-box Testing)**:
    *   *Kỹ thuật Phân lớp tương đương*: Form Đăng ký và Đăng nhập (Email, Mật khẩu).
    *   *Kỹ thuật Phân tích giá trị biên*: Số lượng sản phẩm thêm vào Giỏ hàng (Biên dưới: -1, 0, 1; Biên trên: tồn kho tối đa N, N+1).
    *   *Kỹ thuật Bảng quyết định*: Logic áp dụng mã giảm giá dựa trên 3 điều kiện (Mã đúng, Giá trị đơn hàng tối thiểu, Thời hạn).
*   **2.3. Danh sách Kịch bản kiểm thử (Test Cases)**:
    *   Tạo bảng LaTeX chi tiết chứa 15+ test cases tiêu biểu cho cả 2 Sprint với các cột: ID, Module, Tên Test Case, Đầu vào, Các bước, Kết quả mong đợi.

### CHƯƠNG 3: THỰC THI KIỂM THỬ VÀ QUẢN LÝ LỖI TRÊN MANTIS
*   **3.1. Thiết lập môi trường và Thực thi kiểm thử**:
    *   Môi trường Docker local ([http://localhost](http://localhost)).
    *   Thao tác kiểm thử thực tế trên Chrome DevTools.
    *   So sánh Actual vs Expected để đánh giá Pass/Fail.
*   **3.2. Quản lý vòng đời lỗi với Mantis**:
    *   Vẽ sơ đồ vòng đời lỗi bằng mã **TikZ** trong LaTeX: `New -> Assigned -> Resolved -> Closed`.
    *   Quy trình viết một Defect Report mẫu trên MantisBT.
*   **3.3. Thống kê một số lỗi (Bugs) tiêu biểu**:
    *   Mô tả chi tiết 3 lỗi nghiêm trọng thực tế trên 7coMART:
        1.  *Bug 1 (Auth - Block)*: Lỗi SQL Injection tại Form đăng nhập bằng mã `' OR 1=1 --`.
        2.  *Bug 2 (Search - Major)*: Lỗi 500 Internal Server Error khi tìm kiếm từ khóa tiếng Việt có dấu (Unicode).
        3.  *Bug 3 (Cart - Critical)*: Người dùng có thể hack số lượng âm (ví dụ: `-5` sản phẩm) qua API giỏ hàng.

### CHƯƠNG 4: KIỂM THỬ HỒI QUY VÀ ĐÁNH GIÁ CHẤT LƯỢNG (PHẦN NÂNG CAO)
*   **4.1. Thực hiện Kiểm thử hồi quy (Regression Testing)**:
    *   Mô tả quy trình re-test sau khi Dev báo đã sửa (Resolved) và đóng ticket (Closed).
*   **4.2. Phân tích các độ đo chất lượng (Quality Metrics)**:
    *   *Mật độ lỗi (Defect Density - DD)*: Tính toán số lỗi trên mỗi mô-đun chức năng ($DD = N_{\text{bugs}} / N_{\text{modules}} = 2.0$).
    *   *Hiệu quả loại bỏ lỗi (Defect Removal Efficiency - DRE)*:
        $$DRE = \frac{E}{E + D} \times 100\% = \frac{8}{8 + 1} \times 100\% = 88.89\%$$
*   **4.3. Báo cáo kiểm thử tổng hợp (Test Summary Report)**:
    *   Bảng tổng hợp kết quả Pass/Fail và thống kê lỗi theo mức độ nghiêm trọng.

### CHƯƠNG 5: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
*   **5.1. Kết quả đạt được**: Đánh giá độ ổn định của 7coMART sau sửa lỗi.
*   **5.2. Bài học kinh nghiệm**: Học hỏi kỹ năng thiết kế kịch bản test và làm việc cộng tác qua Mantis.
*   **5.3. Hướng phát triển cho tương lai (Kiểm thử tự động)**:
    *   Giới thiệu Automation Testing bằng Selenium/Playwright Python.
    *   Cung cấp đoạn code kiểm thử tự động đăng nhập mẫu bằng thư viện Playwright trên Python.

---

## 3. Kế hoạch Biên dịch & Hoàn tất báo cáo
*   Chỉnh sửa lần lượt các chương từ `chuong1.tex` đến `chuong5.tex`.
*   Cập nhật `thesis.tex` để chỉ nạp đúng 5 chương này (bỏ `chuong6.tex`).
*   Cập nhật `styles/thesis.sty` để đổi tiêu đề báo cáo thành: **"KIỂM THỬ HỆ THỐNG WEBSITE CỬA HÀNG TIỆN LỢI VỚI CÔNG CỤ MANTIS BUG TRACKER"** và tiêu đề học phần thành: **"BÁO CÁO BÀI TẬP LỚN\\HỌC PHẦN: KIỂM THỬ PHẦN MỀM"**.
*   Cập nhật `chapters/admin_pages.tex`, `chapters/references.tex`, và `chapters/appendix.tex` tương ứng.
*   Chạy lệnh biên dịch `pdflatex` để tạo ra file PDF hoàn chỉnh và kiểm tra độ chính xác của tài liệu.
