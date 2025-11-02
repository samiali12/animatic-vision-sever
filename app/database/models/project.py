from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship
from database.session import base
import enum


class ProjectStatus(str, enum.Enum):
    draft = "draft"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class Project(base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(200), nullable=False)
    story_text = Column(Text, nullable=False)
    duration_sec = Column(Integer, default=20)  # 20 or 30
    status = Column(Enum(ProjectStatus), default=ProjectStatus.draft)
    video_path = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="projects")
    scenes = relationship(
        "Scene", back_populates="project", cascade="all, delete-orphan"
    )
    assets = relationship(
        "Asset", back_populates="project", cascade="all, delete-orphan"
    )
