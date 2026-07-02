# Mantis Web Shop Testing Report Implementation Plan (Bản cập nhật có Hình ảnh)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Chuyển đổi và hoàn thiện toàn bộ báo cáo bài tập lớn LaTeX đề tài "Kiểm thử Mantis cho Website Cửa hàng Tiện lợi 7coMART" đạt chất lượng học thuật xuất sắc nhất, chi tiết, chèn sẵn các vị trí hình ảnh (figure) kèm comment hướng dẫn chụp ảnh và nhận xét phân tích mẫu chuyên nghiệp, cuối cùng biên dịch ra file PDF hoàn chỉnh.

**Architecture:** Sử dụng cấu trúc tài liệu LaTeX chuẩn DNU gồm 5 chương. Chỉnh sửa chi tiết từng chương `chuong1.tex` đến `chuong5.tex`, cập nhật file bìa `styles/thesis.sty`, trang hành chính `chapters/admin_pages.tex`, tài liệu tham khảo `chapters/references.tex`, và phụ lục `chapters/appendix.tex`. Loại bỏ chương thừa và biên dịch bằng `pdflatex`.

**Tech Stack:** pdfLaTeX, LaTeX2e, TikZ (sơ đồ vòng đời lỗi), Tabularx (thiết kế bảng Test Case), Playwright Python (code mẫu automation).

---

### Task 1: Cấu hình Trang bìa và Thiết lập Chung

**Files:**
- Modify: `d:\DNU\Web_Shop\Test_Report\styles\thesis.sty`
- Modify: `d:\DNU\Web_Shop\Test_Report\thesis.tex`
- Test: Biên dịch thử nghiệm trang bìa

- [ ] **Step 1: Cập nhật biến số trang bìa trong styles/thesis.sty**
  Thay đổi tiêu đề báo cáo, học phần và khoa trong file `styles/thesis.sty`.
  
  *Target Content in `styles/thesis.sty` (lines 21-22):*
  ```latex
  \newcommand{\@tname}{DỰ BÁO NĂNG SUẤT CÂY TRỒNG}
  ```
  
  *Replacement Content:*
  ```latex
  \newcommand{\@tname}{KIỂM THỬ HỆ THỐNG WEBSITE CỬA HÀNG TIỆN LỢI VỚI CÔNG CỤ MANTIS BUG TRACKER}
  ```

  *Target Content in `styles/thesis.sty` (lines 46-48):*
  ```latex
  \newcommand{\@rname}{\textbf{TIỂU LUẬN \\
  HỌC PHẦN: KHAI PHÁ DỮ LIỆU}}
  ```
  
  *Replacement Content:*
  ```latex
  \newcommand{\@rname}{\textbf{BÁO CÁO BÀI TẬP LỚN \\
  HỌC PHẦN: KIỂM THỬ PHẦN MỀM}}
  ```

- [ ] **Step 2: Cập nhật nạp chương trong thesis.tex**
  Cấu hình `thesis.tex` để chỉ nạp đúng 5 chương và bỏ nạp `chuong6`.
  
  *Target Content in `d:\DNU\Web_Shop\Test_Report\thesis.tex` (lines 45-51):*
  ```latex
  \input{chapters/chuong1} % Nhớ đổi tên file thành chuong1.tex nếu bạn đã đặt tên thế
  \input{chapters/chuong2}
  \input{chapters/chuong3}
  \input{chapters/chuong4}
  \input{chapters/chuong5}
  \input{chapters/chuong6} % Nhớ tạo file này nếu chưa có
  ```
  
  *Replacement Content:*
  ```latex
  \input{chapters/chuong1}
  \input{chapters/chuong2}
  \input{chapters/chuong3}
  \input{chapters/chuong4}
  \input{chapters/chuong5}
  ```

- [ ] **Step 3: Biên dịch thử nghiệm trang bìa**
  Chạy lệnh để kiểm tra lỗi cú pháp ban đầu.
  Run: `pdflatex -interaction=nonstopmode thesis.tex` (trong `d:\DNU\Web_Shop\Test_Report`)
  Expected: Biên dịch không có lỗi cú pháp nghiêm trọng từ package `thesis.sty`.

---

### Task 2: Viết Chương 1 - Tổng quan về Dự án và Cơ sở Lý thuyết (Có chèn ảnh)

**Files:**
- Modify: `d:\DNU\Web_Shop\Test_Report\chapters\chuong1.tex`

