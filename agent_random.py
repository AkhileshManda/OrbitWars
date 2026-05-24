"""
Orbit Wars - Random Agent

A benchmark baseline agent that makes random moves.
This agent is useful as a lower bound for testing and comparing other strategies.
"""

import math
import random
from kaggle_environments.envs.orbit_wars.orbit_wars import Planet


def agent(obs):
    moves = []
    player = obs.get("player", 0) if isinstance(obs, dict) else obs.player
    raw_planets = obs.get("planets", []) if isinstance(obs, dict) else obs.planets

    planets = [Planet(*p) for p in raw_planets]
    my_planets = [p for p in planets if p.owner == player]
    all_targets = [p for p in planets if p.id not in [m.id for m in my_planets]]

    if not my_planets or not all_targets:
        return moves

    for mine in my_planets:
        # 15% chance to launch a fleet from this planet on any given turn
        if mine.ships > 1 and random.random() < 0.15:
            # Pick a random target planet
            target = random.choice(all_targets)
            
            # Send a random number of ships (at least 1, up to the total available)
            num_ships = random.randint(1, mine.ships)
            
            # Compute angle to target
            angle = math.atan2(target.y - mine.y, target.x - mine.x)
            moves.append([mine.id, angle, num_ships])

    return moves
