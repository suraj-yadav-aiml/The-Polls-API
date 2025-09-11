import time
from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException
from fastapi import status
from uuid import UUID, uuid4
from typing import List, Optional
from datetime import datetime, timezone

from app.models.Choice import Choice
# from .Choice import Choice


class PollCreate(BaseModel):
    """Poll write data model"""
    title: str = Field(min_length=5, max_length=50)
    options: List[str]
    expires_at: Optional[datetime] = None

    @field_validator('options')
    @classmethod
    def validate_options(cls, v: List[str]) -> List[str]:
        if len(v) < 2 or len(v) > 5:
            raise  HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A poll must contain between 2 and 5 choices"
            )
        return v
    

    def create_poll(self):
        choices:List[Choice] =  [
            Choice(
                description=option_name, 
                label=idx 
            ) 
            for idx, option_name in enumerate(self.options, start=1)
        ]

        if self.expires_at is not None and self.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A Poll's expiration must in future"
            )

        return Poll(
            title=self.title,
            options=choices,
            expires_at=self.expires_at
        )




class Poll(PollCreate):
    """Poll read data model, with uuid and creation date"""
    id: UUID = Field(default_factory=uuid4)
    options: List[Choice]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def is_active(self) -> bool:
        if self.expires_at is None:
            return True
        
        return self.expires_at > datetime.now(timezone.utc)
    

