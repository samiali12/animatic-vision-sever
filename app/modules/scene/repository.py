from database.session import session
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import DatabaseConnectionError
from app.database.models.scene import Scene
from app.database.models.project import Project
from sqlalchemy.exc import SQLAlchemyError
from typing import List


class SceneRepository:
    def __init__(self):
        self.db = session()

    def create_many(self, scenes: List[dict], project_id: int):
        db_project = self.db.query(Project).filter(Project.id == project_id).first()
        db_scenes = [
            Scene(
                project_id=project_id,
                scene_index=s["scene_index"],
                description=s["description"],
                background_prompt=s.get("background_prompt"),
                character_prompts=s["character_prompts"],
            )
            for s in scenes
        ]
        try:
            self.db.add_all(db_scenes)
            db_project.status = "segmented"
            self.db.commit()
            self.db.refresh(db_project)
            for s in db_scenes:
                self.db.refresh(s)
            return db_scenes
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseConnectionError(detail=f"Failed to save scenes: {str(e)}")
