# backend/app/models/scene.py
from sqlalchemy import Column, Integer, Text, ForeignKey, String
from sqlalchemy.orm import relationship
from database.session import base

class Scene(base):
    __tablename__ = "scenes"

    id               = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id       = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    scene_index      = Column(Integer, nullable=False)          # 0-based order
    description      = Column(Text, nullable=False)             # AI-generated text
    background_prompt = Column(Text)                            # prompt sent to image model
    background_path  = Column(String(500))                     # generated BG file

    project = relationship("Project", back_populates="scenes")
