import os
from datetime import datetime

import matplotlib.pyplot as plt
import mpld3
from jinja2 import Environment, FileSystemLoader

from db import connection_pool

jinja_env = Environment(loader=FileSystemLoader("./templates"))


def fetch_latency_data(database):
    with connection_pool.connection() as conn:
        with conn.cursor() as cursor:
            query = """
                SELECT created_at, avg_latency, p50_latency, p99_latency, p99_9_latency, type, database, version
                FROM benchmarks_mt WHERE database = %s
                ORDER BY created_at;
            """
            cursor.execute(query, (database,))
            data = cursor.fetchall()

            return data


def plot_latency_data(redis_data, dicedb_data):
    redis_g_created_at = [row[0] for row in redis_data if row[5] == "Gets"]
    redis_g_avg_latency = [row[1] for row in redis_data if row[5] == "Gets"]
    redis_g_p50_latency = [row[2] for row in redis_data if row[5] == "Gets"]
    redis_g_p99_latency = [row[3] for row in redis_data if row[5] == "Gets"]
    redis_g_p99_9_latency = [row[4] for row in redis_data if row[5] == "Gets"]

    dicedb_g_created_at = [row[0] for row in dicedb_data if row[5] == "Gets"]
    dicedb_g_avg_latency = [row[1] for row in dicedb_data if row[5] == "Gets"]
    dicedb_g_p50_latency = [row[2] for row in dicedb_data if row[5] == "Gets"]
    dicedb_g_p99_latency = [row[3] for row in dicedb_data if row[5] == "Gets"]
    dicedb_g_p99_9_latency = [row[4] for row in dicedb_data if row[5] == "Gets"]

    redis_s_created_at = [row[0] for row in redis_data if row[5] == "Sets"]
    redis_s_avg_latency = [row[1] for row in redis_data if row[5] == "Sets"]
    redis_s_p50_latency = [row[2] for row in redis_data if row[5] == "Sets"]
    redis_s_p99_latency = [row[3] for row in redis_data if row[5] == "Sets"]
    redis_s_p99_9_latency = [row[4] for row in redis_data if row[5] == "Sets"]

    dicedb_s_created_at = [row[0] for row in dicedb_data if row[5] == "Sets"]
    dicedb_s_avg_latency = [row[1] for row in dicedb_data if row[5] == "Sets"]
    dicedb_s_p50_latency = [row[2] for row in dicedb_data if row[5] == "Sets"]
    dicedb_s_p99_latency = [row[3] for row in dicedb_data if row[5] == "Sets"]
    dicedb_s_p99_9_latency = [row[4] for row in dicedb_data if row[5] == "Sets"]

    fig, axs = plt.subplots(2, 2, figsize=(16, 9), tight_layout=True)
    axs[0, 0].plot(
        redis_g_created_at, redis_g_avg_latency, label="Redis Avg Latency - GET"
    )
    axs[0, 1].plot(
        redis_g_created_at, redis_g_p50_latency, label="Redis P50 Latency - GET"
    )
    axs[1, 0].plot(
        redis_g_created_at, redis_g_p99_latency, label="Redis P99 Latency - GET"
    )
    axs[1, 1].plot(
        redis_g_created_at, redis_g_p99_9_latency, label="Redis P99.9 Latency - GET"
    )

    axs[0, 0].plot(
        dicedb_g_created_at, dicedb_g_avg_latency, label="DiceDB Avg Latency - GET"
    )
    axs[0, 1].plot(
        dicedb_g_created_at, dicedb_g_p50_latency, label="DiceDB P50 Latency - GET"
    )
    axs[1, 0].plot(
        dicedb_g_created_at, dicedb_g_p99_latency, label="DiceDB P99 Latency - GET"
    )
    axs[1, 1].plot(
        dicedb_g_created_at, dicedb_g_p99_9_latency, label="DiceDB P99.9 Latency - GET"
    )

    axs[0, 0].plot(
        redis_s_created_at, redis_s_avg_latency, label="Redis Avg Latency - SET"
    )
    axs[0, 1].plot(
        redis_s_created_at, redis_s_p50_latency, label="Redis P50 Latency - SET"
    )
    axs[1, 0].plot(
        redis_s_created_at, redis_s_p99_latency, label="Redis P99 Latency - SET"
    )
    axs[1, 1].plot(
        redis_s_created_at, redis_s_p99_9_latency, label="Redis P99.9 Latency - SET"
    )

    axs[0, 0].plot(
        dicedb_s_created_at, dicedb_s_avg_latency, label="DiceDB Avg Latency - SET"
    )
    axs[0, 1].plot(
        dicedb_s_created_at, dicedb_s_p50_latency, label="DiceDB P50 Latency - SET"
    )
    axs[1, 0].plot(
        dicedb_s_created_at, dicedb_s_p99_latency, label="DiceDB P99 Latency - SET"
    )
    axs[1, 1].plot(
        dicedb_s_created_at, dicedb_s_p99_9_latency, label="DiceDB P99.9 Latency - SET"
    )

    axs[0, 0].set_xlabel("Created At")
    axs[0, 0].set_ylabel("Latency (ms)")
    axs[0, 0].set_title("Avg Latency Over Time")
    axs[0, 0].legend()
    axs[0, 0].grid(False)

    axs[0, 1].set_xlabel("Created At")
    axs[0, 1].set_ylabel("Latency (ms)")
    axs[0, 1].set_title("P50 Latency Over Time")
    axs[0, 1].legend()
    axs[0, 1].grid(False)

    axs[1, 0].set_xlabel("Created At")
    axs[1, 0].set_ylabel("Latency (ms)")
    axs[1, 0].set_title("P99 Latency Over Time")
    axs[1, 0].legend()
    axs[1, 0].grid(False)

    axs[1, 1].set_xlabel("Created At")
    axs[1, 1].set_ylabel("Latency (ms)")
    axs[1, 1].set_title("P99.9 Latency Over Time")
    axs[1, 1].legend()
    axs[1, 1].grid(False)

    return mpld3.fig_to_html(fig)


def main(dirpath):
    redis_data = fetch_latency_data("redis")
    dicedb_data = fetch_latency_data("dicedb")
    template = jinja_env.get_template("memtier.html")
    rendered_html = template.render(
        mt1=plot_latency_data(redis_data, dicedb_data),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    filepath = os.path.join(dirpath, "memtier.html")
    with open(filepath, "w") as f:
        f.write(rendered_html)


if __name__ == "__main__":
    main("/home/arpit/dicedb/docs/public/metrics")
