from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class ChoiceCreate(BaseModel):
    """Choice write data model, representing a single choice ina poll"""
    description: str = Field(min_length=1, max_length=100)

class Choice(ChoiceCreate):
    """Choice read model, with an label and auot-gen uuid"""
    id: UUID = Field(default_factory=uuid4)
    label: int = Field(ge=1, le=5)


