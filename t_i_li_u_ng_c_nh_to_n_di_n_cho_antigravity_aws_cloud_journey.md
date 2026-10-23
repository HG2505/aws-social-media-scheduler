# 🧠 TÀI LIỆU NGỮ CẢNH TOÀN DIỆN DÀNH CHO TRỢ LÝ AI (ANTIGRAVITY IDE)
> **Dự án trọng tâm**: Social Media Post Scheduler (AWS Full-Stack)
> **Thư mục làm việc (Workspace)**: `f:\AWS`
> **Nguồn tài liệu Lab chuẩn**: [The First Cloud Journey - AWS Study Group](https://cloudjourney.awsstudygroup.com/)
> **Ngân sách AWS**: $200 USD Credit (Đã kích hoạt AWS Budgets & Auto-Stop Action ở ngưỡng $10/tháng)

---

## 🎯 PHẦN 1: CHỈ THỊ HỆ THỐNG DÀNH CHO ANTIGRAVITY (SYSTEM DIRECTIVES)

Khi đọc file này, **Antigravity** cần nắm vững các nguyên tắc cốt lõi sau để hỗ trợ người dùng:
1. **Vai trò**: Kiến trúc sư Giải pháp AWS (AWS Solutions Architect) kiêm Kỹ sư Full-Stack cao cấp, hướng dẫn thực hành bám sát chuẩn của **The First Cloud Journey (AWS Study Group)**.
2. **Ràng buộc Ngân sách Nghiêm ngặt ($200 Credit)**:
   * Mọi kiến trúc, dịch vụ AWS đề xuất **BẮT BUỘC** ưu tiên tối đa **AWS Free Tier** hoặc **Serverless (Pay-per-use)** để duy trì chi phí ở mức **$0 – $5/tháng**.
   * Tuyệt đối không tự ý cấu hình các dịch vụ tính phí cố định cao theo giờ (như NAT Gateway không cần thiết, EC2 GPU lớn, RDS Multi-AZ bản thương mại, hoặc OpenSearch cluster lớn) mà không cảnh báo trước.
3. **Bảo mật (Security First)**:
   * Không bao giờ ghi cứng (hardcode) `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, hay `GEMINI_API_KEY` vào mã nguồn. Tất cả phải đọc qua biến môi trường (`backend/.env`) và được loại trừ trong `.gitignore`.
   * Áp dụng nguyên tắc **Least Privilege (Quyền tối thiểu)** khi hướng dẫn tạo IAM Role / IAM Policy.

---

## 👤 PHẦN 2: HỒ SƠ NĂNG LỰC & CÁC DỰ ÁN NỀN TẢNG CỦA NGƯỜI DÙNG

Người dùng đã có nền tảng thực chiến qua các repository sau (Antigravity có thể tham chiếu phong cách code khi cần):
1. **`thaikhang113/cv_jd_mapping` (CV Match Platform)**:
   * **Stack**: FastAPI (Python), Motor (Async MongoDB), React + Vite, JWT, Docker, Azure App Service.
   * **Kỹ thuật**: Bóc tách PDF/DOCX (`pdfplumber`, `python-docx`), NLP Matching Engine (`scikit-learn` TF-IDF + Cosine Similarity), hệ thống phân quyền 3 vai trò (Candidate, Recruiter, Admin).
2. **`thaikhang113/dubflow` (AI Video Dubbing Desktop App v3.0.32)**:
   * **Stack**: Python, PySide6 (Modern Dark GUI), QThread Workers, MCP Server (`mcp_server.py`).
   * **Kỹ thuật**: End-to-End Media Pipeline (`yt-dlp` + `aria2c`, `Faster-Whisper` ASR, `Demucs` tách nhạc nền, dịch thuật LLM, `VieNeu TTS` INT8, `FFmpeg` mixer, xóa phụ đề cứng STTN/ProPainter).
3. **`tinkismeeee/Website-Hotel-Management-System`**:
   * **Stack**: Node.js, Express.js (ES Modules), Handlebars (`hbs` SSR), `express-session`, `bcryptjs`.
   * **Kỹ thuật**: Kiến trúc MVC quản lý đặt phòng, hóa đơn, hạng phòng, dịch vụ và khách hàng.

---

## 🏗️ PHẦN 3: TRẠNG THÁI HIỆN TẠI CỦA DỰ ÁN `SOCIAL MEDIA POST SCHEDULER`

### 3.1. Cấu trúc thư mục tại `f:\AWS`
```text
f:\AWS\
├── .gitignore                            # Bảo vệ file .env, venv, node_modules, __pycache__
├── LICH_SU_HOI_THOAI.md                  # Lịch sử quá trình phát triển dự án
├── ANTIGRAVITY_MASTER_CONTEXT.md         # File ngữ cảnh trung tâm này
├── backend/                              # Backend Service (Python FastAPI)
│   ├── app/
│   │   ├── main.py                       # App Entrypoint & Cấu hình CORS
│   │   ├── database.py                   # Kết nối SQLite (Local) / RDS PostgreSQL (AWS)
│   │   ├── models.py                     # SQLAlchemy Models (Post, PostStatus, PostPlatform)
│   │   ├── schemas.py                    # Pydantic Schemas validation
│   │   ├── routes/
│   │   │   ├── posts.py                  # API CRUD bài viết, Upload S3, Publish Now (Đã fix chuẩn UTC)
│   │   │   └── ai.py                     # Multi-Provider AI Copilot Adapter (Gemini, Groq, DeepSeek, Bedrock, OpenAI)
│   │   └── services/
│   │       └── aws_service.py            # Kết nối AWS S3 & AWS EventBridge Scheduler (Có chế độ Mock Fallback)
│   ├── requirements.txt                  # Đã cài đặt đầy đủ (fastapi, uvicorn, boto3, sqlalchemy...)
│   ├── .env.example                      # Mẫu cấu hình môi trường
│   └── .env                              # File cấu hình thực tế (Đã gắn GEMINI_API_KEY hoạt động 200 OK)
│
└── frontend/                             # Frontend Web (React + Vite + Tailwind CSS)
    ├── src/
    │   ├── App.jsx                       # Giao diện Modern Dark UI + AI Modal + Queue List (Đã nâng cấp báo lỗi chi tiết)
    │   ├── main.jsx
    │   └── index.css                     # Tailwind CSS Styling
    ├── package.json                      # Đã chạy npm install thành công
    ├── vite.config.js                    # Cấu hình Proxy API tới cổng 8000
    └── tailwind.config.js
```

### 3.2. Các hạng mục kỹ thuật ĐÃ HOÀN THÀNH (Completed Milestones)
1. **Thiết lập Tài khoản & Bảo vệ Ngân sách AWS ($200 Credit)**:
   * Đã hoàn thành các bài lab để nhận **$200 AWS Credit**.
   * Đã tạo **AWS Cost Budget** với ngưỡng **$10.00/tháng** (Cảnh báo email ở mốc 80% thực tế và 100% dự báo).
   * Đã tạo IAM Role `AWSBudgetsActionRole` (gắn policy `AWSBudgetsActionsWithAWSResourceControlAccess`) và kích hoạt **AWS Budget Action**: Tự động dừng máy chủ (`Automate instances to stop for EC2 or RDS` - chế độ `Automatic`) khi chạm ngưỡng 100% ngân sách.
2. **Khởi chạy Local & Xử lý lỗi Timezone**:
   * Đã sửa lỗi `500 Internal Server Error` (`TypeError: can't compare offset-naive and offset-aware datetimes`) trong `backend/app/routes/posts.py` bằng cách đồng bộ chuẩn `datetime.now(timezone.utc)`.
   * Đã kiểm thử tạo lịch đăng bài thành công (`201 Created`).
3. **Nâng cấp Kiến trúc Multi-Provider AI Adapter (`backend/app/routes/ai.py`)**:
   * Thay thế hoàn toàn dữ liệu AI gán cứng bằng bộ điều phối tự động nhận diện qua `.env`:
     * `GEMINI_API_KEY`: Gọi Google Gemini (`gemini-3.5-flash-lite` / `gemini-1.5-flash` - Miễn phí 15 RPM / 1.500 RPD).
     * `GROQ_API_KEY`: Gọi Groq (Llama 3.3 70B).
     * `DEEPSEEK_API_KEY`: Gọi DeepSeek Chat.
     * `AI_PROVIDER=bedrock`: Gọi Claude 3.5 Sonnet / Llama 3 trên Amazon Bedrock qua `boto3`.
     * `OPENAI_API_KEY`: Gọi GPT-4o-mini / GPT-3.5.
   * Đã cấu hình `backend/.env` với `GEMINI_API_KEY` thực tế và tạo `.gitignore` bảo vệ.

---

## 📚 PHẦN 4: TOÀN BỘ KIẾN THỨC & DANH MỤC BÀI LAB TỪ `THE FIRST CLOUD JOURNEY`
*(Nguồn: https://cloudjourney.awsstudygroup.com/ - Cộng đồng AWS Study Group)*

Dưới đây là toàn bộ 8 Chương (Pillars) và danh sách chi tiết hơn 100+ bài thực hành (Hands-on Labs) trên trang **The First Cloud Journey**. Antigravity sử dụng danh mục này để hướng dẫn người dùng cấu hình AWS theo đúng chuẩn của AWS Study Group:

### 1️⃣ Chương 1: Explore AWS Services (Khám phá Dịch vụ AWS Nền tảng)
* **Quản trị Tài khoản, Chi phí & Bảo mật cơ bản**:
  1. *Creating Your First AWS Account* (Tạo tài khoản AWS đầu tiên).
  2. *Managing Costs with AWS Budgets* (Quản lý chi phí với AWS Budgets — **Đã áp dụng vào dự án**).
  3. *Getting Help with AWS Support* (Liên hệ hỗ trợ AWS Support).
  4. *Access Management with AWS Identity and Access Management (IAM)* (Quản lý danh tính & phân quyền IAM — **Áp dụng tạo IAM User & Role cho dự án**).
* **Hạ tầng Mạng & Máy chủ ảo (Networking & Compute)**:
  5. *Networking Essentials with Amazon Virtual Private Cloud (VPC)* (Thiết lập mạng riêng ảo VPC, Subnet, Route Table, Internet Gateway, NAT Gateway).
  6. *Compute Essentials with Amazon Elastic Compute Cloud (EC2)* (Khởi tạo máy chủ ảo EC2, Security Group, Key Pair).
  7. *Instance Profiling with IAM Roles for EC2* (Gắn quyền IAM Role trực tiếp cho máy chủ EC2 không cần lưu Access Key).
  8. *Cloud Development with AWS Cloud9* (Môi trường lập trình IDE trên đám mây).
  9. *Simplified Computing with Amazon Lightsail* (Máy chủ ảo tinh gọn chi phí cố định).
  10. *Container Deployment with Amazon Lightsail Containers* (Triển khai Container trên Lightsail).
  11. *Scaling Applications with EC2 Auto Scaling* (Tự động co giãn số lượng máy chủ theo tải).
  12. *Windows Workloads on AWS* & *Directory Services with AWS Managed Microsoft AD*.
  13. *Building Highly Available Web Applications* (Xây dựng ứng dụng Web có độ sẵn sàng cao đa vùng khả dụng Multi-AZ).
* **Lưu trữ, Cơ sở dữ liệu & Phân phối nội dung (Storage, DB & CDN)**:
  14. *Static Website Hosting with Amazon S3* (Lưu trữ file và host giao diện Web tĩnh trên S3 — **Áp dụng trực tiếp cho Frontend React & lưu ảnh bài đăng**).
  15. *Database Essentials with Amazon Relational Database Service (RDS)* (Khởi tạo và quản trị CSDL quan hệ PostgreSQL/MySQL — **Áp dụng cho Database Production của dự án**).
  16. *NoSQL Database Essentials with Amazon DynamoDB* (Cơ sở dữ liệu NoSQL Serverless tốc độ cao).
  17. *In-Memory Caching with Amazon ElastiCache* (Tăng tốc truy xuất với bộ nhớ đệm Redis/Memcached).
  18. *Hybrid DNS Management with Amazon Route 53* (Quản lý tên miền và định tuyến DNS).
  19. *Content Delivery with Amazon CloudFront* (Mạng phân phối nội dung CDN toàn cầu kèm HTTPS — **Áp dụng đứng trước S3 Frontend**).
  20. *Edge Computing with CloudFront and Lambda@Edge* (Xử lý logic tại trạm biên CDN).
* **Giám sát & Công cụ dòng lệnh**:
  21. *Monitoring with Amazon CloudWatch* (Thu thập Metrics, Logs và tạo Cảnh báo Alarms).
  22. *Command Line Operations with AWS CLI* (Thao tác quản trị AWS qua giao diện dòng lệnh `aws-cli`).
  23. *Networking on AWS Workshop* (Chuỗi thực hành mạng chuyên sâu).

### 2️⃣ Chương 2: Migrate to AWS (Di chuyển Hệ thống lên Đám mây)
1. *VM Migration with AWS VM Import/Export* (Chuyển đổi máy ảo từ On-premises lên EC2).
2. *Database Migration with AWS Database Migration Service (DMS) and Schema Conversion Tool (SCT)* (Di chuyển cơ sở dữ liệu không gián đoạn).
3. *Disaster Recovery with AWS Elastic Disaster Recovery* (Thiết lập hệ thống phục hồi sau thảm họa).

### 3️⃣ Chương 3: Optimizing the System on AWS (Tối ưu hóa Hệ thống theo 5 Trụ cột Well-Architected)

#### 🔹 A. Operations (Vận hành xuất sắc & Infrastructure as Code)
1. *Serverless Automation with AWS Lambda* (Tự động hóa tác vụ không máy chủ với Lambda — **Áp dụng cho hàm `PublishPostFunction` của dự án**).
2. *Advanced Monitoring with CloudWatch and Grafana* & *CloudWatch Advanced Workshop*.
3. *Resource Organization with Tags and Resource Groups* & *Access Control with IAM and Resource Tags* (Quản lý tài nguyên và phân quyền theo thẻ Tag).
4. *Systems Management with AWS Systems Manager (SSM)* & *Remote Server Access with Systems Manager Session Manager* (Truy cập máy chủ bảo mật không cần mở port SSH 22).
5. *Infrastructure as Code with AWS CloudFormation* (Định nghĩa hạ tầng bằng YAML/JSON).
6. *Cloud Development Kit (AWS CDK) Essentials* & *AWS CDK Advanced* & *Infrastructure as Code Workshop Series* (Xây dựng hạ tầng bằng code TypeScript/Python).
7. *Right-Sizing with EC2 Resource Optimization* & *Network Monitoring with VPC Flow Logs*.
8. *Billing Console Delegation*, *Managing Quotas with Service Quotas*, *Cost and Usage Management*.
9. *Snapshot Automation with Amazon EBS Data Lifecycle Manager* & *Anomaly Detection for EBS Backups*.
10. *Development Environment with AWS Toolkit for VS Code* (Tích hợp bộ công cụ AWS trực tiếp vào IDE).

#### 🔹 B. Security (Bảo mật toàn diện)
1. *Identity Federation with AWS Single Sign-On (IAM Identity Center)*.
2. *Permission Management with IAM Permission Boundaries* & *Access Control with IAM Policies and Conditions*.
3. *Security Compliance with AWS Security Hub* & *Threat Detection with AWS GuardDuty*.
4. *Private Access to S3 with VPC Endpoints* (Kết nối S3 nội bộ không đi qua Internet).
5. *Application Protection with AWS WAF* & *Security Governance with AWS Firewall Manager* (Tường lửa bảo vệ ứng dụng Web).
6. *Encryption with AWS Key Management Service (KMS)* (Mã hóa dữ liệu với khóa KMS).
7. *Data Protection with Amazon Macie* (Tự động phát hiện dữ liệu nhạy cảm trên S3).
8. *Credentials Management with AWS Secrets Manager* (Lưu trữ và xoay vòng khóa API/DB Password an toàn — **Có thể nâng cấp thay cho `.env` khi lên Production**).
9. *Systems Patching with EC2 Image Builder*.
10. *Cross-Domain Authentication with Amazon Cognito* (Xác thực người dùng OAuth2/JWT).
11. *S3 Security Best Practices* (Cấu hình Bucket Policy, CORS, Block Public Access, Presigned URLs — **Áp dụng trực tiếp cho tính năng Upload ảnh của dự án**).

#### 🔹 C. Reliability (Độ tin cậy & Khả năng chịu lỗi)
1. *Data Protection with AWS Backup*.
2. *Network Integration with VPC Peering* & *Centralized Network Management with AWS Transit Gateway*.
3. *Messaging Systems with SQS and SNS* (Hàng đợi tin nhắn bất đồng bộ Amazon SQS và dịch vụ thông báo đẩy Amazon SNS).
4. *Shared Storage with Amazon EBS Multi-Attach* & *Database High Availability with EBS Multi-Attach and Systems Manager*.
5. *Windows Server Failover Clustering on AWS* & *SQL Server High Availability on AWS (2019 / 2022)*.

#### 🔹 D. Performance Efficiency (Hiệu suất & Hiện đại hóa quy trình)
1. *Containerization with Docker* & *Container Orchestration with Amazon ECS* & *Infrastructure as Code for ECS with CDK*.
2. *CI/CD Pipeline with AWS CodePipeline*, *Automated Deployments with AWS CodePipeline*, *DevOps with AWS CodePipeline* (Tự động hóa quy trình Build - Test - Deploy).
3. *Hybrid Storage with AWS Storage Gateway* & *Windows File Storage with Amazon FSx*.
4. *Building Advanced Applications with Amazon DynamoDB*.
5. *Workflow Orchestration with AWS Step Functions* (Điều phối luồng công việc Serverless phức tạp).
6. *Storage Performance Workshop*.

#### 🔹 E. Cost Optimization (Tối ưu hóa Chi phí)
1. *Cost Savings with Savings Plans and Reserved Instances*.
2. *Cost Visualization and Analytics* (Trực quan hóa chi phí).
3. *Cost Data Analysis with AWS Glue and Amazon Athena* (Truy vấn dữ liệu hóa đơn chi tiết bằng SQL).

### 4️⃣ Chương 4: Application Modernization on AWS (Hiện đại hóa Ứng dụng & Serverless)
*(Chương này chứa các kiến trúc mẫu sát nhất với dự án `Social Media Post Scheduler`)*

* **Serverless - DevAx Series**:
  1. *Monolith to Microservices Migration* (Chuyển đổi từ nguyên khối sang vi dịch vụ).
  2. *CI/CD for Application Release* & *Building Microservices*.
  3. *Data and Workflow Restructuring*.
  4. *Event-Driven Architecture* (Kiến trúc hướng sự kiện với Amazon EventBridge — **Trái tim của tính năng Lập lịch đăng bài**).
  5. *Single Page Application Authentication* (Xác thực cho ứng dụng React SPA).
  6. *AWS AI Services Integration* (Tích hợp dịch vụ AI vào ứng dụng).
* **Serverless - Book Store Series**:
  1. *Serverless Backend with Lambda, S3, and DynamoDB*.
  2. *Frontend Development for Serverless APIs* (Kết nối React với Backend AWS).
  3. *Deployment Automation with AWS SAM (Serverless Application Model)*.
  4. *User Authentication with Amazon Cognito*.
  5. *Custom Domains and SSL for Serverless Applications* (Cấu hình tên miền riêng & chứng chỉ ACM SSL).
  6. *Event Processing with SQS and SNS*.
  7. *CI/CD for Serverless Applications* & *Monitoring Serverless Applications*.
  8. *Building GraphQL APIs with AWS AppSync*.
* **Serverless - Document Management System Series**:
  1. *Building Serverless CRUD with Lambda and DynamoDB*.
  2. *Serverless Storage and Auth with AWS Amplify*.
  3. *Frontend Integration with API Gateway* (Kết nối Frontend qua REST/HTTP API Gateway).
  4. *Document Management System Deployment with AWS SAM*.
  5. *Content Delivery Setup with CloudFront*.
  6. *Adding Search Functionality*.
  7. *DevOps for Document Management System*.
  8. *Distributed Tracing with X-Ray and CloudWatch* (Theo dõi vết thực thi request xuyên suốt các dịch vụ).
* **Serverless Web App Workshop**:
  1. *Building Serverless APIs* & *Serverless Chat Application*.
* **Elastic Beanstalk & WordPress Workshops**:
  1. *Deploying Node.js Applications* & *CI/CD with Elastic Beanstalk and CDK Pipelines*.
  2. *WordPress Architecture on AWS* & *Running WordPress on Amazon EC2*.

### 5️⃣ Chương 5: Container Services on AWS (Dịch vụ Container)
1. *Getting Started with Amazon Lightsail Containers*.
2. **Amazon ECS Workshop**:
   * *Containerization with Amazon ECS and AWS Fargate* (Chạy Docker Container không cần quản lý máy chủ — **Giải pháp thay thế hoặc song hành cùng AWS App Runner cho Backend FastAPI**).
   * *Infrastructure as Code for ECS with CDK*.
   * *CI/CD Pipeline for ECS Applications*.
3. **Amazon EKS Workshop**:
   * *Getting Started with Amazon EKS (Kubernetes)*, *EKS Blueprints for CDK*, *CI/CD for EKS Applications*.
4. *Red Hat OpenShift Service on AWS (ROSA)*.

### 6️⃣ Chương 6: Data & Analytics Services on AWS (Dữ liệu & Phân tích)
1. *Data Lake Fundamentals on AWS* & *Building a Data Lake with Your Own Data*.
2. *Data Analytics Services Overview* & *Data Engineering Immersion Day*.
3. *Business Intelligence with Amazon QuickSight* (Vẽ biểu đồ BI phân tích dữ liệu).
4. *Serverless Analytics with Amazon Athena* (Truy vấn trực tiếp dữ liệu trên S3 bằng SQL).
5. *Advanced PostgreSQL on AWS - Part 1 & Part 2* (Tối ưu hóa và vận hành PostgreSQL chuyên sâu trên Amazon RDS — **Tài liệu tham khảo cho tầng Database của dự án**).

### 7️⃣ Chương 7: AI/ML Services on AWS (Trí tuệ nhân tạo & Học máy)
1. *Machine Learning with Amazon SageMaker* & *SageMaker Immersion Day*.
2. Kết hợp với **Amazon Bedrock** (Foundation Models như Claude 3.5 Sonnet / Llama 3) đã được tích hợp sẵn trong `backend/app/routes/ai.py`.

### 8️⃣ Chương 8: FCJ Workforce Program
* Chương trình đào tạo và phát triển nguồn nhân lực thực chiến thông qua việc xây dựng dự án hoàn chỉnh từ con số 0 (chính là mục tiêu của dự án **Social Media Post Scheduler** này).

---

## 🔗 PHẦN 5: BẢNG ÁNH XẠ CÁC BÀI LAB FCJ VÀO DỰ ÁN `SOCIAL MEDIA POST SCHEDULER`

Khi Antigravity hướng dẫn người dùng thực hiện từng bước tiếp theo của dự án, hãy bám sát kiến trúc từ các bài Lab tương ứng sau:

| Thành phần trong Dự án | Dịch vụ AWS sử dụng | Bài Lab tương ứng trên The First Cloud Journey | Trạng thái |
| :--- | :--- | :--- | :--- |
| **Quản lý Ngân sách $200** | AWS Budgets + Budget Actions | *Chương 1: Managing Costs with AWS Budgets* | ✅ Đã hoàn thành |
| **Phân quyền Code & Dịch vụ** | AWS IAM (User, Role, Policy) | *Chương 1: Access Management with AWS IAM* | 🔄 Đang thực hiện |
| **Lưu trữ Ảnh đính kèm bài đăng** | Amazon S3 + CORS / Presigned URL | *Chương 1: Static Website Hosting with S3* & *Chương 3B: S3 Security Best Practices* | ⏳ Chuẩn bị làm |
| **Bộ hẹn giờ đăng bài tự động** | Amazon EventBridge Scheduler | *Chương 4: Event-Driven Architecture* | ⏳ Chuẩn bị làm |
| **Worker thực thi đăng bài** | AWS Lambda (`PublishPostFunction`) | *Chương 3A: Serverless Automation with AWS Lambda* | ⏳ Chuẩn bị làm |
| **AI Copilot tạo Caption/Hashtags** | Google Gemini API / Amazon Bedrock | *Chương 4: AWS AI Services Integration* | ✅ Đã xong (Gemini) |
| **Cơ sở dữ liệu Production** | Amazon RDS for PostgreSQL (`db.t4g.micro`) | *Chương 1: Database Essentials with RDS* & *Chương 6: Advanced PostgreSQL* | ⏳ Giai đoạn 3 |
| **Triển khai Backend FastAPI** | AWS App Runner / ECS Fargate / Lightsail | *Chương 5: Containerization with Amazon ECS & Fargate* | ⏳ Giai đoạn 3 |
| **Triển khai Frontend React SPA** | Amazon S3 + Amazon CloudFront (CDN) | *Chương 1: Content Delivery with CloudFront* & *Chương 4: DMS Content Delivery* | ⏳ Giai đoạn 3 |
| **Giám sát Log & Lỗi hệ thống** | Amazon CloudWatch Logs & Alarms | *Chương 1: Monitoring with Amazon CloudWatch* | ⏳ Giai đoạn 3 |
| **Xác thực người dùng (Mở rộng)** | Amazon Cognito | *Chương 4: User Authentication with Amazon Cognito* | 💡 Giai đoạn 4 |
| **Tự động hóa Deploy (Mở rộng)** | AWS CodePipeline / GitHub Actions | *Chương 3D: CI/CD Pipeline with AWS CodePipeline* | 💡 Giai đoạn 4 |

---

## 🚀 PHẦN 6: LỘ TRÌNH HÀNH ĐỘNG TIẾP THEO (NEXT ACTION ITEMS CHO ANTIGRAVITY)

Hiện tại người dùng đã hoàn tất **Giai đoạn 1 (Chạy Local, sửa lỗi Timezone, tích hợp Gemini AI Copilot, cài đặt AWS Budgets Action)**. Khi người dùng yêu cầu tiếp tục, Antigravity hãy hướng dẫn lần lượt từ **Giai đoạn 2**:

### 📌 Giai đoạn 2: Tích hợp Dịch vụ AWS Thật vào Môi trường Local (Đang ở bước này)
1. **Bước 2.1 - Tạo S3 Bucket lưu trữ ảnh (`ap-southeast-1`)**:
   * Hướng dẫn tạo Bucket trên AWS Console (ví dụ: `social-scheduler-media-<username>`).
   * Cấu hình **CORS Policy** cho phép `GET`, `PUT`, `POST`, `DELETE`, `HEAD` từ Frontend.
   * Cấu hình quyền đọc ảnh hoặc sử dụng Presigned URLs theo chuẩn *S3 Security Best Practices*.
2. **Bước 2.2 - Tạo IAM User / Policy cho Backend Local**:
   * Tạo IAM User (ví dụ: `scheduler-dev-user`) với quyền tối thiểu truy cập S3 Bucket vừa tạo và quyền tạo lịch trên EventBridge Scheduler.
   * Điền `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION=ap-southeast-1`, `AWS_S3_BUCKET_NAME` vào `f:\AWS\backend\.env`.
3. **Bước 2.3 - Thiết lập AWS Lambda (`PublishPostFunction`) & EventBridge Scheduler Role**:
   * Tạo hàm AWS Lambda (Python 3.12) nhận payload `{"post_id": ...}` từ EventBridge Scheduler.
   * Tạo IAM Role `EventBridgeSchedulerRole` (Trusted entity: `scheduler.amazonaws.com`) có quyền `lambda:InvokeFunction` tới hàm Lambda trên.
   * Cập nhật `AWS_EVENTBRIDGE_SCHEDULER_ROLE_ARN` và `AWS_LAMBDA_TARGET_ARN` vào `f:\AWS\backend\.env`.
   * Kiểm thử thực tế: Tạo bài đăng hẹn giờ sau 2 phút trên giao diện React `http://localhost:5173` ➔ Kiểm tra ảnh xuất hiện trên S3 ➔ Kiểm tra lịch xuất hiện trong AWS EventBridge Console ➔ Kiểm tra Lambda tự động kích hoạt sau 2 phút.

### 📌 Giai đoạn 3: Đưa Toàn Bộ Hệ Thống Lên AWS Cloud (Production Deployment)
1. **Bước 3.1 - Khởi tạo Amazon RDS PostgreSQL (Free Tier)**:
   * Chọn `PostgreSQL`, mẫu `Free tier`, instance `db.t4g.micro` (miễn phí 750 giờ/tháng), vùng `ap-southeast-1`.
   * Cấu hình Security Group cho phép Backend và Lambda kết nối vào port `5432`.
   * Cập nhật `DATABASE_URL` trong Backend để chuyển từ SQLite sang RDS PostgreSQL.
2. **Bước 3.2 - Đóng gói Docker & Deploy Backend FastAPI**:
   * Tạo `Dockerfile` tối ưu cho thư mục `f:\AWS\backend`.
   * Triển khai lên **AWS App Runner** hoặc **Amazon ECS Fargate / Amazon Lightsail Containers** (Lưu ý cấu hình Auto-pause hoặc giới hạn task để tiết kiệm tối đa $200 credit).
3. **Bước 3.3 - Deploy Frontend React lên S3 + CloudFront CDN**:
   * Cập nhật biến môi trường `VITE_API_URL` trỏ về URL HTTPS của Backend trên Cloud.
   * Chạy `npm run build` tại `f:\AWS\frontend`.
   * Tạo S3 Bucket cho Frontend, đồng bộ thư mục `dist/` lên S3 và tạo **CloudFront Distribution** (kèm cấu hình Custom Error Response `403/404 -> /index.html` mã `200` cho React Router SPA).

### 📌 Giai đoạn 4: Nâng Cấp Hoàn Thiện Hồ Sơ Năng Lực (Portfolio Polish)
1. Đấu nối API mạng xã hội thật (Facebook Fanpage Graph API / LinkedIn API / Telegram Channel Bot) bên trong hàm Lambda `PublishPostFunction`.
2. Bổ sung **Amazon Cognito** để hỗ trợ nhiều người dùng đăng nhập và quản lý lịch đăng bài riêng.
3. Thiết lập **CI/CD Pipeline** (GitHub Actions hoặc AWS CodePipeline) để tự động deploy mỗi khi `git push`.
4. Viết tài liệu `README.md` chuẩn chỉnh kèm sơ đồ kiến trúc AWS (Architecture Diagram) để đưa vào CV.