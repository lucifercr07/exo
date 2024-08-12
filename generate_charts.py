from datetime import datetime

import matplotlib.pyplot as plt
import mpld3
from jinja2 import Environment, FileSystemLoader

from db import connection_pool

jinja_env = Environment(loader=FileSystemLoader("./templates"))


def fetch_latency_data():
    with connection_pool.connection() as conn:
        with conn.cursor() as cursor:
            query = """
                SELECT created_at, avg_latency, p50_latency, p99_latency, p99_9_latency
                FROM benchmarks_mt
                ORDER BY created_at;
            """
            cursor.execute(query)
            data = cursor.fetchall()

            return data


def plot_latency_data(data):
    created_at = [row[0] for row in data]
    avg_latency = [row[1] for row in data]
    p50_latency = [row[2] for row in data]
    p99_latency = [row[3] for row in data]
    p99_9_latency = [row[4] for row in data]

    fig, axs = plt.subplots(2, 2, figsize=(16, 9), tight_layout=True)
    axs[0, 0].plot(created_at, avg_latency, label="Avg Latency")
    axs[0, 1].plot(created_at, p50_latency, label="P50 Latency")
    axs[1, 0].plot(created_at, p99_latency, label="P99 Latency")
    axs[1, 1].plot(created_at, p99_9_latency, label="P99.9 Latency")

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


def main():
    data = fetch_latency_data()
    template = jinja_env.get_template("memtier.html")
    rendered_html = template.render(
        mt1=plot_latency_data(data),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )
    with open("memtier.html", "w") as f:
        f.write(rendered_html)


if __name__ == "__main__":
    main()
