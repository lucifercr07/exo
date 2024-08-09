from typing import Optional

from pydantic import BaseModel


class Contributor(BaseModel):
    id: int
    username: str
    avatar: str
    url: str
    name: Optional[str] = None
    blog: Optional[str] = None
    location: Optional[str] = None
    twitter_username: Optional[str] = None
