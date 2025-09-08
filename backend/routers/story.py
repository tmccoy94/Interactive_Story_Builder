import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import CompleteStoryResopnse, CompleteStoryNodeResponse, CreateStoryRequest
from schemas.job import StoryJobResponse

router = APIRouter(
    prefix="/stories",
    tags=["stories"]
)

def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())
    job = StoryJob(
        job_id = job_id,
        session_id = session_id,
        theme = request.theme,
        status = "pending"
    )
    db.add(job)
    db.commit()
    # --- ASYNC [A] ---
    # Background task runs after returning the pending job response.
    # Once complete, it updates the job status and attaches the story.
    # Triggers [B].
    background_tasks.add_task(
        generate_story_task,
        job_id = job_id,
        theme=request.theme,
        session_id=session_id
    )

    return job  # Returns immediately with job in "pending" state

def generate_story_task(job_id: str, theme: str, session_id: str):
    # --- ASYNC [B] ---
    # Executed in background, scheduled by [A].
    # Must create a new DB session since request-scoped sessions
    # cannot be reused outside the request lifecycle.
    db = SessionLocal()

    try:
        # query story job table, look for matching id, return first response
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
        
        if not job:
            return
        
        try:
            job.status = "processing"
            db.commit()

            story = {} # TODO: generate the story

            job.story_id = 1 # TODO: update the story id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    finally:
        db.close()