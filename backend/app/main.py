import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import posts, ai

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Social Media Post Scheduler API",
    description="Full-stack AWS Social Media Scheduler with EventBridge and S3 Integration",
    version="1.0.0"
)

# Enable CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(posts.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Social Media Post Scheduler API",
        "status": "online",
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
