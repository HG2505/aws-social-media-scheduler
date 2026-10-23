"""
Script tự động khởi tạo AWS S3 Bucket và cấu hình CORS cho dự án Social Media Scheduler.
Sử dụng chính Access Key đã lưu trong backend/.env.
"""
import os
import sys
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Đảm bảo in tiếng Việt & emoji không bị lỗi trên Windows PowerShell / CMD
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Nạp cấu hình từ .env
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)

AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or "your_" in AWS_ACCESS_KEY_ID:
    print("❌ Lỗi: Chưa cấu hình AWS Access Key hợp lệ trong file .env!")
    sys.exit(1)

# Khởi tạo S3 Client
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

# Lấy Account ID để sinh tên Bucket duy nhất toàn cầu
sts = boto3.client(
    "sts",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
account_id = sts.get_caller_identity()["Account"]
BUCKET_NAME = f"social-posts-media-{account_id}"

print(f"🚀 Bắt đầu thiết lập AWS S3 Bucket: {BUCKET_NAME} (Region: {AWS_REGION})...")

# 1. Tạo S3 Bucket
try:
    if AWS_REGION == "us-east-1":
        s3.create_bucket(Bucket=BUCKET_NAME)
    else:
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={"LocationConstraint": AWS_REGION},
        )
    print(f"✅ Đã tạo thành công S3 Bucket: {BUCKET_NAME}")
except ClientError as e:
    code = e.response["Error"]["Code"]
    if code in ["BucketAlreadyOwnedByYou", "BucketAlreadyExists"]:
        print(f"ℹ️ Bucket '{BUCKET_NAME}' đã tồn tại sẵn trong tài khoản của bạn.")
    else:
        print(f"❌ Lỗi khi tạo Bucket: {e}")
        sys.exit(1)

# 2. Cấu hình CORS cho Bucket để Frontend có thể Upload và hiển thị ảnh
print("🔧 Đang cấu hình CORS Policy...")
cors_configuration = {
    "CORSRules": [
        {
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
            "AllowedOrigins": ["*"],
            "ExposeHeaders": ["ETag"],
            "MaxAgeSeconds": 3000,
        }
    ]
}

try:
    s3.put_bucket_cors(Bucket=BUCKET_NAME, CORSConfiguration=cors_configuration)
    print("✅ Đã gắn CORS Policy thành công! (Cho phép Web App tải ảnh)")
except ClientError as e:
    print(f"⚠️ Cảnh báo cấu hình CORS: {e}")

# 3. Cập nhật lại tên Bucket vào file .env
print(f"📝 Đang cập nhật AWS_S3_BUCKET_NAME={BUCKET_NAME} vào file .env...")
try:
    with open(env_path, "r", encoding="utf-8") as f:
        content = f.read()

    import re
    new_content = re.sub(
        r"AWS_S3_BUCKET_NAME=.*",
        f"AWS_S3_BUCKET_NAME={BUCKET_NAME}",
        content
    )

    with open(env_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("🎉 Hoàn tất! File .env đã được cập nhật tên Bucket thật.")
except Exception as e:
    print(f"⚠️ Không thể tự động ghi file .env: {e}")

print("\n" + "="*60)
print(f"✨ S3 BUCKET ĐÃ SẴN SÀNG SỬ DỤNG:")
print(f"   - Tên Bucket : {BUCKET_NAME}")
print(f"   - Khu vực     : {AWS_REGION}")
print(f"   - Phân quyền  : Đã bật CORS")
print("="*60)
