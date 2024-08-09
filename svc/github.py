from typing import List

import requests

from config import GITHUB_TOKEN
from entities.contributors import Contributor
from entities.pull_requests import PullRequest


def get_contributor_github(username: str) -> Contributor:
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(
        f"https://api.github.com/users/{username}", headers=headers, timeout=10
    )
    response.raise_for_status()
    data = response.json()
    return Contributor(
        username=data["login"],
        id=data["id"],
        avatar=data["avatar_url"],
        url=data["html_url"],
        name=data["name"],
        blog=data["blog"],
        location=data["location"],
        twitter_username=data["twitter_username"],
    )


def get_merged_pull_requests_github(owner, repo, page=1) -> List[PullRequest]:
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    params = {
        "state": "closed",
        "sort": "updated",
        "base": "master",
        "direction": "desc",
        "page": page,
    }
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return [
        PullRequest(
            id=pr["id"],
            owner=owner,
            repo=repo,
            contributor_id=pr["user"]["id"],
            contributor_username=pr["user"]["login"],
            number=pr["number"],
            title=pr["title"],
            url=pr["html_url"],
            issue_url=pr["issue_url"],
            merged_at=pr["merged_at"],
        )
        for pr in response.json()
        if pr["merged_at"]
    ]
