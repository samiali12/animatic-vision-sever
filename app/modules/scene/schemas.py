# modules/scene/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SceneRequest(BaseModel):
    projectId: int

class SceneCreate(BaseModel):
    scene_index: int
    description: str
    background_prompt: Optional[str] = None

class SceneResponse(BaseModel):
    id: int
    description: str
    background_prompt: str | None

    model_config = {"from_attributes": True}