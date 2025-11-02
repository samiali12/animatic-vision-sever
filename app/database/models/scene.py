from sqlalchemy import Column, Integer, Text, ForeignKey, String, JSON
from sqlalchemy.orm import relationship
from database.session import base


class Scene(base):
    __tablename__ = "scenes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    scene_index = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    background_prompt = Column(Text)
    background_path = Column(String(500))
    character_prompts = Column(JSON, nullable=True)
    character_paths = Column(JSON, nullable=True)

    project = relationship("Project", back_populates="scenes")
