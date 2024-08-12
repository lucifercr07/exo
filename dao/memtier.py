from datetime import datetime
from typing import Dict, List

from db import connection_pool


def create_bechmark_mt(
    benchmark, database, version, execution_type, mt_stats: List[Dict]
):
    with connection_pool.connection() as conn:
        with conn.cursor() as cursor:
            query = """
            INSERT INTO benchmarks_mt (
                created_at, benchmark, database, version, execution_type, type,
                ops_per_sec, hits_per_sec, misses_per_sec, avg_latency,
                p50_latency, p99_latency, p99_9_latency, kb_per_sec
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            args = (
                datetime.now(),
                benchmark,
                database,
                version,
                execution_type,
                *mt_stats.values(),
            )
            cursor.execute(query, args)
            conn.commit()
