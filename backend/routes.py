from fastapi import FastAPI, HTTPException
from typing import Optional, Dict, Union
from bacon_distance import bacon_distance
from database import db

app = FastAPI()


@app.get("/bacon-distance")
def get_bacon_distance(actor_name: str) -> Dict[str, Union[Optional[int], str]]:
    if not db.is_actor_in_database(actor_name):
        raise HTTPException(status_code=404, detail="Actor not found")
    distance = bacon_distance.get_bacon_distance(actor_name)
    return {"actor": actor_name, "bacon_distance": distance}
