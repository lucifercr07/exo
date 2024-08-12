import sys

from dao.memtier import create_bechmark_mt
from svc.memtier import parse_memtier_all_stats

execution_type = sys.argv[1]
database = sys.argv[2]
version = sys.argv[3]
filepath = sys.argv[4]

stats = parse_memtier_all_stats(filepath)
for kv_stat in stats:
    create_bechmark_mt("mt1", database, version, execution_type, kv_stat)
