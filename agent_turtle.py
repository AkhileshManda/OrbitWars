"""
Orbit Wars - Turtle Agent

A highly defensive agent that hoards ships at home to defend.
It only launches an attack on the nearest unowned planet if the home planet's
garrison exceeds a safety threshold of 50 ships.

Strategy:
  For each owned planet:
    1. Check if the planet has more than 50 ships.
    2. If yes, locate the closest target planet (neutral or enemy).
    3. If we can afford to capture it (target garrison + 1 <= current ships), send the fleet.
    4. Otherwise, do nothing and keep defending.
"""

import math
from kaggle_environments.envs.orbit_wars.orbit_wars import Planet

# Minimum ships to maintain on a planet before launching attacks
DEFENSIVE_THRESHOLD = 50


def agent(obs):
    moves = []
    player = obs.get("player", 0) if isinstance(obs, dict) else obs.player
    raw_planets = obs.get("planets", []) if isinstance(obs, dict) else obs.planets

    planets = [Planet(*p) for p in raw_planets]
    my_planets = [p for p in planets if p.owner == player]
    targets = [p for p in planets if p.owner != player]

    if not my_planets or not targets:
        return moves

    for mine in my_planets:
        # Only consider launching if we have a massive defense buffer
        if mine.ships > DEFENSIVE_THRESHOLD:
            # Find nearest target planet
            nearest = min(
                targets,
                key=lambda t: math.sqrt((mine.x - t.x) ** 2 + (mine.y - t.y) ** 2)
            )
            
            ships_needed = nearest.ships + 1
            # Ensure we can afford it and still stay above defensive threshold or at least afford it
            if mine.ships >= ships_needed:
                angle = math.atan2(nearest.y - mine.y, nearest.x - mine.x)
                moves.append([mine.id, angle, ships_needed])

    return moves
