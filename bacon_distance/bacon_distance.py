from typing import Optional
from collections import deque
from database import db


def get_shortest_path_length(start_actor: str, goal_actor: str) -> Optional[int]:
    if start_actor == goal_actor:
        return 0
    queue = deque([(start_actor, 0)])
    visited = {start_actor}
    while queue:
        actor, distance_to_start = queue.popleft()
        neighbors = db.get_actor_colleagues(actor)
        if goal_actor in neighbors:
            return distance_to_start + 1
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance_to_start + 1))
    return None


def get_bacon_distance(actor_name: str) -> Optional[int]:
    return get_shortest_path_length(actor_name, "Kevin Bacon")


def main() -> None:
    input_actor = input("Enter an actor's name: ")
    if not db.is_actor_in_database(input_actor):
        print(f"ERROR: {input_actor} is not in the database!")
        return
    bacon_distance = get_bacon_distance(input_actor)
    if bacon_distance is not None:
        print(f"The Bacon distance of {input_actor} is: {bacon_distance}")
    else:
        print(f"The Bacon distance of {input_actor} is: INFINITY")


if __name__ == "__main__":
    main()
