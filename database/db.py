import sqlite3
from typing import Set
from pathlib import Path

LOCAL_DB_PATH = Path("database") / "database.db"


def is_actor_in_database(actor_name: str) -> bool:
    conn = sqlite3.connect(LOCAL_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM actors WHERE name = ?", (actor_name,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def get_actor_colleagues(actor_name: str) -> Set[str]:
    conn = sqlite3.connect(LOCAL_DB_PATH)
    cursor = conn.cursor()
    query = """
    SELECT DISTINCT actor2_name
    FROM colleagues
    WHERE actor1_name = ?
    """
    params = (actor_name,)
    cursor.execute(query, params)
    colleagues = {row[0] for row in cursor.fetchall()}
    conn.close()
    return colleagues
