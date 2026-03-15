import pandas as pd
import yaml
from pathlib import Path

NAMES_URL = "https://datasets.imdbws.com/name.basics.tsv.gz"
TITLES_URL = "https://datasets.imdbws.com/title.basics.tsv.gz"
PRINCIPALS_URL = "https://datasets.imdbws.com/title.principals.tsv.gz"

local_database_path = Path("bacon_distance") / Path("database") / Path("database.yaml")


def generate_database():

    database = {"actors": {}, "movies": {}}

    titles = pd.read_table(
        TITLES_URL,
        compression="gzip",
        usecols=["tconst", "primaryTitle", "titleType"],
        na_values="\\N",
    )

    movie_titles = titles[titles["titleType"] == "movie"][["tconst", "primaryTitle"]]

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

    merged = actors_principals.merge(movie_titles, on="tconst")
    merged = merged.merge(names, on="nconst")
    merged = merged.drop_duplicates(subset=["primaryTitle", "primaryName"])

    movie_to_actors = (
        merged.groupby("primaryTitle")["primaryName"].apply(list).to_dict()
    )

    actor_to_movies = (
        merged.groupby("primaryName")["primaryTitle"].apply(list).to_dict()
    )

    database["movies"] = {
        movie: {"actors": actors} for movie, actors in movie_to_actors.items()
    }

    database["actors"] = {
        actor: {"movies": movies} for actor, movies in actor_to_movies.items()
    }

    with open(local_database_path, "w", encoding="utf-8") as f:
        yaml.dump(database, f, allow_unicode=True)


if __name__ == "__main__":
    generate_database()
