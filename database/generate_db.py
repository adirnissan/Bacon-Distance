import pandas as pd
import sqlite3
from pathlib import Path

NAMES_URL = "https://datasets.imdbws.com/name.basics.tsv.gz"
TITLES_URL = "https://datasets.imdbws.com/title.basics.tsv.gz"
PRINCIPALS_URL = "https://datasets.imdbws.com/title.principals.tsv.gz"


LOCAL_DB_PATH = Path("database") / "database.db"


def create_tables(cursor) -> None:
    cursor.execute("DROP TABLE IF EXISTS movies")
    cursor.execute("DROP TABLE IF EXISTS actors")
    cursor.execute("DROP TABLE IF EXISTS roles")
    cursor.execute("""
    CREATE TABLE movies (
        id TEXT PRIMARY KEY,
        title TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE actors (
        id TEXT PRIMARY KEY,
        name TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE roles (
        actor_id TEXT,
        movie_id TEXT,
        FOREIGN KEY(actor_id) REFERENCES actors(id),
        FOREIGN KEY(movie_id) REFERENCES movies(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE colleagues (
        actor1_name TEXT,
        actor2_name TEXT,
        FOREIGN KEY(actor1_name) REFERENCES actors(name),
        FOREIGN KEY(actor2_name) REFERENCES actors(name)
    )
    """)


def generate_database() -> None:
    conn = sqlite3.connect(LOCAL_DB_PATH)
    cursor = conn.cursor()
    create_tables(cursor)

    titles = pd.read_table(
        TITLES_URL,
        compression="gzip",
        usecols=["tconst", "primaryTitle", "titleType", "startYear"],
        na_values="\\N",
    )

    movie_titles = titles[
        (titles["titleType"] == "movie") & (titles["startYear"] >= 1970)
    ][["tconst", "primaryTitle"]]

    principals = pd.read_table(
        PRINCIPALS_URL,
        compression="gzip",
        usecols=["tconst", "nconst", "category"],
        na_values="\\N",
    )

    actors_principals = principals[principals["category"].isin(["actor", "actress"])][
        ["tconst", "nconst"]
    ]

    names = pd.read_table(
        NAMES_URL,
        compression="gzip",
        usecols=["nconst", "primaryName"],
        na_values="\\N",
    )

    merged = (
        actors_principals.merge(movie_titles, on="tconst")
        .merge(names, on="nconst")
        .drop_duplicates(subset=["primaryTitle", "primaryName"])
    )

    actors = merged[["nconst", "primaryName"]].drop_duplicates()
    movies = merged[["tconst", "primaryTitle"]].drop_duplicates()

    cursor.executemany(
        "INSERT INTO actors (id, name) VALUES (?, ?)",
        [
            (actor_id, name)
            for actor_id, name in zip(actors["nconst"], actors["primaryName"])
        ],
    )

    cursor.executemany(
        "INSERT INTO movies (id, title) VALUES (?, ?)",
        [
            (movie_id, title)
            for movie_id, title in zip(movies["tconst"], movies["primaryTitle"])
        ],
    )

    cursor.executemany(
        "INSERT INTO roles (actor_id, movie_id) VALUES (?, ?)",
        [
            (actor_id, movie_id)
            for actor_id, movie_id in zip(merged["nconst"], merged["tconst"])
        ],
    )

    cursor.execute("CREATE INDEX idx_actor ON roles(actor_id)")
    cursor.execute("CREATE INDEX idx_movie ON roles(movie_id)")

    conn.commit()

    cursor.execute("""
    INSERT INTO colleagues (actor1_name, actor2_name)
    SELECT DISTINCT a1.name, a2.name
    FROM actors a1 JOIN roles r1 ON a1.id = r1.actor_id
    JOIN roles r2 ON r1.movie_id = r2.movie_id
    JOIN actors a2 ON r2.actor_id = a2.id
    WHERE a1.name != a2.name
    """)

    cursor.execute("CREATE INDEX idx_colleague1 ON colleagues(actor1_name)")
    cursor.execute("CREATE INDEX idx_colleague2 ON colleagues(actor2_name)")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    generate_database()
