from psycopg_pool import ConnectionPool

from config import DB_HOST, DB_NAME, DB_PASS, DB_USER

connection_pool = ConnectionPool(
    min_size=1,
    max_size=7,
    conninfo=f"dbname={DB_NAME} user={DB_USER} password={DB_PASS} host={DB_HOST} sslmode=require",
)
