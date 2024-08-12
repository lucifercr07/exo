from typing import List

import loguru

from db import connection_pool
from entities.contributors import Contributor
from entities.pull_requests import PullRequest


def create_pull_request(pull_request: PullRequest):
    loguru.logger.info(
        f"creating pull request in the database: {pull_request.number} by {pull_request.contributor_username}"
    )
    with connection_pool.connection() as conn:
        with conn.cursor() as cursor:
            query = """
                    INSERT INTO pull_requests
                        (id, owner, repo, contributor_id, number, title, url, merged_at, issue_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;
                """
            cursor.execute(
                query,
                (
                    pull_request.id,
                    pull_request.owner,
                    pull_request.repo,
                    pull_request.contributor_id,
                    pull_request.number,
                    pull_request.title,
                    pull_request.url,
                    pull_request.merged_at,
                    pull_request.issue_url,
                ),
            )
            conn.commit()


def get_pull_request(pull_request_id: int) -> PullRequest:
    with connection_pool.connection() as conn:
        with conn.cursor() as cursor:
            query = """
                    SELECT number, html_url, issue_url, merged_at, title,
                    userid, username FROM pull_requests WHERE id = %s"""
            cursor.execute(query, (pull_request_id,))
            result = cursor.fetchone()
            if result:
                return PullRequest(
                    number=result[0],
                    html_url=result[1],
                    issue_url=result[2],
                    merged_at=result[3],
                    title=result[4],
                    userid=result[5],
                    username=result[6],
                )
            return None


def get_pull_requests(owner: str, repo: str) -> List[PullRequest]:
    with connection_pool.connection() as conn:
        with conn.cursor() as cursor:
            query = """
                    SELECT
                        p.id, p.owner, p.repo, p.number, p.title, p.url, p.merged_at, p.issue_url,
                        c.id, c.username, c.avatar, c.url, c.name, c.blog, c.location, c.twitter_username
                    FROM pull_requests p INNER JOIN contributors c ON p.contributor_id = c.id
                    WHERE p.owner = %s AND p.repo = %s AND p.merged_at >= NOW() - INTERVAL '8 days'
                    ORDER BY p.merged_at DESC
                    """
            cursor.execute(query, (owner, repo))
            results = cursor.fetchall()
            pull_requests = []
            for result in results:
                pull_requests.append(
                    PullRequest(
                        id=result[0],
                        owner=result[1],
                        repo=result[2],
                        number=result[3],
                        title=result[4],
                        url=result[5],
                        merged_at=result[6],
                        issue_url=result[7],
                        contributor_id=result[8],
                        contributor=Contributor(
                            id=result[8],
                            username=result[9],
                            avatar=result[10],
                            url=result[11],
                            name=result[12],
                            blog=result[13],
                            location=result[14],
                            twitter_username=result[15],
                        ),
                    )
                )
            return pull_requests
