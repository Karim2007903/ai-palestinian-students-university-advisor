from typing import Optional
from pydantic import BaseModel


class University(BaseModel):
    id: str
    name: str
    country: str
    city: Optional[str] = None
    ranking_tier: Optional[int] = None
