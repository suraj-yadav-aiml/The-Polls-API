from typing import List
from pydantic import BaseModel


class Result(BaseModel):
    description: str
    vote_count: int

class PollResult(BaseModel):
    title: str
    total_votes: int
    result: List[Result]
