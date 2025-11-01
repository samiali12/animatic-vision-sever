# backend/app/models/asset.py
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, JSON, func
from sqlalchemy.orm import relationship
from database.session import base
import enum


class AssetType(str, enum.Enum):
    background = "background"
    character = "character"
    audio = "audio"
    narration = "narration"
    subtitle = "subtitle"


class Asset(base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    type = Column(Enum(AssetType), nullable=False)
    file_path = Column(String(500), nullable=False)
    meta = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

    # ---- relationship back to Project ----
    project = relationship("Project", back_populates="assets")
