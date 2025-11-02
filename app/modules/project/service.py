# backend/app/modules/project/service.py
from modules.project.repository import ProjectRepository
from core.response import ApiResponse
from core.exceptions import HTTPException
from app.database.models.project import Project
from typing import Any
from modules.project.schemas import ProjectResponse


class ProjectService:
    def __init__(self):
        self.repo = ProjectRepository()

    def create_project(
        self, user_id: int, title: str, story_text: str, duration_sec: int = 20
    ) -> ApiResponse:
        try:
            project: Project = self.repo.create(
                user_id=user_id,
                title=title,
                story_text=story_text,
                duration_sec=duration_sec,
            )

            project_response = ProjectResponse(
                id=project.id,
                title=project.title,
                story_text=project.story_text,
                duration_sec=project.duration_sec,
                status=project.status,
                video_path=project.video_path,
                created_at=str(project.created_at),
                updated_at=str(project.updated_at),
            )

            return ApiResponse(
                message="Project created successfully",
                status_code=201,
                data=project_response,
            )
        except Exception as e:
            return ApiResponse.error(message=str(e), status_code=500)

    def get_projects(self, user_id: int) -> ApiResponse:
        try:
            projects = self.repo.get_projects(user_id)
            return ApiResponse(
                message="Project retrieved successfully",
                status_code=200,
                data=[p.__dict__ for p in projects],
            )
        except Exception as e:
            return ApiResponse.error(message=str(e), status_code=500)

    def get_project(self, project_id: int, user_id: int) -> ApiResponse:
        try:
            project: Project | None = self.repo.get_by_id(
                project_id=project_id, user_id=user_id
            )
            if not project:
                return ApiResponse.error(
                    message="Project not found or access denied", status_code=404
                )

            project_format = {
                "id": project.id,
                "title": project.title,
                "story_text": project.story_text,
                "duration_sec": project.duration_sec,
                "status": project.status,
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat(),
                "video_path": project.video_path,
                "scenes": (
                    [
                        {
                            "id": s.id,
                            "description": s.description,
                            "background_prompt": s.background_prompt,
                            "background_path": s.background_path,
                            "character_prompts": s.character_prompts or [],
                            "character_paths": s.character_paths or [],
                        }
                        for s in project.scenes
                    ]
                    if project.scenes
                    else []
                ),
            }

            return ApiResponse(
                message="Project retrieved successfully",
                status_code=200,
                data=project_format,
            )
        except Exception as e:
            return ApiResponse.error(message=str(e), status_code=500)

    def update_project_status(self, project: Project, new_status: str) -> ApiResponse:
        try:
            updated_project: Project = self.repo.update_status(
                project=project, status=new_status
            )
            return ApiResponse(
                message=f"Project status updated to '{new_status}'",
                status_code=200,
                data=updated_project.__dict__,
            )
        except Exception as e:
            return ApiResponse.error(message=str(e), status_code=500)

    def delete_project(self, project: Project) -> ApiResponse:
        try:
            self.repo.delete(project)
            return ApiResponse(
                message="Project deleted successfully", status_code=200, data=None
            )
        except Exception as e:
            return ApiResponse.error(message=str(e), status_code=500)
