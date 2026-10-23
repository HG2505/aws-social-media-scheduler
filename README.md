# 🚀 AWS Cloud Social Media Scheduler

> **Nền tảng Quản lý & Tự động Lên lịch Đăng bài Mạng xã hội trên nền tảng AWS Cloud Serverless kết hợp AI Copilot.**

[![AWS](https://img.shields.io/badge/AWS-Cloud-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)](https://aws.amazon.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-8E75C2?style=for-the-badge&logo=googlegemini&logoColor=white)](https://aistudio.google.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

---

## 🌟 Tổng quan Dự án

**AWS Cloud Social Media Scheduler** là ứng dụng Full-Stack hỗ trợ người sáng tạo nội dung và doanh nghiệp:
1. **Soạn thảo & Sáng tạo với AI Copilot**: Tích hợp Google Gemini (`gemini-3.5-flash-lite`) tự động tạo bài viết, gợi ý hashtag và tùy biến phong cách (Chuyên nghiệp, Hài hước, Truyền cảm hứng).
2. **Lưu trữ Media Đám mây (Amazon S3)**: Tải lên hình ảnh/video trực tiếp lên AWS S3 Bucket với chính sách CORS mở rộng.
3. **Động cơ Lên lịch Không Máy chủ (Serverless Scheduler)**: Sử dụng **AWS EventBridge Scheduler** phối hợp cùng **AWS Lambda** để tự động kích hoạt xuất bản bài viết chính xác tới từng giây khi đến lịch hẹn mà không cần server chạy ngầm.
4. **Tối ưu hóa Chi phí ($0 Budget Guardrail)**: 100% tài nguyên được thiết kế nằm gọn trong hạn mức **AWS Free Tier** kết hợp **AWS Budgets Alert** cảnh báo tự động.

---

## 🏗️ Kiến trúc Hệ thống (Architecture)

```
[ Người dùng / Trình duyệt ]
             │
             ▼
[ Frontend: React + Vite + Tailwind CSS ]
             │
             ▼ (RESTful API / JSON)
[ Backend: FastAPI (Python 3.12) ]
     │                │                 │
     ▼                ▼                 ▼
[ SQLite / RDS ] [ AWS S3 Media ] [ Google Gemini AI ]
(Database lưu    (Lưu trữ hình    (Sinh Caption & Hashtags)
 bài viết)        ảnh/video)
                      │
                      ▼
       [ AWS EventBridge Scheduler ]
                      │ (Kích hoạt khi đến giờ hẹn)
                      ▼
          [ AWS Lambda Function ]
             (PublishPostFunction)
```

---

## 🛠️ Công nghệ Sử dụng

### 1. Backend
- **Framework**: FastAPI (Asynchronous Python Web Framework).
- **ORM & DB**: SQLAlchemy, Pydantic v2, SQLite (Local Dev) / Amazon RDS PostgreSQL (Production).
- **AWS SDK**: `boto3` (Tương tác S3, EventBridge Scheduler, Lambda, STS, IAM).
- **AI Integration**: Google Gemini 3.5 Flash Lite qua `httpx`.

### 2. Frontend
- **Framework**: React 18, Vite.
- **Styling**: Tailwind CSS, Lucide Icons.
- **HTTP Client**: Axios.

### 3. AWS Cloud Services (Serverless & Storage)
- **Amazon S3**: Lưu trữ media bucket với CORS configuration.
- **AWS EventBridge Scheduler**: Quản lý lịch trình One-time schedule với `ActionAfterCompletion="DELETE"`.
- **AWS Lambda**: Hàm `PublishPostFunction` xử lý xuất bản khi trigger được kích hoạt.
- **AWS IAM**: Phân quyền tối thiểu (Least Privilege) với `EventBridgeSchedulerRole` và `PublishPostLambdaRole`.
- **AWS Budgets**: Giám sát và tự động cảnh báo ngân sách $10/tháng.

---

## 🚀 Hướng dẫn Cài đặt & Chạy Cục bộ

### Bước 1: Clone Repository
```bash
git clone https://github.com/HG2505/aws-social-media-scheduler.git
cd aws-social-media-scheduler
```

### Bước 2: Thiết lập Backend
```bash
cd backend
python -m venv .venv
# Kích hoạt venv (Windows):
.venv\Scripts\activate

# Cài đặt thư viện:
pip install -r requirements.txt

# Cấu hình biến môi trường:
cp .env.example .env
# (Mở file .env và điền thông tin AWS Access Key và Gemini API Key)

# Khởi chạy server Backend:
uvicorn app.main:app --reload --port 8000
```
Backend sẽ khởi chạy tại: `http://localhost:8000` (Swagger UI: `http://localhost:8000/docs`).

### Bước 3: Thiết lập Frontend
Mở một terminal mới:
```bash
cd frontend
npm install
npm run dev
```
Frontend sẽ chạy tại: `http://localhost:5173`.

---

## ⚙️ Các Script Tự động hóa AWS Đi kèm

Dự án cung cấp sẵn các script Python dùng `boto3` để khởi tạo tài nguyên AWS tự động chỉ bằng 1 câu lệnh:
- **Tự động tạo S3 Bucket & CORS**:
  ```bash
  python backend/scripts/setup_s3.py
  ```
- **Tự động tạo IAM Roles, Lambda Function & EventBridge Scheduler**:
  ```bash
  python backend/scripts/setup_scheduler_lambda.py
  ```

---

## 👨‍💻 Tác giả

* **Trần Lê Gia Huy (HG2505)**
* GitHub: [https://github.com/HG2505](https://github.com/HG2505)
* Email: [tranlegiahuy25052005@gmail.com](mailto:tranlegiahuy25052005@gmail.com)
