from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import List, Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from clients.http.dm_api_account.models.user_envelope import UserRole, Rating


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[UserDetails] = None
    metadata: Optional[Any] = None
    type: Optional[str] = None
    title: Optional[str] = None
    status: Optional[int] = None
    traceId: Optional[str] = None


class UserDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")
    login: Optional[str] = Field(None, description="Login")
    roles: List[UserRole]
    medium_picture_url: Optional[str] = Field(None, alias="mediumPictureUrl")
    small_picture_url: Optional[str] = Field(None, alias="smallPictureUrl")
    status: Optional[str] = Field(None)
    rating: Rating
    online: Optional[datetime] = Field(None)
    name: Optional[str] = Field(None)
    location: Optional[str] = Field(None)
    registration: Optional[datetime] = Field(None)
    icq: Optional[str] = Field(None)
    skype: Optional[str] = Field(None)
    original_picture_url: Optional[str] = Field(None, alias="originalPictureUrl")
    info: Optional[Any] = Field(None)
    settings: Optional[UserSettings] = None


class UserSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    color_schema: Optional[ColorSchema] = Field(None, alias="colorSchema")
    nanny_greetings_message: Optional[str] = Field(None, alias="nannyGreetingsMessage")
    paging: Optional[PagingSettings] = None


class ColorSchema(Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSIC_PALE = "ClassicPale"
    NIGHT = "Night"


class PagingSettings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    posts_per_page: Optional[int | None] = Field(None, alias="postsPerPage")
    comments_per_page: Optional[int | None] = Field(None, alias="commentsPerPage")
    topics_per_page: Optional[int | None] = Field(None, alias="topicsPerPage")
    messages_per_page: Optional[int | None] = Field(None, alias="messagesPerPage")
    entities_per_page: Optional[int | None] = Field(None, alias="entitiesPerPage")
