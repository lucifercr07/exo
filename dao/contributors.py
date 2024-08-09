import loguru

from db import connection_pool
from entities.contributors import Contributor


def create_contributor(contributor: Contributor):
    loguru.logger.info(f"creating contributor in the database: {contributor.username}")
    with connection_pool.connection() as conn:
        with conn.cursor() as cursor:
            query = """
                    INSERT INTO contributors (id, username, avatar, url, name, blog, location, twitter_username)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
            cursor.execute(
                query,
                (
                    contributor.id,
                    contributor.username,
                    contributor.avatar,
                    contributor.url,
                    contributor.name,
                    contributor.blog,
                    contributor.location,
                    contributor.twitter_username,
                ),
            )
            conn.commit()


def get_contributor(contributor_id: int) -> Contributor:
    with connection_pool.connection() as conn:
        with conn.cursor() as cursor:
            query = """
                    SELECT c.id, c.username, c.avatar, c.url, c.name,
                        c.blog, c.location, c.twitter_username
                        FROM contributors c WHERE id = %s"""
            cursor.execute(query, (contributor_id,))
            result = cursor.fetchone()
            if result:
                return Contributor(
                    id=result[0],
                    username=result[1],
                    avatar=result[2],
                    url=result[3],
                    name=result[4],
                    blog=result[5],
                    location=result[6],
                    twitter_username=result[7],
                )
            return None
