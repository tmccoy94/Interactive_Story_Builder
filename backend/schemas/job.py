
from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel

class StoryJobBase(BaseModel):
    theme: str

class StoryJobResponse(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    story_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    
    class Config:
        from_attributes = True

# This class is just to have the naming convention be more clear
# It's not really going to have any unique properties.
# At least as of now...
class StoryJobCreate(StoryJobBase):
    pass