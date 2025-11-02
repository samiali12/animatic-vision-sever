# backend/app/modules/project/controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from core.middleware import is_authenticated
from modules.project.service import ProjectService
from modules.project.schemas import ProjectCreate, ProjectStatusUpdate
from app.database.models.project import Project


router = APIRouter(prefix="/projects", tags=["Projects"])

def get_project_service():
    return ProjectService()

@router.post("/")
def create_project(
    request: ProjectCreate,
    user: dict = Depends(is_authenticated),
    service: ProjectService = Depends(get_project_service),
):
    return service.create_project(
        user_id=user["id"],
        title=request.title,
        story_text=request.story_text,
        duration_sec=request.duration_sec or 20,
    )

@router.get("/{project_id}")
def get_project(
    project_id: int,
    user: dict = Depends(is_authenticated),
    service: ProjectService = Depends(get_project_service),
):
    result = service.get_project(project_id=project_id, user_id=user["id"])
    if result.status_code != 200:
        raise HTTPException(status_code=result.status_code, detail=result.message)
    return result.data

@router.get("/")
def get_projects(
    user: dict = Depends(is_authenticated),
    service: ProjectService = Depends(get_project_service),
):
    result = service.get_projects(user_id=user["id"])
    if result.status_code != 200:
        raise HTTPException(status_code=result.status_code, detail=result.message)
    return result.data

@router.patch(
    "/{project_id}/status",
)
def update_project_status(
    project_id: int,
    request: ProjectStatusUpdate,
    user: dict = Depends(is_authenticated),
    service: ProjectService = Depends(get_project_service),
):
    project: Project | None = service.repo.get_by_id(
        project_id=project_id, user_id=user["id"]
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or you don't have access",
        )

    result = service.update_project_status(project=project, new_status=request.status)
    if result.status_code != 200:
        raise HTTPException(status_code=result.status_code, detail=result.message)
    return result.data


@router.delete(
    "/{project_id}",
)
def delete_project(
    project_id: int,
    user: dict = Depends(is_authenticated),
    service: ProjectService = Depends(get_project_service),
):
    project: Project | None = service.repo.get_by_id(
        project_id=project_id, user_id=user["id"]
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or you don't have access",
        )

    result = service.delete_project(project=project)
    if result.status_code != 200:
        raise HTTPException(status_code=result.status_code, detail=result.message)
    return None
