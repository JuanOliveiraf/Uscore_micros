from pydantic import BaseModel, Field, HttpUrl, constr
from typing import Optional, List

class Profile(BaseModel):
    user_id: constr(min_length=1)
    display_name: constr(min_length=1, max_length=120)
    bio: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    favorite_teams: List[str] = Field(default_factory=list)
    favorite_competitions: List[str] = Field(default_factory=list)
