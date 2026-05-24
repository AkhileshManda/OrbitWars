"""
Orbit Wars - Nearest Neutral Agent

An expansionist strategy that prioritizes conquering neutral planets first before
engaging with other players. This helps build a safe, strong economy.

Strategy:
  For each owned planet, find the closest neutral planet (owner == -1).
  If found and we have enough ships (garrison + 1), send exactly enough to capture it.
  If no neutral planets are available, fall back to targeting the closest enemy planet.
"""

import math
from kaggle_environments.envs.orbit_wars.orbit_wars import Planet


def agent(obs):
    moves = []
    player = obs.get("player", 0) if isinstance(obs, dict) else obs.player
    raw_planets = obs.get("planets", []) if isinstance(obs, dict) else obs.planets

    planets = [Planet(*p) for p in raw_planets]
    my_planets = [p for p in planets if p.owner == player]
    
    # Target separation
    neutral_targets = [p for p in planets if p.owner == -1]
    enemy_targets = [p for p in planets if p.owner != -1 and p.owner != player]

    if not my_planets:
        return moves

    for mine in my_planets:
        target = None
        min_dist = float("inf")

        # 1. Prioritize neutral planets first
        if neutral_targets:
            for t in neutral_targets:
                dist = math.sqrt((mine.x - t.x) ** 2 + (mine.y - t.y) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    target = t

        # 2. Fallback to enemy planets if no neutral planets are left
        if target is None and enemy_targets:
            for t in enemy_targets:
                dist = math.sqrt((mine.x - t.x) ** 2 + (mine.y - t.y) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    target = t

        if target is None:
            continue

        # Calculate ships needed to capture (target garrison + 1)
        ships_needed = target.ships + 1

        # Only launch if we can afford it to guarantee capture
        if mine.ships >= ships_needed:
            angle = math.atan2(target.y - mine.y, target.x - mine.x)
            moves.append([mine.id, angle, ships_needed])

    return moves
