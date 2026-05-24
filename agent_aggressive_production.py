"""
Orbit Wars - Aggressive Production Agent

A strategy focused on securing high-yield assets as quickly as possible. It
prioritizes capturing planets with high ship production rates, using proximity
as a tie-breaker.

Strategy:
  For each owned planet:
    1. Filter all targets (neutral or enemy planets).
    2. Sort targets by production (highest first), then by distance (closest first).
    3. Choose the first target in the sorted list that we have enough ships to capture (garrison + 1).
    4. Send exactly enough ships to guarantee capture.
"""

import math
from kaggle_environments.envs.orbit_wars.orbit_wars import Planet


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
        # Sort targets by production (descending) and then by Euclidean distance (ascending)
        sorted_targets = sorted(
            targets,
            key=lambda t: (
                -t.production,
                math.sqrt((mine.x - t.x) ** 2 + (mine.y - t.y) ** 2)
            )
        )

        for target in sorted_targets:
            ships_needed = target.ships + 1
            if mine.ships >= ships_needed:
                angle = math.atan2(target.y - mine.y, target.x - mine.x)
                moves.append([mine.id, angle, ships_needed])
                # Stop looking for targets for this planet once a launch is scheduled
                break

    return moves