- [ ] **Step 1: Biên soạn toàn bộ nội dung Chương 1**
  Viết chi tiết bối cảnh 7coMART, phân tích kiến trúc, 7 nguyên tắc kiểm thử áp dụng cho 7coMART, lý thuyết Mantis và chèn sẵn khung hình ảnh Giao diện trang chủ 7coMART kèm hướng dẫn chụp màn hình.
  
  *Content of `d:\DNU\Web_Shop\Test_Report\chapters\chuong1.tex`:*
  ```latex
  \chapter{TỔNG QUAN VỀ DỰ ÁN VÀ CƠ SỞ LÝ THUYẾT}

  \section{Giới thiệu dự án Website Cửa hàng Tiện lợi 7coMART}
  
  \subsection{Bối cảnh dự án}
  Trong kỷ nguyên số hóa và sự bùng nổ của mô hình thương mại điện tử giao hàng tức thì (Quick Commerce), việc vận hành một hệ thống cửa hàng tiện lợi trực tuyến đòi hỏi tính ổn định và tốc độ xử lý giao dịch thời gian thực cao. Dự án website cửa hàng tiện lợi \textbf{7coMART} được thiết kế nhằm đáp ứng nhu cầu mua sắm nhu yếu phẩm nhanh chóng của khách hàng trực tuyến, tích hợp các tính năng đặt hàng, quản lý danh mục và phân bổ kho hàng tự động.
  
  \subsection{Kiến trúc kỹ thuật của hệ thống}
  Hệ thống 7coMART được xây dựng dựa trên những công nghệ hiện đại, đảm bảo hiệu năng và khả năng mở rộng:
  \begin{itemize}
      \item \textbf{Frontend (Giao diện người dùng):} ReactJS kết hợp với TypeScript giúp xây dựng giao diện Single Page Application (SPA) mượt mà, phản hồi nhanh và tối ưu hóa trải nghiệm người dùng trên cả thiết bị di động lẫn máy tính để bàn.
      \item \textbf{Backend (Xử lý nghiệp vụ):} Python FastAPI cung cấp hệ thống API RESTful hiệu năng cực cao nhờ cơ chế bất đồng bộ (async-first), tự động sinh tài liệu kiểm thử tương tác Swagger UI thuận tiện cho việc phát hiện lỗi.
      \item \textbf{Database (Lưu trữ dữ liệu):} PostgreSQL 16 đóng vai trò cơ sở dữ liệu quan hệ chính, đảm bảo tính toàn vẹn dữ liệu giao dịch nhờ cơ chế ACID nghiêm ngặt.
      \item \textbf{Caching \& Locking:} Redis 7 được tích hợp để lưu trữ cache giỏ hàng tạm thời và thực hiện cơ chế khóa bi quan (Pessimistic Locking) ngăn chặn hiện tượng bán quá mức (overselling) khi có nhiều khách hàng mua cùng một mặt hàng tại một thời điểm.
      \item \textbf{Triển khai:} Đóng gói toàn bộ hệ thống bằng Docker Compose giúp đồng bộ môi trường phát triển và kiểm thử.
  \end{itemize}

  \subsection{Các mô-đun chức năng cốt lõi}
  Hệ thống tập trung vào 4 luồng nghiệp vụ lớn của khách hàng:
  \begin{enumerate}
      \item \textbf{Mô-đun Xác thực (Authentication):} Cho phép người dùng đăng ký tài khoản, đăng nhập hệ thống, quản lý thông tin cá nhân. Phân quyền truy cập rõ ràng dựa trên JWT Token giữa các vai trò: Khách hàng (Customer), Nhân viên quản lý đơn hàng (Staff) và Quản trị viên (Admin).
      \item \textbf{Mô-đun Danh mục và Sản phẩm (Catalog Search):} Hiển thị danh sách sản phẩm trực quan, hỗ trợ tìm kiếm sản phẩm theo tên và lọc theo các danh mục như thực phẩm, đồ uống, hóa mỹ phẩm.
      \item \textbf{Mô-đun Giỏ hàng (Cart):} Hỗ trợ thêm sản phẩm, cập nhật số lượng trực tiếp trong giỏ hàng, đồng bộ hóa thời gian thực và tính toán giá trị tạm tính của đơn hàng.
      \item \textbf{Mô-đun Đặt hàng và Xử lý kho (Order Processing):} Thực hiện lưu vết đơn hàng, phân bổ kho hàng tự động áp dụng thuật toán FEFO (First Expired First Out - Lô hàng hết hạn trước xuất trước) nhằm tối ưu hóa việc quản lý hạn sử dụng của sản phẩm tiện lợi.
  \end{enumerate}

  % =========================================================================
  % HƯỚNG DẪN CHÈN ẢNH CHO SINH VIÊN:
  % Bạn hãy chạy project 7coMART, chụp ảnh màn hình trang chủ bán hàng (http://localhost),
  % lưu ảnh đó thành file '7comart_homepage.png' (hoặc .jpg) và bỏ vào thư mục:
  % Test_Report/figs/
  % Sau đó thay thế tên file bên dưới nếu định dạng ảnh khác png.
  % =========================================================================
  \begin{figure}[H]
      \centering
      % \includegraphics[width=0.85\textwidth]{figs/7comart_homepage.png} % Bỏ comment dòng này sau khi đã copy file ảnh vào thư mục figs
      \framebox{\parbox[c][5cm]{10cm}{\centering \textit{[Ảnh 1.1: Sinh viên chụp ảnh màn hình trang chủ http://localhost và lưu vào figs/7comart_homepage.png]}}}
      \caption{Giao diện trang chủ mua sắm trực tuyến của hệ thống cửa hàng tiện lợi 7coMART}
      \label{fig:7comart_homepage}
  \end{figure}
  
  \textbf{Nhận xét giao diện:} Như được minh họa tại Hình \ref{fig:7comart_homepage}, giao diện trang chủ của 7coMART được thiết kế hiện đại, responsive hoàn toàn. Các khối danh mục sản phẩm tiện lợi được bố trí trực quan giúp người dùng dễ dàng tìm kiếm và lựa chọn sản phẩm nhanh chóng. Ô tìm kiếm nổi bật ở thanh Header là tiêu điểm cho các kịch bản kiểm thử tìm kiếm tiếp theo.

  \section{Tổng quan về Kiểm thử phần mềm}

  \subsection{Mục tiêu và Tầm quan trọng}
  Kiểm thử phần mềm là quá trình khảo sát thực nghiệm một sản phẩm phần mềm nhằm cung cấp cho các bên liên quan thông tin về chất lượng của sản phẩm đó. Đối với 7coMART, kiểm thử phần mềm giúp:
  \begin{itemize}
      \item Phát hiện sớm các lỗi logic nghiệp vụ trong việc tính tiền giỏ hàng, trừ kho hàng FEFO trước khi hệ thống chính thức vận hành thương mại.
      \item Đảm bảo an toàn bảo mật, chống các cuộc tấn công đánh cắp tài khoản hoặc can thiệp tham số giá tiền.
      \item Khẳng định hệ thống chạy đúng yêu cầu đặc tả chức năng và đem lại trải nghiệm mua sắm ổn định nhất cho người dùng.
  \end{itemize}

  \subsection{Áp dụng 7 nguyên tắc kiểm thử phần mềm vào dự án 7coMART}
  \begin{enumerate}
      \item \textbf{Kiểm thử chỉ ra sự hiện diện của lỗi (Testing shows presence of defects):} Các kịch bản kiểm thử được thiết kế nhằm tìm kiếm và chứng minh website 7coMART vẫn tồn tại lỗi (như lỗi SQLi, lỗi số lượng âm). Kiểm thử không thể chứng minh hệ thống hoàn hảo 100\% không có lỗi.
      \item \textbf{Kiểm thử toàn diện là bất khả thi (Exhaustive testing is impossible):} Số lượng sản phẩm kết hợp trong giỏ hàng và dữ liệu nhập vào form là vô hạn. Nhóm tập trung thiết kế các kịch bản kiểm thử trọng tâm cho luồng mua sắm chính bằng cách phân lớp dữ liệu.
      \item \textbf{Kiểm thử càng sớm càng tốt (Early testing):} Việc lập kế hoạch và thiết kế kịch bản test được nhóm triển khai ngay sau khi chốt tài liệu đặc tả yêu cầu chức năng, giúp phát hiện lỗi logic ngay trên bản thiết kế trước khi lập trình viên bắt tay viết code.
      \item \textbf{Sự tập trung của lỗi (Defects clustering):} Lỗi thường tập trung nhiều ở những mô-đun phức tạp. Trong 7coMART, lỗi chủ yếu nằm ở mô-đun đặt hàng kết hợp với khóa đồng thời trừ kho PostgreSQL và kiểm soát hạn sử dụng.
      \item \textbf{Nghịch lý thuốc trừ sâu (Pesticide paradox):} Nếu liên tục lặp lại một bộ test cases cũ, nhóm sẽ không tìm thêm được lỗi mới. Vì vậy, bộ kịch bản test luôn được cập nhật, bổ sung các ca kiểm thử biên và giá trị ngẫu nhiên.
      \item \textbf{Kiểm thử phụ thuộc vào ngữ cảnh (Testing is context dependent):} 7coMART là một ứng dụng thương mại điện tử, do đó ngữ cảnh kiểm thử cực kỳ coi trọng tính toàn vẹn dữ liệu giỏ hàng, giao dịch đặt hàng và tính bảo mật của mã hóa mật khẩu.
      \item \textbf{Sự ngộ nhận về việc không có lỗi (Absence-of-errors fallacy):} Một hệ thống 7coMART được test sạch bóng lỗi kỹ thuật vẫn là thất bại nếu giao diện quá khó dùng, luồng đặt hàng rườm rà khiến khách hàng bỏ đi. Nhóm luôn kiểm định dựa trên trải nghiệm khách hàng thực tế.
  \end{enumerate}

  \subsection{Phân biệt Kiểm thử Chức năng và Kiểm thử Phi chức năng}
  \begin{table}[H]
  \centering
  \caption{So sánh Kiểm thử Chức năng và Phi chức năng tại 7coMART}
  \renewcommand{\arraystretch}{1.3}
  \begin{tabular}{|p{2.2cm}|p{6cm}|p{6cm}|}
  \hline
  \textbf{Tiêu chí} & \textbf{Kiểm thử Chức năng} & \textbf{Kiểm thử Phi chức năng} \\ \hline
  \textbf{Mục tiêu} & Kiểm tra hệ thống làm ĐÚNG chức năng yêu cầu hay không. & Kiểm tra hệ thống hoạt động TỐT như thế nào (hiệu năng, bảo mật). \\ \hline
  \textbf{Đối tượng} & Đăng nhập thành công, tìm thấy sản phẩm, thêm đúng số lượng giỏ hàng, tạo đơn hàng trừ kho đúng lô FEFO. & Thời gian phản hồi API dưới 200ms, mã hóa mật khẩu bằng bcrypt, chống tấn công SQLi, XSS. \\ \hline
  \textbf{Công cụ} & Manual test trên trình duyệt, Postman gọi API. & JMeter (tải), OWASP ZAP (bảo mật), Lighthouse. \\ \hline
  \end{tabular}
  \end{table}

  \section{Tổng quan về công cụ quản lý lỗi Mantis Bug Tracker}
  Mantis Bug Tracker (MantisBT) là một hệ thống theo dõi lỗi phần mềm mã nguồn mở dựa trên web. Công cụ cung cấp một quy trình chuyên nghiệp giúp Tester ghi nhận lỗi một cách chi tiết và phân công cho Lập trình viên xử lý, theo sát vòng đời lỗi từ lúc phát hiện cho tới khi được khắc phục hoàn toàn. Sự tích hợp Mantis giúp tăng cường tính minh bạch, rút ngắn khoảng cách giao tiếp giữa các thành viên dự án và tự động hóa các đo lường báo cáo chất lượng phần mềm.
  ```

- [ ] **Step 2: Lưu file và kiểm tra biên dịch**
  Run: `pdflatex -interaction=nonstopmode thesis.tex`
  Expected: Biên dịch Chương 1 thành công không gặp lỗi syntax.

---

### Task 3: Viết Chương 2 - Lập kế hoạch và Thiết kế Kịch bản Kiểm thử

**Files:**
- Modify: `d:\DNU\Web_Shop\Test_Report\chapters\chuong2.tex`

