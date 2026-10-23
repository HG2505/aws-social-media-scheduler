from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.models import PostStatus, PostPlatform

class PostBase(BaseModel):
    title: str
    content: str
    platform: PostPlatform = PostPlatform.FACEBOOK
    scheduled_at: datetime
    media_url: Optional[str] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    platform: Optional[PostPlatform] = None
    scheduled_at: Optional[datetime] = None
    media_url: Optional[str] = None
    status: Optional[PostStatus] = None

class PostResponse(PostBase):
    id: int
    status: PostStatus
    eventbridge_schedule_name: Optional[str] = None
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AICaptionRequest(BaseModel):
    topic: str
    tone: Optional[str] = "Professional"
    platform: Optional[PostPlatform] = PostPlatform.FACEBOOK

class AICaptionResponse(BaseModel):
    caption: str
    hashtags: list[str]
