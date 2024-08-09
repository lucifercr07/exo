from typing import Optional

from pydantic import BaseModel


class PullRequest(BaseModel):
    id: int
    owner: str
    repo: str
    contributor_id: int
    contributor_username: str

    number: int
    title: str
    url: str
    merged_at: str
    issue_url: Optional[str] = None
