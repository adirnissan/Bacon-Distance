
from fastapi import FastAPI
from typing import Union
from bacon_distance import bacon_distance
from database import db
from math import inf

app = FastAPI()

@app.get("/bacon-distance/{actor_name}")
def get_bacon_distance(actor_name: str) -> Union[int, float]:
    
    if not db.is_actor_in_database(actor_name):
        return -1  # Actor not in database
    distance = bacon_distance.get_bacon_distance(actor_name)
    return distance if distance is not None else inf  # Return infinity if actor is not connected to Kevin Bacon