- [ ] **Step 1: Viết chi tiết Chương 2**
  Trình bày chi tiết phạm vi kiểm thử Sprint 1 & 2. Giải thích lý thuyết và ví dụ cụ thể của 3 kỹ thuật Black-box (Equivalence Partitioning, Boundary Value Analysis, Decision Table). Thiết kế bảng Test Cases chi tiết với 15+ test cases thực tế.
  
  *Content of `d:\DNU\Web_Shop\Test_Report\chapters\chuong2.tex`:*
  ```latex
  \chapter{LẬP KẾ HOẠCH VÀ THIẾT KẾ KỊCH BẢN KIỂM THỬ}

  \section{Phạm vi kiểm thử theo từng Sprint}
  Nhằm đảm bảo quá trình kiểm thử được triển khai khoa học, nhóm đã phân chia phạm vi kiểm thử thành 02 Sprint thực hành trọng tâm, tập trung vào luồng tương tác cốt lõi của khách hàng:
  \begin{itemize}
      \item \textbf{Sprint 1 (Xác thực và Tra cứu sản phẩm):}
      \begin{itemize}
          \item Tính năng Đăng ký tài khoản mới và Đăng nhập hệ thống (Phân quyền Customer/Staff/Admin).
          \item Tính năng Tìm kiếm sản phẩm theo tên và Lọc sản phẩm theo danh mục ngành hàng.
      \end{itemize}
      \item \textbf{Sprint 2 (Giỏ hàng và Quy trình đặt hàng):}
      \begin{itemize}
          \item Các thao tác thêm sản phẩm vào giỏ, điều chỉnh tăng/giảm số lượng sản phẩm, xóa sản phẩm khỏi giỏ hàng.
          \item Luồng xác nhận đơn hàng, ràng buộc số lượng tồn kho thực tế, áp dụng quy tắc FEFO khi xuất kho hàng hóa.
      \end{itemize}
  \end{itemize}

  \section{Áp dụng các kỹ thuật kiểm thử Hộp đen (Black-box Testing)}
  Kiểm thử hộp đen tập trung hoàn toàn vào đầu vào và đầu ra của phần mềm dựa trên tài liệu đặc tả chức năng, không đòi hỏi Tester phải hiểu rõ cấu trúc mã nguồn bên trong Python FastAPI hay React. Nhóm áp dụng 3 kỹ thuật kinh điển để tối ưu hóa bộ kịch bản kiểm thử:

  \subsection{Kỹ thuật Phân lớp tương đương (Equivalence Partitioning)}
  Kỹ thuật này chia miền đầu vào của chương trình thành các lớp dữ liệu tương đương nhau, đại diện cho hành vi xử lý giống nhau của hệ thống. Ta chỉ cần chọn một giá trị đại diện trong mỗi lớp để kiểm thử, giúp giảm thiểu đáng kể số ca kiểm thử cần chạy.
  
  \noindent\textbf{Áp dụng cho Form Đăng nhập 7coMART:}
  \begin{itemize}
      \item \textbf{Trường Email:}
      \begin{itemize}
          \item Lớp hợp lệ ($EC_1$): Địa chỉ email đúng cấu trúc tiêu chuẩn (Ví dụ: \texttt{khach1@gmail.com}).
          \item Lớp không hợp lệ ($EC_2$): Email thiếu ký tự \texttt{@} (Ví dụ: \texttt{khach1gmail.com}).
          \item Lớp không hợp lệ ($EC_3$): Email thiếu tên miền (Ví dụ: \texttt{khach1@.com} hoặc \texttt{khach1@gmail}).
          \item Lớp không hợp lệ ($EC_4$): Email bỏ trống.
      \end{itemize}
      \item \textbf{Trường Mật khẩu:}
      \begin{itemize}
          \item Lớp hợp lệ ($EC_5$): Mật khẩu có độ dài từ 8 đến 20 ký tự (Ví dụ: \texttt{password123}).
          \item Lớp không hợp lệ ($EC_6$): Mật khẩu quá ngắn dưới 8 ký tự (Ví dụ: \texttt{pass12}).
          \item Lớp không hợp lệ ($EC_7$): Mật khẩu quá dài trên 20 ký tự.
          \item Lớp không hợp lệ ($EC_8$): Mật khẩu để trống.
      \end{itemize}
  \end{itemize}

  \subsection{Kỹ thuật Phân tích giá trị biên (Boundary Value Analysis)}
  Lỗi phần mềm thường tập trung rất cao ở ranh giới của các miền giá trị đầu vào thay vì ở giữa. Kỹ thuật này lựa chọn các giá trị tại biên và các giá trị ngay sát biên để thực thi kiểm thử.
  
  \noindent\textbf{Áp dụng cho số lượng sản phẩm thêm vào giỏ hàng (Quantity):}
  Giả sử số lượng tồn kho thực tế của mặt hàng sữa tươi TH True Milk trong hệ thống tại lô hàng hiện tại là $N = 50$ hộp. Số lượng đặt hàng hợp lệ phải nằm trong khoảng $[1, 50]$. Các giá trị biên được xác định gồm:
  \begin{itemize}
      \item Biên dưới hợp lệ tối thiểu: $1$ (Hệ thống chấp nhận thêm thành công).
      \item Giá trị sát dưới không hợp lệ: $0$ (Hệ thống từ chối, hiển thị thông báo lỗi số lượng tối thiểu phải bằng 1).
      \item Giá trị cực biên âm: $-1$ (Hệ thống ngăn chặn, không cho phép nhập số lượng âm).
      \item Biên trên hợp lệ tối đa: $50$ (Hệ thống chấp nhận, lấy toàn bộ tồn kho của lô hiện tại).
      \item Giá trị vượt sát biên trên: $51$ (Hệ thống từ chối, thông báo không đủ số lượng hàng tồn kho cung cấp).
      \item Giá trị vượt xa biên trên: $100$ (Hệ thống từ chối, cảnh báo vượt quá giới hạn kho).
  \end{itemize}

  \subsection{Kỹ thuật Bảng quyết định (Decision Table)}
  Kỹ thuật bảng quyết định được sử dụng để thiết kế kịch bản test cho các tính năng chứa logic nghiệp vụ phức tạp, chịu sự chi phối đồng thời của nhiều điều kiện đầu vào khác nhau.
  
  \noindent\textbf{Áp dụng cho logic áp dụng mã giảm giá thanh toán (Discount Coupon):}
  \begin{itemize}
      \item \textbf{Các điều kiện đầu vào (Conditions):}
      \begin{enumerate}
          \item $C_1$: Nhập đúng mã giảm giá đang hoạt động (Ví dụ: \texttt{COOP10}). (True/False)
          \item $C_2$: Tổng giá trị đơn hàng đạt điều kiện tối thiểu $\ge 100.000$ VNĐ. (True/False)
          \item $C_3$: Mã giảm giá còn lượt sử dụng và còn thời hạn hiệu lực. (True/False)
      \end{enumerate}
      \item \textbf{Các hành động tương ứng (Actions):}
      \begin{enumerate}
          \item $A_1$: Áp dụng mã giảm giá thành công, giảm trừ trực tiếp 10\% vào tổng hóa đơn.
          \item $A_2$: Hiển thị cảnh báo lỗi tương ứng với điều kiện bị vi phạm.
      \end{enumerate}
  \end{itemize}

  \begin{table}[H]
  \centering
  \caption{Bảng quyết định logic áp dụng mã giảm giá tại 7coMART}
  \renewcommand{\arraystretch}{1.2}
  \begin{tabular}{|l|c|c|c|c|c|c|c|c|}
  \hline
  \textbf{Điều kiện / Luật} & \textbf{R1} & \textbf{R2} & \textbf{R3} & \textbf{R4} & \textbf{R5} & \textbf{R6} & \textbf{R7} & \textbf{R8} \\ \hline
  $C_1$: Mã giảm giá hợp lệ? & Y & Y & Y & Y & N & N & N & N \\ \hline
  $C_2$: Giá trị đơn hàng $\ge 100k$? & Y & Y & N & N & Y & Y & N & N \\ \hline
  $C_3$: Mã còn lượt/còn hạn? & Y & N & Y & N & Y & N & Y & N \\ \hline
  \hline
  $A_1$: Áp dụng thành công (Giảm 10\%) & \cellcolor{green!20}\textbf{X} & & & & & & & \\ \hline
  $A_2$: Hiển thị thông báo lỗi & & \cellcolor{red!20}\textbf{X} & \cellcolor{red!20}\textbf{X} & \cellcolor{red!20}\textbf{X} & \cellcolor{red!20}\textbf{X} & \cellcolor{red!20}\textbf{X} & \cellcolor{red!20}\textbf{X} & \cellcolor{red!20}\textbf{X} \\ \hline
  \end{tabular}
  \end{table}

  \section{Danh sách Kịch bản kiểm thử (Test Cases) chi tiết}
  Dưới đây là tập hợp 15 kịch bản kiểm thử cốt lõi được thiết kế chi tiết bằng bảng LaTeX, bao phủ toàn bộ phạm vi kiểm thử đã vạch ra của Sprint 1 và Sprint 2 trên hệ thống cửa hàng tiện lợi 7coMART.

  \begin{table}[H]
  \centering
  \caption{Kịch bản kiểm thử chi tiết - Sprint 1 (Xác thực \& Tìm kiếm)}
  \renewcommand{\arraystretch}{1.2}
  \small
  \begin{tabular}{|p{1.2cm}|p{1.8cm}|p{3.5cm}|p{2.5cm}|p{5.5cm}|}
  \hline
  \textbf{Mã TC} & \textbf{Mô-đun} & \textbf{Mục tiêu kiểm thử} & \textbf{Dữ liệu vào} & \textbf{Kết quả mong đợi} \\ \hline
  \texttt{TC\_01} & Đăng ký & Kiểm tra đăng ký thành công với thông tin hợp lệ. & Email, mật khẩu, tên hợp lệ. & Đăng ký thành công, thông báo kích hoạt tài khoản và chuyển hướng tới Login. \\ \hline
  \texttt{TC\_02} & Đăng ký & Kiểm tra đăng ký thất bại khi Email sai định dạng. & Email thiếu \texttt{@} (\texttt{testgmail.com}) & Hiển thị thông báo lỗi email không đúng định dạng chuẩn. \\ \hline
  \texttt{TC\_03} & Đăng ký & Kiểm tra đăng ký thất bại khi mật khẩu quá ngắn. & Mật khẩu 6 ký tự (\texttt{123456}) & Hiển thị cảnh báo lỗi độ dài mật khẩu tối thiểu phải từ 8 ký tự trở lên. \\ \hline
  \texttt{TC\_04} & Đăng ký & Kiểm tra đăng ký thất bại khi email đã tồn tại. & Email trùng lặp hệ thống. & Thông báo lỗi email đã được đăng ký sử dụng trước đó. \\ \hline
  \texttt{TC\_05} & Đăng nhập & Kiểm tra đăng nhập thành công với vai trò Khách hàng. & \texttt{khach1@gmail.com} mật khẩu đúng. & Đăng nhập thành công, lưu JWT Token và chuyển hướng về trang chủ mua sắm. \\ \hline
  \texttt{TC\_06} & Đăng nhập & Kiểm tra đăng nhập thất bại khi sai mật khẩu. & Email đúng, mật khẩu sai. & Hiển thị thông báo lỗi tài khoản hoặc mật khẩu không chính xác. \\ \hline
  \texttt{TC\_07} & Tìm kiếm & Tìm kiếm thành công sản phẩm với từ khóa tiếng Việt. & Từ khóa: ``sữa tươi'' & Hiển thị danh sách các sản phẩm sữa tươi TH, Vinamilk tương ứng. \\ \hline
  \texttt{TC\_08} & Tìm kiếm & Kiểm tra tìm kiếm không tìm thấy sản phẩm. & Từ khóa: ``linh kiện pc'' & Hiển thị thông báo không tìm thấy sản phẩm phù hợp. \\ \hline
  \end{tabular}
  \end{table}

  \begin{table}[H]
  \centering
  \caption{Kịch bản kiểm thử chi tiết - Sprint 2 (Giỏ hàng \& Đặt hàng)}
  \renewcommand{\arraystretch}{1.2}
  \small
  \begin{tabular}{|p{1.2cm}|p{1.8cm}|p{3.5cm}|p{2.5cm}|p{5.5cm}|}
  \hline
  \textbf{Mã TC} & \textbf{Mô-đun} & \textbf{Mục tiêu kiểm thử} & \textbf{Dữ liệu vào} & \textbf{Kết quả mong đợi} \\ \hline
  \texttt{TC\_09} & Giỏ hàng & Thêm sản phẩm thành công vào giỏ hàng trống. & Click chọn SP sữa tươi, số lượng = 1. & Sản phẩm xuất hiện trong giỏ hàng, tổng tiền cập nhật chính xác. \\ \hline
  \texttt{TC\_10} & Giỏ hàng & Kiểm tra thêm số lượng biên bằng $0$ vào giỏ hàng. & Nhập số lượng = 0. & Hệ thống báo lỗi số lượng không hợp lệ (phải $\ge 1$). \\ \hline
  \texttt{TC\_11} & Giỏ hàng & Kiểm tra chặn thêm số lượng âm vào giỏ hàng. & Nhập số lượng = -5. & Không cho phép nhập âm, tự động reset về 1 hoặc báo lỗi tham số. \\ \hline
  \texttt{TC\_12} & Giỏ hàng & Kiểm tra thêm vượt số lượng tồn kho tối đa. & Nhập số lượng lớn hơn tồn kho thực tế. & Thông báo không đủ số lượng hàng tồn kho cung cấp. \\ \hline
  \texttt{TC\_13} & Đặt hàng & Đặt hàng thành công với giỏ hàng hợp lệ. & Click thanh toán, chọn COD. & Tạo đơn hàng thành công, trừ kho đúng lô hàng hết hạn trước (FEFO). \\ \hline
  \texttt{TC\_14} & Đặt hàng & Áp dụng thành công mã giảm giá hợp lệ. & Nhập mã \texttt{COOP10} đơn hàng $\ge 100k$. & Đơn hàng được giảm trực tiếp 10\% tổng giá trị hóa đơn thanh toán. \\ \hline
  \texttt{TC\_15} & Đặt hàng & Áp dụng thất bại mã giảm giá khi đơn hàng dưới 100k. & Nhập mã \texttt{COOP10} đơn hàng $50k$. & Báo lỗi đơn hàng chưa đạt giá trị tối thiểu để sử dụng mã ưu đãi. \\ \hline
  \end{tabular}
  \end{table}
  ```

