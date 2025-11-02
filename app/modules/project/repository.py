from database.session import session
from app.database.models.project import Project
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import DatabaseConnectionError


class ProjectRepository:
    def __init__(self):
        self.db = session()

    def create(
        self, user_id: int, title: str, story_text: str, duration_sec: int = 20
    ) -> Project:
        project = Project(
            user_id=user_id,
            title=title,
            story_text=story_text,
            duration_sec=duration_sec,
            status="draft",
        )
        try:
            self.db.add(project)
            self.db.commit()
            self.db.refresh(project)
            return project
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseConnectionError(detail=f"Failed to create project: {str(e)}")

    def get_by_id(self, project_id: int, user_id: int) -> Project | None:
        return (
            self.db.query(Project)
            .filter(Project.id == project_id, Project.user_id == user_id)
            .first()
        )

    def update_status(self, project: Project, status: str) -> Project:
        project.status = status
        try:
            self.db.add(project)
            self.db.commit()
            self.db.refresh(project)
            return project
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseConnectionError(detail=f"Failed to update status: {str(e)}")

    def delete(self, project: Project) -> None:
        try:
            self.db.delete(project)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseConnectionError(detail=f"Failed to delete project: {str(e)}")
