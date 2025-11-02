from fastapi import APIRouter, Depends
from modules.scene.service import SceneService
from core.middleware import is_authenticated

router = APIRouter(prefix="/projects", tags=["Scenes"])
scene_service = SceneService()


@router.post("/{project_id}/segment")
def segment_story(project_id: int, user: dict = Depends(is_authenticated)):
    return scene_service.segment_story(project_id, user["id"])