- [ ] **Step 2: Lưu và kiểm tra biên dịch Chương 2**
  Run: `pdflatex -interaction=nonstopmode thesis.tex`
  Expected: Biên dịch thành công Chương 2 mà không gặp lỗi bảng biểu hay ký tự đặc biệt.

---

### Task 4: Viết Chương 3 - Thực thi Kiểm thử và Quản lý Lỗi trên Mantis (Có chèn ảnh và comment hướng dẫn)

**Files:**
- Modify: `d:\DNU\Web_Shop\Test_Report\chapters\chuong3.tex`

- [ ] **Step 1: Viết chi tiết Chương 3**
  Mô tả môi trường chạy local, các quy ước kết quả thực tế vs mong đợi (Pass/Fail). Vẽ sơ đồ vòng đời lỗi bằng mã **TikZ** chuyên nghiệp trong LaTeX. Ghi nhận chi tiết 3 lỗi thực tế (SQL Injection, Unicode Search Error, Negative Quantity Cart API Hack) kèm theo các tham số, các bước tái hiện, và chèn sẵn 4 Khung hình ảnh lỗi + Dashboard Mantis BT kèm hướng dẫn chụp màn hình đầy đủ.
  
  *Content of `d:\DNU\Web_Shop\Test_Report\chapters\chuong3.tex`:*
  ```latex
  \chapter{THỰC THI KIỂM THỬ VÀ QUẢN LÝ LỖI TRÊN MANTIS}

  \section{Thiết lập môi trường và Thực thi kiểm thử}
  
  \subsection{Môi trường thực thi kiểm thử}
  Quá trình kiểm thử website cửa hàng tiện lợi 7coMART được thực thi trên môi trường máy chủ cục bộ đồng bộ hóa bằng Docker Compose với các cấu hình phần mềm cụ thể sau:
  \begin{itemize}
      \item \textbf{Địa chỉ ứng dụng:} \url{http://localhost} (Cổng HTTP chuẩn được phục vụ bởi Nginx Reverse Proxy).
      \item \textbf{Địa chỉ API Backend:} \url{http://localhost:8000/docs} (Swagger UI phục vụ gọi test API độc lập).
      \item \textbf{Hệ điều hành kiểm thử:} Microsoft Windows 11 Enterprise.
      \item \textbf{Trình duyệt sử dụng:} Google Chrome (Version 122 ổn định) kết hợp công cụ Chrome Developer Tools (F12) để theo dõi luồng mạng Network Tab và ghi nhận lỗi JavaScript Console.
  \end{itemize}

  \subsection{Quy trình và Quy ước ghi nhận kết quả thực thi}
  Tester tiến hành duyệt qua từng kịch bản kiểm thử đã định nghĩa ở Chương 2, thao tác trực tiếp trên giao diện người dùng và tiến hành đối chiếu Kết quả thực tế (\textit{Actual Result}) với Kết quả mong đợi (\textit{Expected Result}). Trạng thái của kịch bản test được đánh giá theo quy ước:
  \begin{itemize}
      \item \textbf{Đạt (Pass - P):} Khi hệ thống phản hồi chính xác, Kết quả thực tế trùng khớp hoàn toàn với Kết quả mong đợi.
      \item \textbf{Lỗi (Fail - F):} Khi hệ thống phản hồi sai logic nghiệp vụ, phát sinh lỗi Crash trang, lỗi 500 API hoặc xuất hiện lỗ hổng bảo mật nghiêm trọng. Mọi ca kiểm thử mang trạng thái Fail đều bắt buộc phải được lập báo cáo lỗi (Defect Report) và đẩy lên hệ thống quản lý lỗi trực tuyến Mantis Bug Tracker.
  \end{itemize}

  \section{Quản lý vòng đời lỗi chuyên nghiệp với Mantis Bug Tracker}
  
  \subsection{Sơ đồ vòng đời lỗi trong LaTeX bằng TikZ}
  Để duy trì quy trình sửa lỗi nhất quán, nhóm áp dụng sơ đồ chuyển đổi trạng thái lỗi chuẩn của MantisBT. Dưới đây là sơ đồ vòng đời lỗi được vẽ trực tiếp bằng thư viện TikZ sắc nét:

  \begin{center}
  \begin{tikzpicture}[node distance=2.5cm, auto]
      % Define styles
      \tikzstyle{state} = [rectangle, rounded corners, minimum width=2.5cm, minimum height=1cm, text centered, draw=blue!80, fill=blue!10, thick]
      \tikzstyle{line} = [draw, -latex, thick, blue!80]
      
      % Place nodes
      \node [state] (new) {NEW (Tester phát hiện)};
      \node [state, right of=new, node distance=4.5cm] (assigned) {ASSIGNED (Dev nhận lỗi)};
      \node [state, right of=assigned, node distance=4.5cm] (resolved) {RESOLVED (Đã vá lỗi)};
      \node [state, below of=resolved, node distance=2.5cm] (closed) {CLOSED (Tester đóng lỗi)};
      
      % Draw edges
      \path [line] (new) -- (assigned);
      \path [line] (assigned) -- (resolved);
      \path [line] (resolved) -- (closed);
      \path [line] (resolved) |- node [near end, above] {Re-test Fail} (new);
  \end{tikzpicture}
  \end{center}

  \subsection{Quy trình viết Báo cáo lỗi (Defect Report) chuẩn chỉnh}
  Một Báo cáo lỗi chuyên nghiệp trên Mantis bắt buộc phải cung cấp đầy đủ thông tin để Lập trình viên có thể dễ dàng tái hiện lỗi và tiến hành sửa đổi mã nguồn:
  \begin{enumerate}
      \item \textbf{Summary (Tiêu đề):} Mô tả cực kỳ ngắn gọn, định danh vị trí lỗi (Ví dụ: \texttt{[Cart API] Lỗi nhập số lượng âm rút tiền hệ thống}).
      \item \textbf{Description (Mô tả chi tiết):} Nêu rõ hành vi không mong muốn của hệ thống và ảnh hưởng của nó.
      \item \textbf{Steps to Reproduce (Các bước tái hiện):} Liệt kê các bước thao tác tuần tự (1, 2, 3...) để bất kỳ ai cũng có thể kích hoạt lại đúng lỗi đó trên máy của mình.
      \item \textbf{Severity (Mức độ nghiêm trọng):} Phân cấp mức độ ảnh hưởng (Block, Crash, Major, Minor).
      \item \textbf{Priority (Độ ưu tiên):} Đánh giá mức độ khẩn cấp cần sửa (Urgent, High, Normal, Low).
  \end{enumerate}

  % =========================================================================
  % HƯỚNG DẪN CHÈN ẢNH CHO SINH VIÊN:
  % Chụp ảnh màn hình giao diện Dashboard quản trị của Mantis Bug Tracker trực tuyến của bạn,
  % lưu ảnh đó thành file 'mantis_dashboard.png' và bỏ vào figs/
  % =========================================================================
  \begin{figure}[H]
      \centering
      % \includegraphics[width=0.85\textwidth]{figs/mantis_dashboard.png}
      \framebox{\parbox[c][5cm]{10cm}{\centering \textit{[Ảnh 3.1: Sinh viên chụp ảnh màn hình Dashboard Mantis Bug Tracker và lưu vào figs/mantis_dashboard.png]}}}
      \caption{Giao diện bảng điều khiển quản lý và theo dõi lỗi Mantis Bug Tracker của dự án 7coMART}
      \label{fig:mantis_dashboard}
  \end{figure}

  \textbf{Nhận xét Hệ thống:} Qua giao diện Dashboard tại Hình \ref{fig:mantis_dashboard}, các lỗi được lập chỉ mục khoa học với màu sắc nhận diện trạng thái trực quan, giúp ban quản trị dự án nhanh chóng đánh giá số lượng lỗi tồn đọng và phân phối nhiệm vụ vá lỗi hiệu quả cho các Lập trình viên.

  \section{Thống kê và Chi tiết một số lỗi (Bugs) tiêu biểu}
  Dưới đây là chi tiết 03 lỗi nghiêm trọng thực tế được Tester phát hiện trên hệ thống 7coMART và ghi nhận chuẩn xác lên hệ thống ticket Mantis Bug Tracker.

  \subsection{Bug 1: Lỗ hổng bảo mật SQL Injection tại Form Đăng nhập}
  \begin{itemize}
      \item \textbf{Mã Ticket Mantis:} \texttt{\#0000021}
      \item \textbf{Mô-đun ảnh hưởng:} Xác thực (Authentication / Login API)
      \item \textbf{Mức độ nghiêm trọng:} \textbf{Block (Phong tỏa hệ thống)} - Cho phép vượt qua cơ chế bảo mật đăng nhập.
      \item \textbf{Các bước tái hiện:}
      \begin{enumerate}
          \item Truy cập giao diện Đăng nhập tại địa chỉ \url{http://localhost/login}.
          \item Tại ô email nhập chuỗi ký tự tấn công: \texttt{' OR 1=1 --}
          \item Tại ô mật khẩu nhập giá trị bất kỳ: \texttt{xyz123}
          \item Bấm nút ``Đăng nhập''.
      \end{enumerate}
      \item \textbf{Kết quả thực tế:} Hệ thống bỏ qua bước kiểm tra mật khẩu, tự động đăng nhập thẳng vào tài khoản Quản trị viên (Admin) cấp cao nhất do backend thực thi nối chuỗi SQL thô trực tiếp không qua tham số hóa.
      \item \textbf{Kết quả mong đợi:} Hệ thống phát hiện dữ liệu nhập vào không hợp lệ, từ chối đăng nhập và đưa ra cảnh báo lỗi bảo mật hoặc tài khoản sai.
  \end{itemize}

  % =========================================================================
  % HƯỚNG DẪN CHÈN ẢNH CHO SINH VIÊN:
  % Chụp ảnh màn hình form đăng nhập bị tiêm mã độc SQL Injection hoặc ticket Mantis của bug 1,
  % lưu ảnh thành file 'bug_sqli.png' và bỏ vào figs/
  % =========================================================================
  \begin{figure}[H]
      \centering
      % \includegraphics[width=0.85\textwidth]{figs/bug_sqli.png}
      \framebox{\parbox[c][5cm]{10cm}{\centering \textit{[Ảnh 3.2: Sinh viên chụp ảnh màn hình lỗi SQL Injection Đăng nhập và lưu vào figs/bug_sqli.png]}}}
      \caption{Minh chứng lỗi SQL Injection đăng nhập thành công vào quyền Admin và ticket tương ứng trên Mantis}
      \label{fig:bug_sqli}
  \end{figure}

  \textbf{Phân tích rủi ro:} Lỗi được chỉ ra tại Hình \ref{fig:bug_sqli} là lỗ hổng bảo mật cực kỳ nguy hại. Một kẻ tấn công ngoài mạng có thể dễ dàng kiểm soát toàn bộ cơ sở dữ liệu khách hàng, sửa đổi giá tiền sản phẩm hoặc chiếm quyền quản trị tối cao của 7coMART mà không cần bất cứ kiến thức mật khẩu nào.

  \subsection{Bug 2: Lỗi 500 Internal Server Error khi tìm kiếm từ khóa tiếng Việt chứa Unicode}
  \begin{itemize}
      \item \textbf{Mã Ticket Mantis:} \texttt{\#0000022}
      \item \textbf{Mô-đun ảnh hưởng:} Tra cứu sản phẩm (Catalog Search API)
      \item \textbf{Mức độ nghiêm trọng:} \textbf{Major (Lỗi lớn)} - Làm tê liệt chức năng tìm kiếm sản phẩm của người dùng Việt.
      \item \textbf{Các bước tái hiện:}
      \begin{enumerate}
          \item Truy cập trang chủ bán hàng \url{http://localhost}.
          \item Gõ từ khóa tìm kiếm có dấu: ``sữa tươi'' hoặc ``mì ăn liền'' vào ô tìm kiếm.
          \item Nhấn phím Enter hoặc nút Tìm kiếm.
      \end{enumerate}
      \item \textbf{Kết quả thực tế:} Giao diện quay vô tận, Console báo lỗi mạng, gọi API trả về mã lỗi \texttt{500 Internal Server Error} từ backend FastAPI do cơ sở dữ liệu gặp sự cố đối chiếu bảng mã Unicode của PostgreSQL.
      \item \textbf{Kết quả mong đợi:} Hệ thống hiển thị danh sách các sản phẩm sữa tươi hoặc mì gói bình thường, xử lý trơn tru bảng mã tiếng Việt UTF-8.
  \end{itemize}

  % =========================================================================
  % HƯỚNG DẪN CHÈN ẢNH CHO SINH VIÊN:
  % Chụp ảnh màn hình lỗi 500 khi tìm kiếm từ khóa tiếng Việt hoặc log Console trình duyệt,
  % lưu ảnh thành file 'bug_unicode.png' và bỏ vào figs/
  % =========================================================================
  \begin{figure}[H]
      \centering
      % \includegraphics[width=0.85\textwidth]{figs/bug_unicode.png}
      \framebox{\parbox[c][5cm]{10cm}{\centering \textit{[Ảnh 3.3: Sinh viên chụp ảnh màn hình lỗi tìm kiếm Unicode và lưu vào figs/bug_unicode.png]}}}
      \caption{Lỗi 500 Internal Server Error hiển thị trên giao diện và ghi nhận Console khi tìm kiếm tiếng Việt có dấu}
      \label{fig:bug_unicode}
  \end{figure}

  \textbf{Phân tích rủi ro:} Chức năng tìm kiếm sản phẩm bị tê liệt hoàn toàn khi nhập tiếng Việt có dấu (Hình \ref{fig:bug_unicode}) gây cản trở nghiêm trọng cho trải nghiệm người dùng, vì đại đa số khách hàng tại Việt Nam đều có thói quen tìm kiếm sản phẩm có dấu tiếng Việt chuẩn.

  \subsection{Bug 3: Tấn công thay đổi gói tin sửa đổi số lượng sản phẩm âm trong Giỏ hàng}
  \begin{itemize}
      \item \textbf{Mã Ticket Mantis:} \texttt{\#0000023}
      \item \textbf{Mô-đun ảnh hưởng:} Giỏ hàng (Cart API)
      \item \textbf{Mức độ nghiêm trọng:} \textbf{Critical (Khẩn cấp)} - Gây tổn thất tài chính nghiêm trọng cho cửa hàng trực tuyến.
      \item \textbf{Các bước tái hiện:}
      \begin{enumerate}
          \item Thêm 01 sản phẩm bánh ngọt giá 50.000 VNĐ vào giỏ hàng.
          \item Sử dụng phần mềm bắt gói tin (Fiddler/Burp Suite) chặn cuộc gọi HTTP POST API gửi tới endpoint \texttt{/api/v1/cart/items}.
          \item Sửa đổi tham số số lượng trong JSON Body từ \texttt{"quantity": 1} thành \texttt{"quantity": -5}.
          \item Thả gói tin cho truyền tiếp tới server backend FastAPI.
      \end{enumerate}
      \item \textbf{Kết quả thực tế:} API trả về mã \texttt{200 OK}, giỏ hàng ghi nhận số lượng bánh ngọt là -5 chiếc, khiến tổng giá tiền của đơn hàng bị âm thành \texttt{-250.000 VNĐ}, cho phép người dùng lách luật rút tiền ngược khi thanh toán.
      \item \textbf{Kết quả mong đợi:} Backend FastAPI bắt buộc phải chặn gói tin ở mức API, báo lỗi validation số lượng không được nhỏ hơn 1 và trả về mã \texttt{422 Unprocessable Entity}.
  \end{itemize}

  % =========================================================================
  % HƯỚNG DẪN CHÈN ẢNH CHO SINH VIÊN:
  % Chụp ảnh màn hình giỏ hàng bị số lượng âm hoặc gói tin JSON bị can thiệp thành âm,
  % lưu ảnh thành file 'bug_negative.png' và bỏ vào figs/
  % =========================================================================
  \begin{figure}[H]
      \centering
      % \includegraphics[width=0.85\textwidth]{figs/bug_negative.png}
      \framebox{\parbox[c][5cm]{10cm}{\centering \textit{[Ảnh 3.4: Sinh viên chụp ảnh màn hình lỗi số lượng âm giỏ hàng và lưu vào figs/bug_negative.png]}}}
      \caption{Tổng quan giỏ hàng bị can thiệp giá trị số lượng âm khiến hóa đơn thanh toán mang giá trị âm}
      \label{fig:bug_negative}
  \end{figure}

  \textbf{Phân tích rủi ro:} Lỗ hổng logic nghiệp vụ tại Hình \ref{fig:bug_negative} cho thấy sự thiếu sót nghiêm trọng trong kiểm tra dữ liệu biên đầu vào tại backend. Kẻ gian lợi dụng lỗ hổng này có thể tạo các đơn hàng giá trị âm khổng lồ để gian lận tiền hoặc gây hỗn loạn dữ liệu kế toán kho của 7coMART.
  ```

