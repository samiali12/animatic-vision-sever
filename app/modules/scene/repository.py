from database.session import session
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import DatabaseConnectionError
from app.database.models.scene import Scene
from sqlalchemy.exc import SQLAlchemyError
from typing import List


class SceneRepository:
    def __init__(self):
        self.db = session()

    def create_many(self, scenes: List[dict], project_id: int):
        db_scenes = [
            Scene(
                project_id=project_id,
                scene_index=s["scene_index"],
                description=s["description"],
                background_prompt=s.get("background_prompt"),
            )
            for s in scenes
        ]
        try:
            self.db.add_all(db_scenes)
            self.db.commit()
            for s in db_scenes:
                self.db.refresh(s)
            return db_scenes
        except SQLAlchemyError as e:
            self.db.rollback()
            raise DatabaseConnectionError(detail=f"Failed to save scenes: {str(e)}")
