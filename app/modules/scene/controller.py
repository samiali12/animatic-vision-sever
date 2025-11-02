from fastapi import APIRouter, Depends
from modules.scene.service import SceneService
from core.middleware import is_authenticated
from modules.scene.schemas import SceneRequest

router = APIRouter(prefix="/projects", tags=["Scenes"])
scene_service = SceneService()


@router.post("/segment")
def segment_story(request: SceneRequest, user: dict = Depends(is_authenticated)):
    return scene_service.segment_story(request.projectId, user["id"])