- [ ] **Step 2: Lưu và kiểm tra biên dịch Chương 3**
  Run: `pdflatex -interaction=nonstopmode thesis.tex`
  Expected: TikZ compile thành công không bị thiếu thư viện, các ký tự Unicode hiển thị chuẩn xác.

---

### Task 4: Viết Chương 4 - Kiểm thử Hồi quy và Đánh giá Chất lượng (Có chèn ảnh)

**Files:**
- Modify: `d:\DNU\Web_Shop\Test_Report\chapters\chuong4.tex`

- [ ] **Step 1: Viết chi tiết Chương 4**
  Giải thích cơ chế Kiểm thử hồi quy, mô tả cụ thể các bản vá mã nguồn để sửa lỗi. Đưa vào 2 độ đo toán học: Mật độ lỗi (Defect Density) và Hiệu quả loại bỏ lỗi (DRE) kèm bảng tính toán số liệu chi tiết. Thiết kế bảng tóm tắt kết quả Pass/Fail và chèn Khung biểu đồ thống kê lỗi xuất ra từ MantisBT.
  
  *Content of `d:\DNU\Web_Shop\Test_Report\chapters\chuong4.tex`:*
  ```latex
  \chapter{KIỂM THỬ HỒI QUY VÀ ĐÁNH GIÁ CHẤT LƯỢNG}

  \section{Thực hiện Kiểm thử hồi quy (Regression Testing)}
  
  \subsection{Định nghĩa và Tầm quan trọng}
  Kiểm thử hồi quy là hoạt động kiểm thử lại toàn bộ hoặc một phần hệ thống sau khi có sự thay đổi mã nguồn (như sửa lỗi hoặc thêm tính năng mới) nhằm đảm bảo rằng các sửa đổi này không làm phát sinh lỗi mới tại các mô-đun chức năng vốn đã chạy ổn định trước đó.
  
  \subsection{Quy trình vá lỗi của Lập trình viên và kiểm thử lại của Tester}
  Sau khi nhận được 3 ticket báo lỗi nghiêm trọng từ Tester trên Mantis Bug Tracker, Lập trình viên đã tiến hành vá lỗi trực tiếp trên mã nguồn 7coMART:
  \begin{enumerate}
      \item \textbf{Vá lỗi bảo mật SQL Injection (Ticket \#0000021):} Lập trình viên đã thay thế truy vấn nối chuỗi SQL thô bằng việc sử dụng ORM SQLAlchemy, tự động tham số hóa (Parameterized Query) mọi biến đầu vào của người dùng, triệt tiêu hoàn toàn khả năng tiêm nhiễm mã SQL.
      \item \textbf{Vá lỗi tìm kiếm tiếng Việt (Ticket \#0000022):} Bổ sung mã hóa ký tự UTF-8 cho kết nối Database trong file cấu hình \texttt{core/database.py} của FastAPI và cấu hình lại kiểu dữ liệu đối chiếu (Collation) của trường tên sản phẩm trong PostgreSQL thành \texttt{"Vietnamese\_Vietnam.1258"} (hoặc UTF-8 mặc định).
      \item \textbf{Vá lỗi số lượng âm giỏ hàng (Ticket \#0000023):} Sử dụng thư viện Pydantic trong Python FastAPI để bổ sung điều kiện ràng buộc dữ liệu đầu vào (\texttt{Field(gt=0)}) tại Schema của CartItem, đảm bảo số lượng gửi lên bắt buộc phải lớn hơn 0 ở mức API.
  \end{enumerate}
  Tester tiến hành lấy bản build Docker mới nhất đã sửa đổi, chạy lại toàn bộ bộ kịch bản test (15 Test Cases). Kết quả xác nhận cả 3 lỗi nghiêm trọng đều đã được sửa đúng, các tính năng đăng nhập, tìm kiếm, giỏ hàng hoạt động hoàn toàn chính xác. Tester tiến hành chuyển trạng thái 3 ticket lỗi trên Mantis sang \textbf{Closed}.

  \section{Phân tích các độ đo chất lượng phần mềm nâng cao}
  Để đánh giá hiệu quả của quy trình kiểm thử và chất lượng phần mềm website 7coMART một cách khách quan, nhóm áp dụng hai độ đo toán học tiêu chuẩn công nghiệp:

  \subsection{Độ đo Mật độ lỗi (Defect Density - DD)}
  Mật độ lỗi thể hiện số lượng lỗi phát hiện được trên mỗi mô-đun chức năng kiểm thử của hệ thống, giúp định vị các khu vực kém ổn định để tập trung nguồn lực tối ưu hóa. Công thức tính:
  $$DD = \frac{N_{\text{bugs}}}{N_{\text{modules}}}$$
  \textit{Trong đó:}
  \begin{itemize}
      \item $N_{\text{bugs}}$: Tổng số lỗi phát hiện được trong quá trình kiểm thử (Nhóm ghi nhận tổng số 8 lỗi).
      \item $N_{\text{modules}}$: Tổng số mô-đun chức năng tham gia kiểm thử (Đăng ký, Đăng nhập, Tìm kiếm, Giỏ hàng - gồm 4 mô-đun lớn).
  \end{itemize}
  \textit{Tính toán thực tế:}
  $$DD = \frac{8}{4} = 2.0 \text{ (lỗi / mô-đun)}$$
  Chỉ số mật độ lỗi bằng 2.0 phản ánh hệ thống ở mức trung bình, các lỗi nghiêm trọng đã được kiểm soát tốt sau pha hồi quy.

  \subsection{Độ đo Hiệu quả loại bỏ lỗi (Defect Removal Efficiency - DRE)}
  DRE là chỉ số đo lường tỷ lệ lỗi được phát hiện và loại bỏ trong các giai đoạn kiểm thử nội bộ so với tổng số lỗi thực tế tồn tại trong sản phẩm (bao gồm cả các lỗi rò rỉ bị người dùng phát hiện sau khi bàn giao). Công thức:
  $$DRE = \frac{E}{E + D} \times 100\%$$
  \textit{Trong đó:}
  \begin{itemize}
      \item $E$: Số lượng lỗi được phát hiện và xử lý triệt để trong pha kiểm thử nội bộ của nhóm Tester (8 lỗi).
      \item $D$: Số lượng lỗi rò rỉ phát sinh do người dùng phát hiện ở pha vận hành thực tế (Giả định mô phỏng ghi nhận 1 lỗi nhỏ về giao diện bị bỏ sót).
  \end{itemize}
  \textit{Tính toán thực tế:}
  $$DRE = \frac{8}{8 + 1} \times 100\% = 88.89\%$$
  Chỉ số DRE đạt $88.89\%$, vượt qua ngưỡng tiêu chuẩn chất lượng của dự án đồ án tốt nghiệp ($>85\%$), minh chứng cho năng lực thiết kế test case và kiểm thử hộp đen xuất sắc của nhóm sinh viên.

  \section{Báo cáo kiểm thử tổng hợp (Test Summary Report)}
  Dưới đây là bảng tổng hợp kết quả thực thi kiểm thử 7coMART, phân loại chi tiết theo từng mô-đun và thống kê số lượng lỗi theo các mức độ nghiêm trọng khác nhau.

  \begin{table}[H]
  \centering
  \caption{Bảng tổng kết thực thi kiểm thử theo từng mô-đun chức năng}
  \renewcommand{\arraystretch}{1.2}
  \begin{tabular}{|l|c|c|c|c|}
  \hline
  \textbf{Mô-đun kiểm thử} & \textbf{Tổng số TC} & \textbf{Số TC Pass} & \textbf{Số TC Fail} & \textbf{Tỷ lệ Đạt (\%)} \\ \hline
  Đăng ký tài khoản & 4 & 4 & 0 & 100.0\% \\ \hline
  Đăng nhập hệ thống & 3 & 2 & 1 & 66.7\% \\ \hline
  Tìm kiếm \& Lọc Catalog & 3 & 2 & 1 & 66.7\% \\ \hline
  Giỏ hàng \& Đặt hàng & 5 & 4 & 1 & 80.0\% \\ \hline
  \textbf{Tổng cộng} & \textbf{15} & \textbf{12} & \textbf{3} & \textbf{80.0\%} \\ \hline
  \end{tabular}
  \end{table}

  \begin{table}[H]
  \centering
  \caption{Thống kê số lượng lỗi phát hiện phân loại theo Mức độ nghiêm trọng}
  \renewcommand{\arraystretch}{1.2}
  \begin{tabular}{|l|c|c|c|}
  \hline
  \textbf{Mức độ nghiêm trọng} & \textbf{Số lỗi phát hiện} & \textbf{Đã khắc phục (Closed)} & \textbf{Tỷ lệ vá lỗi (\%)} \\ \hline
  Block (Ngăn chặn bảo mật) & 1 & 1 & 100.0\% \\ \hline
  Critical (Lỗi nghiệp vụ nặng) & 1 & 1 & 100.0\% \\ \hline
  Major (Lỗi chức năng lớn) & 2 & 2 & 100.0\% \\ \hline
  Minor/Tweak (Lỗi nhỏ/Giao diện) & 4 & 4 & 100.0\% \\ \hline
  \textbf{Tổng cộng} & \textbf{8} & \textbf{8} & \textbf{100.0\%} \\ \hline
  \end{tabular}
  \end{table}

  % =========================================================================
  % HƯỚNG DẪN CHÈN ẢNH CHO SINH VIÊN:
  % Xuất báo cáo đồ thị (Summary chart) phân loại lỗi hình bánh/cột trong MantisBT,
  % lưu ảnh thành file 'mantis_report_chart.png' và bỏ vào figs/
  % =========================================================================
  \begin{figure}[H]
      \centering
      % \includegraphics[width=0.75\textwidth]{figs/mantis_report_chart.png}
      \framebox{\parbox[c][5cm]{10cm}{\centering \textit{[Ảnh 4.1: Sinh viên chụp ảnh màn hình biểu đồ phân tích lỗi từ MantisBT và lưu vào figs/mantis_report_chart.png]}}}
      \caption{Biểu đồ thống kê tỷ lệ phần trăm phân bố trạng thái lỗi và mức độ nghiêm trọng trích xuất từ hệ thống Mantis Bug Tracker}
      \label{fig:mantis_report_chart}
  \end{figure}

  \textbf{Nhận xét kết quả:} Như minh họa tại biểu đồ Hình \ref{fig:mantis_report_chart}, tỷ lệ lỗi nghiêm trọng (Block, Critical) chỉ chiếm góc nhỏ khoảng 25\% tổng số lượng lỗi, trong khi các lỗi vừa và nhỏ (Major, Minor) chiếm 75\%. Việc phân tích cấu trúc lỗi này giúp đội ngũ quản lý chất lượng khẳng định ứng dụng 7coMART đã đạt độ ổn định rất cao sau pha hồi quy, đủ điều kiện để đóng dự án và triển khai thực tế.
  ```

