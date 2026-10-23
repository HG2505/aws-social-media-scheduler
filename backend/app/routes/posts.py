from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.services.aws_service import upload_file_to_s3, create_eventbridge_schedule, delete_eventbridge_schedule

router = APIRouter(prefix="/api/posts", tags=["Posts"])

@router.get("/", response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    """Retrieves all posts sorted by scheduled time descending."""
    return db.query(models.Post).order_by(models.Post.scheduled_at.desc()).all()

@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post_data: schemas.PostCreate, db: Session = Depends(get_db)):
    """Creates a new post and registers an AWS EventBridge Schedule."""
    # Handle timezone comparison safely
    scheduled_at = post_data.scheduled_at
    if scheduled_at.tzinfo is not None:
        now = datetime.now(timezone.utc)
        if scheduled_at <= now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scheduled time must be in the future."
            )
        # Store naive UTC in database for consistency across SQLite and PostgreSQL
        scheduled_at_db = scheduled_at.astimezone(timezone.utc).replace(tzinfo=None)
    else:
        now = datetime.utcnow()
        if scheduled_at <= now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scheduled time must be in the future."
            )
        scheduled_at_db = scheduled_at

    new_post = models.Post(
        title=post_data.title,
        content=post_data.content,
        platform=post_data.platform,
        scheduled_at=scheduled_at_db,
        media_url=post_data.media_url,
        status=models.PostStatus.SCHEDULED
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # Schedule AWS EventBridge Trigger
    schedule_name = create_eventbridge_schedule(new_post.id, new_post.scheduled_at)
    new_post.eventbridge_schedule_name = schedule_name
    db.commit()
    db.refresh(new_post)

    return new_post

@router.post("/upload-media")
async def upload_media(file: UploadFile = File(...)):
    """Uploads media attachment (image/video) to S3."""
    try:
        contents = await file.read()
        filename = f"{int(datetime.utcnow().timestamp())}_{file.filename}"
        url = upload_file_to_s3(contents, filename, file.content_type)
        return {"media_url": url}
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"S3 Upload failed: {str(err)}"
        )

@router.post("/{post_id}/publish-now", response_model=schemas.PostResponse)
def publish_now(post_id: int, db: Session = Depends(get_db)):
    """Immediately publishes a post and updates status."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    if post.eventbridge_schedule_name:
        delete_eventbridge_schedule(post.eventbridge_schedule_name)

    post.status = models.PostStatus.PUBLISHED
    post.published_at = datetime.utcnow()
    db.commit()
    db.refresh(post)
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Cancels and deletes a scheduled post."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found.")

    if post.eventbridge_schedule_name:
        delete_eventbridge_schedule(post.eventbridge_schedule_name)

    db.delete(post)
    db.commit()
    return None
