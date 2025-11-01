# modules/scene/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SceneCreate(BaseModel):
    scene_index: int
    description: str
    background_prompt: Optional[str] = None

class SceneResponse(BaseModel):
    id: int
    project_id: int
    scene_index: int
    description: str
    background_prompt: Optional[str]
    background_path: Optional[str]
    created_at: str

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}