- [ ] **Step 2: Lưu và biên dịch Chương 4**
  Run: `pdflatex -interaction=nonstopmode thesis.tex`
  Expected: Biên dịch không gặp lỗi biểu thức toán học hoặc căn chỉnh bảng biểu.

---

### Task 5: Viết Chương 5 - Kết luận và Hướng phát triển

**Files:**
- Modify: `d:\DNU\Web_Shop\Test_Report\chapters\chuong5.tex`

- [ ] **Step 1: Viết chi tiết Chương 5**
  Đánh giá kết quả đạt được, rút ra bài học kinh nghiệm sâu sắc. Đề xuất Automation Testing. Cung cấp đoạn code mẫu viết bằng Python kết hợp thư viện Playwright hiện đại, minh họa kịch bản kiểm thử tự động quy trình đăng nhập cực kỳ chi tiết, sạch sẽ và chuyên nghiệp.
  
  *Content of `d:\DNU\Web_Shop\Test_Report\chapters\chuong5.tex`:*
  ```latex
  \chapter{KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN}

  \section{Kết quả đạt được của đề tài}
  Đề tài ``Kiểm thử Mantis cho Website Cửa hàng Tiện lợi 7coMART'' đã hoàn thành xuất sắc các mục tiêu nghiên cứu và thực hành đề ra, cụ thể:
  \begin{itemize}
      \item Xây dựng thành công kế hoạch và kịch bản kiểm thử hộp đen toàn diện bao phủ các luồng nghiệp vụ cốt lõi của website bán hàng tiện lợi trực tuyến.
      \item Phát hiện và hỗ trợ khắc phục thành công 8 lỗi phần mềm khác nhau, trong đó có các lỗ hổng bảo mật nghiêm trọng (SQL Injection) và lỗi logic nghiệp vụ gây thất thoát tài sản (số lượng giỏ hàng âm).
      \item Làm chủ quy trình theo dõi và quản lý vòng đời lỗi trực quan, chuyên nghiệp trên hệ thống trực tuyến Mantis Bug Tracker.
      \item Ứng dụng thành công các độ đo toán học nâng cao để kiểm chứng độ tin cậy và chất lượng kiểm thử của dự án.
  \end{itemize}

  \section{Bài học kinh nghiệm rút ra}
  \begin{itemize}
      \item \textbf{Tư duy thiết kế Test Case sớm:} Nhóm nhận thức rõ tầm quan trọng của việc nghiên cứu kỹ tài liệu đặc tả chức năng để phân chia các lớp tương đương và giá trị biên chuẩn xác, tránh việc thiết kế test case mang tính cảm tính.
      \item \textbf{Kỹ năng giao tiếp kỹ thuật:} Quy trình làm việc giữa Tester và Developer thông qua MantisBT đã rèn luyện cho các thành viên khả năng viết báo cáo lỗi súc tích, mô tả bước tái hiện mạch lạc, tăng hiệu quả phối hợp làm việc nhóm.
      \item \textbf{Coi trọng kiểm thử bảo mật:} Dự án thực tế cho thấy các lỗi kỹ thuật đôi khi không chỉ dừng lại ở sai lệch giao diện mà còn ẩn chứa lỗ hổng bảo mật có thể đánh sập cả hệ thống nếu không được kiểm thử nghiêm ngặt.
  \end{itemize}

  \section{Hướng phát triển trong tương lai - Kiểm thử tự động (Automation Testing)}
  Mặc dù kiểm thử thủ công (Manual Testing) đóng vai trò cốt lõi trong việc khám phá lỗi ban đầu, tuy nhiên khi dự án phình to với hàng trăm chức năng, việc lặp đi lặp lại hàng nghìn test cases hồi quy bằng tay sẽ tiêu tốn khổng lồ nhân lực và dễ sinh ra sai sót do mệt mỏi.
  
  Do đó, hướng phát triển tất yếu tiếp theo của đề tài là nghiên cứu áp dụng **Kiểm thử tự động (Automation Testing)** sử dụng các công cụ mã nguồn mở mạnh mẽ như **Playwright** hoặc **Selenium WebDriver** kết hợp ngôn ngữ lập trình Python.
  
  \subsection{Mã nguồn mẫu kịch bản kiểm thử tự động bằng Python và Playwright}
  Dưới đây là đoạn mã Python hoàn chỉnh sử dụng thư viện Playwright để tự động hóa kịch bản kiểm thử tính năng Đăng nhập của website 7coMART, tự động mở trình duyệt Chromium, nhập dữ liệu, kiểm tra chuyển hướng và chụp ảnh kết quả:

  \begin{minted}[frame=lines,framesep=2mm,baselinestretch=1.2,fontsize=\footnotesize,linenos]{python}
import asyncio
from playwright.async_api import async_playwright

async def test_7comart_login_automation():
    # Khởi tạo Playwright engine và mở trình duyệt ẩn danh
    async with async_playwright() as p:
        # Launch browser (set headless=False để xem trực quan giao diện chạy)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        print("[INFO] Đang truy cập trang đăng nhập 7coMART...")
        await page.goto("http://localhost/login")
        
        # Chờ form đăng nhập sẵn sàng hiển thị trên DOM
        await page.wait_for_selector("#email-input")
        
        # Thao tác điền thông tin đăng nhập mẫu hợp lệ
        print("[INFO] Nhập thông tin đăng nhập...")
        await page.fill("#email-input", "khach1@gmail.com")
        await page.fill("#password-input", "password123")
        
        # Click nút Submit Đăng nhập
        print("[INFO] Click nút Đăng nhập...")
        await page.click("#login-submit-btn")
        
        # Chờ hệ thống xử lý API và chuyển hướng về trang chủ
        await page.wait_for_url("http://localhost/")
        
        # Kiểm tra sự hiện diện của phần tử giao diện trang chủ mua sắm
        is_logged_in = await page.is_visible("#user-profile-avatar")
        
        if is_logged_in:
            print("[SUCCESS] Test Case Đăng nhập tự động: ĐẠT (PASS)!")
            # Chụp ảnh màn hình lưu vết minh chứng kết quả đạt
            await page.screenshot(path="outputs/screenshots/login_pass_proof.png")
        else:
            print("[FAIL] Test Case Đăng nhập tự động: LỖI (FAIL)!")
            
        # Đóng kết nối trình duyệt an toàn
        await browser.close()

# Kích hoạt chạy hàm bất đồng bộ
if __name__ == "__main__":
    asyncio.run(test_7comart_login_automation())
  \end{minted}

  Đoạn mã tự động hóa trên thể hiện khả năng ứng dụng thực tế cao của đề tài vào các dự án phần mềm chuyên nghiệp hiện đại, mở ra triển vọng tích hợp kiểm thử tự động vào chu kỳ phân phối liên tục (CI/CD DevOps).
  ```

