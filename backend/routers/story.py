import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import (
    CompleteStoryResponse,
    CompleteStoryNodeResponse,
    CreateStoryRequest,
    StoryOptionsSchema,
)
from schemas.job import StoryJobResponse
from core.story_generator import StoryGenerator

router = APIRouter(prefix="/stories", tags=["stories"])


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
    db: Session = Depends(get_db),
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())
    job = StoryJob(
        job_id=job_id, session_id=session_id, theme=request.theme, status="pending"
    )
    db.add(job)
    db.commit()
    # --- ASYNC [A] ---
    # Background task runs after returning the pending job response.
    # Once complete, it updates the job status and attaches the story.
    # Triggers [B].
    background_tasks.add_task(
        generate_story_task, job_id=job_id, theme=request.theme, session_id=session_id
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

            story = StoryGenerator.generate_story(
                db=db, theme=theme, session_id=session_id
            )

            job.story_id = story.id
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


@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    complete_story = build_complete_story_tree(db, story)
    return complete_story


def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    # TODO: parse story to the usable front end format
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    node_dict = {}
    root_node = None
    for node in nodes:
        complete_story_node = CompleteStoryNodeResponse(
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            id=node.id,
            options=node.options,
        )
        node_dict[complete_story_node.id] = complete_story_node

        # check if root node and add that separately
        if node.is_root:
            root_node = complete_story_node

    if not root_node:
        raise HTTPException(
            status_code=500,
            detail="Story root node not found in story response from GPT API.",
        )

    complete_story_response = CompleteStoryResponse(
        id=story.id,
        created_at=story.created_at,
        root_node=root_node,
        all_nodes=node_dict,
        session_id=story.session_id,
        title=story.title
    )

    return complete_story_response
