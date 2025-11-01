from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str
    story_text: str
    duration_sec: Optional[int] = 20


class ProjectStatusUpdate(BaseModel):
    status: str 


class ProjectResponse(BaseModel):
    id: int
    title: str
    story_text: str
    duration_sec: int
    status: str
    video_path: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat()  # ← CONVERT datetime → ISO string
        }