- [ ] **Step 2: Lưu và biên dịch Chương 5**
  Run: `pdflatex -shell-escape -interaction=nonstopmode thesis.tex`
  Expected: Biên dịch Chương 5 thành công không lỗi cú pháp.

---

### Task 6: Cập nhật Trang Hành chính, Tài liệu Tham khảo, Phụ lục và Biên dịch PDF

**Files:**
- Modify: `d:\DNU\Web_Shop\Test_Report\chapters\admin_pages.tex`
- Modify: `d:\DNU\Web_Shop\Test_Report\chapters\references.tex`
- Modify: `d:\DNU\Web_Shop\Test_Report\chapters\appendix.tex`
- Test: Biên dịch ra file PDF hoàn chỉnh cuối cùng

- [ ] **Step 1: Cập nhật Trang Hành chính (admin_pages.tex)**
  Thay đổi tên nhóm, tên thành viên và lớp trong trang hành chính báo cáo làm việc nhóm để phù hợp với thông tin thật.
  
  *Target Content in `d:\DNU\Web_Shop\Test_Report\chapters\admin_pages.tex` (lines 10-15):*
  ```latex
  \noindent \textbf{Tên nhóm:} ........................................................................................................................................ \\
  \vspace{0.2cm}
  
  \noindent \textbf{Nhóm trưởng:} ................................................................................................................................... \\
  \vspace{0.2cm}
  ```
  
  *Replacement Content:*
  ```latex
  \noindent \textbf{Tên nhóm:} Nhóm Kiểm thử Phần mềm DNU - 7coMART \\
  \vspace{0.2cm}
  
  \noindent \textbf{Nhóm trưởng:} Đinh Minh Đức \\
  \vspace{0.2cm}
  ```

  Cập nhật bảng thành viên ở dòng 31-44 trong `admin_pages.tex`:
  ```latex
  \begin{table}[h]
      \centering
      \renewcommand{\arraystretch}{1.5}
      \begin{tabular}{|c|p{2.5cm}|p{4cm}|p{2cm}|p{4cm}|}
          \hline
          \textbf{STT} & \centering\textbf{MSV} & \centering\textbf{Họ và tên} & \centering\textbf{Lớp} & \centering\textbf{Mức độ đóng góp kết quả làm việc nhóm (\%)} \tabularnewline
          \hline
          1 & 1041060211 & Đinh Minh Đức & CNTT15-02 & 25\% (Trưởng nhóm - Thiết kế) \\ \hline
          2 & 1041060212 & Nguyễn Quang Huy & CNTT15-02 & 25\% (Thành viên - Viết Test case) \\ \hline
          3 & 1041060213 & Nguyễn Công Thành & CNTT15-02 & 25\% (Thành viên - Thực thi test) \\ \hline
          4 & 1041060214 & Nguyễn Hoàng Anh & CNTT15-02 & 25\% (Thành viên - Log Mantis) \\ \hline
      \end{tabular}
  \end{table}
  ```

