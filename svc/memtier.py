import re
from typing import Dict, List


def parse_memtier_all_stats(file_path) -> List[Dict[str, object]]:
    with open(file_path, "r") as file:
        lines = file.readlines()

    index = 0
    for idx, line in enumerate(lines):
        if "ALL STATS" in line:
            index = idx
            break

    data_lines = lines[index:]
    kv_pairs = []

    for line in data_lines:
        parts = re.split(r"\s{2,}", line.strip())
        if len(parts) >= 9:
            if parts[0] == "Type":
                continue
            kv_pairs.append(
                {
                    "type": parts[0] if parts[0] != "---" else None,
                    "ops_per_sec": parts[1] if parts[1] != "---" else None,
                    "hits_per_sec": parts[2] if parts[2] != "---" else None,
                    "misses_per_sec": parts[3] if parts[3] != "---" else None,
                    "avg_latency": parts[4] if parts[4] != "---" else None,
                    "p50_latency": parts[5] if parts[5] != "---" else None,
                    "p99_latency": parts[6] if parts[6] != "---" else None,
                    "p99_9_latency": parts[7] if parts[7] != "---" else None,
                    "kb_per_sec": parts[8] if parts[8] != "---" else None,
                }
            )
    return kv_pairs
