import os
import boto3
from datetime import datetime
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

def get_aws_config():
    """Reloads and returns latest AWS settings from .env."""
    load_dotenv(override=True)
    region = os.getenv("AWS_REGION", "ap-southeast-1")
    s3_bucket = os.getenv("AWS_S3_BUCKET_NAME")
    scheduler_role_arn = os.getenv("AWS_EVENTBRIDGE_SCHEDULER_ROLE_ARN", "")
    return region, s3_bucket, scheduler_role_arn

def upload_file_to_s3(file_bytes, filename: str, content_type: str) -> str:
    """Uploads media file to AWS S3 bucket and returns public S3 URL."""
    region, s3_bucket, _ = get_aws_config()
    
    if not s3_bucket:
        raise ValueError("AWS_S3_BUCKET_NAME is not configured in .env")
    
    s3_client = boto3.client("s3", region_name=region)
    s3_client.put_object(
        Bucket=s3_bucket,
        Key=f"media/{filename}",
        Body=file_bytes,
        ContentType=content_type,
    )
    return f"https://{s3_bucket}.s3.{region}.amazonaws.com/media/{filename}"

def create_eventbridge_schedule(post_id: int, scheduled_at: datetime) -> str:
    """Schedules a one-time trigger in AWS EventBridge Scheduler to publish the post."""
    region, _, scheduler_role_arn = get_aws_config()
    schedule_name = f"post-schedule-{post_id}-{int(scheduled_at.timestamp())}"
    
    if not scheduler_role_arn or "123456789012" in scheduler_role_arn:
        print(f"[Local Dev] EventBridge Scheduler role not yet provisioned. Schedule mocked for post {post_id}.")
        return schedule_name

    cron_expression = f"at({scheduled_at.strftime('%Y-%m-%dT%H:%M:%S')})"
    account_id = scheduler_role_arn.split(":")[4]
    
    try:
        scheduler_client = boto3.client("scheduler", region_name=region)
        scheduler_client.create_schedule(
            Name=schedule_name,
            GroupName="default",
            ScheduleExpression=cron_expression,
            FlexibleTimeWindow={"Mode": "OFF"},
            Target={
                "Arn": f"arn:aws:lambda:{region}:{account_id}:function:PublishPostFunction",
                "RoleArn": scheduler_role_arn,
                "Input": f'{{"post_id": {post_id}}}',
            },
            ActionAfterCompletion="DELETE",
        )
        print(f"✅ [AWS EventBridge] Scheduled trigger created: {schedule_name} at {cron_expression}")
        return schedule_name
    except (BotoCoreError, ClientError) as err:
        print(f"EventBridge Scheduler Error: {err}")
        return schedule_name

def delete_eventbridge_schedule(schedule_name: str):
    """Deletes a scheduled trigger in AWS EventBridge Scheduler."""
    if not schedule_name or schedule_name.startswith("post-schedule-") and "mock" in schedule_name:
        return
    region, _, _ = get_aws_config()
    try:
        scheduler_client = boto3.client("scheduler", region_name=region)
        scheduler_client.delete_schedule(Name=schedule_name, GroupName="default")
    except Exception as err:
        print(f"Error deleting schedule {schedule_name}: {err}")