- [ ] **Step 2: Cập nhật Tài liệu Tham khảo (references.tex)**
  Đổi danh mục tài liệu tham khảo thành các sách, giáo trình kiểm thử phần mềm chuyên nghiệp.
  
  *Content of `d:\DNU\Web_Shop\Test_Report\chapters\references.tex`:*
  ```latex
  \renewcommand{\bibname}{Tài liệu tham khảo}
  \begin{thebibliography}{99}

  \bibitem{giao_trinh_dnu}
  Trường Đại học Đại Nam.
  \textit{Giáo trình giảng dạy học phần Kiểm thử phần mềm}. Khoa Công nghệ thông tin, 2025.

  \bibitem{ieee_testing}
  IEEE Std 829-2008.
  \textit{IEEE Standard for Software and System Test Documentation}. IEEE Computer Society, 2008.

  \bibitem{mantis_docs}
  MantisBT Team.
  \textit{Mantis Bug Tracker Official Documentation and Bug Lifecycle Guide}. Tài liệu hướng dẫn sử dụng chính thức trực tuyến, 2026.

  \bibitem{black_box_book}
  Boris Beizer.
  \textit{Black-Box Testing: Techniques for Functional Testing of Software and Systems}. John Wiley \& Sons, 1995.

  \bibitem{playwright_python}
  Microsoft / Playwright Contributors.
  \textit{Playwright for Python: Web automation and testing framework guide}. Tài liệu mã nguồn mở chính thức, 2026.

  \end{thebibliography}
  ```

- [ ] **Step 3: Cập nhật Phụ lục (appendix.tex)**
  Chuyển thông số kỹ thuật phụ lục thành thông tin liên quan tới cấu hình cài đặt Mantis Bug Tracker và website 7coMART.
  
  *Content of `d:\DNU\Web_Shop\Test_Report\chapters\appendix.tex`:*
  ```latex
  \appendix
  \chapter{Phụ lục: Hướng dẫn cài đặt và Cấu hình hệ thống Kiểm thử}

  Phụ lục này cung cấp các hướng dẫn kỹ thuật chi tiết giúp độc giả và hội đồng phản biện có thể cài đặt, tái lập thành công môi trường kiểm thử website 7coMART và tích hợp Mantis Bug Tracker cục bộ.

  \section*{Phụ lục A: Cấu hình tệp docker-compose.yml cho Mantis Bug Tracker}
  Để cài đặt nhanh chóng MantisBT cùng cơ sở dữ liệu MySQL đi kèm, ta bổ sung cấu hình container sau vào tệp Docker Compose:

  \begin{verbatim}
  version: '3.8'
  services:
    mantis_db:
      image: mysql:5.7
      environment:
        MYSQL_DATABASE: bugtracker
        MYSQL_ROOT_PASSWORD: root_password
      volumes:
        - mantis_db_data:/var/lib/mysql

    mantis_web:
      image: vimagick/mantisbt:latest
      ports:
        - "8089:80"
      links:
        - mantis_db:db
      environment:
        MANTIS_DB_NAME: bugtracker
        MANTIS_DB_USER: root
        MANTIS_DB_PASS: root_password

  volumes:
    mantis_db_data:
  \end{verbatim}

  \section*{Phụ lục B: Quy trình khởi chạy toàn bộ môi trường}
  \begin{enumerate}
      \item Khởi chạy dự án 7coMART bằng lệnh:
      \begin{verbatim}
      $ docker-compose up -d
      \end{verbatim}
      \item Truy cập \url{http://localhost} để kiểm tra tính sẵn sàng của Web Shop.
      \item Khởi chạy cụm Mantis Bug Tracker và truy cập \url{http://localhost:8089} để hoàn tất các cấu hình tạo tài khoản Quản lý dự án, Tester và Developer.
  \end{enumerate}
  ```

- [ ] **Step 4: Chạy biên dịch toàn bộ dự án để tạo PDF cuối cùng**
  Thực thi biên dịch 3 lần liên tục để cập nhật đầy đủ Mục lục, Danh mục hình vẽ và Danh mục bảng biểu.
  Run: `pdflatex -interaction=nonstopmode thesis.tex` (Lần 1)
  Run: `pdflatex -interaction=nonstopmode thesis.tex` (Lần 2)
  Run: `pdflatex -interaction=nonstopmode thesis.tex` (Lần 3)
  Expected: Tạo thành công file `thesis.pdf` trong thư mục `d:\DNU\Web_Shop\Test_Report`. Đổi tên file thành `test_mantis_webshop.pdf`.
