from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from entities.contributors import Contributor


class PullRequest(BaseModel):
    id: int
    owner: str
    repo: str
    contributor_id: int
    contributor_username: Optional[str] = None

    number: int
    title: str
    url: str
    merged_at: datetime
    issue_url: Optional[str] = None

    contributor: Optional[Contributor] = None
