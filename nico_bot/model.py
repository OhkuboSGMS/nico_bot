from typing import Optional

from sqlmodel import SQLModel, Field


class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    end: bool = False
