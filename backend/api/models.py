# This module contains all database models.

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import datetime


class AccessToken(Base):
    """Model for storing user's access token."""

    __tablename__ = "token"

    id = Column(String, primary_key=True, index=True)
    access_token = Column(String)
    refresh_token = Column(String)
    # date_added = Column(DateTime(timezone=True), datetime.datetime.now())


class TiktokRepliedComments(Base):
    """Model for storing tiktok comments"""
    __tablename__ = "tiktokcomments"

    comment_id = Column(String(80), primary_key=True, index=True)
    video_id = Column(String(80))
    date_added = Column(DateTime(timezone=True), server_default=func.now())
