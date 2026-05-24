# Orbit Wars

Conquer planets rotating around a central sun in continuous 2D space. Orbit Wars is a real-time strategy game for 2 or 4 players.

---

## Game Overview

- **Board**: A 100x100 continuous grid with a Sun at the center `(50, 50)`.
- **Planets**: Produce ships each turn (proportional to their radius).
  - *Inner planets* rotate around the central Sun.
  - *Outer planets* remain static.
- **Fleets**: Fly in straight lines from a source planet to a destination at a target angle.
- **Fleet Speed**: Scales logarithmically with fleet size (1 ship moves at speed 1.0, up to a maximum speed of 6.0 for large fleets).
- **Sun Collision**: Any fleet that passes through or hits the Sun's radius (10.0 units) is immediately destroyed.
- **Comets**: Elliptical, fast-moving temporary planets that spawn at steps 50, 150, 250, 350, and 450, and eventually leave the board.
- **Combat**: Resolved when fleets collide with a planet. Arriving fleets are grouped by owner; the largest force fights the second-largest, and survivors fight the planet's garrison.
- **Scoring**: Final Score = Total ships on owned planets + total ships in active fleets at step 500. Highest score wins!

---

## Project Development Rules (For Humans and LLMs)

To ensure repository cleanliness, reliable benchmarks, and easy local testing, follow these rules:

1. **Modular Strategy Files**:
   - Write every new algorithm or agent strategy in its own Python file at the root directory: `agent_<strategy_name>.py` (e.g., `agent_nearest_neutral.py`).
   - Do NOT overwrite `main.py` unless you are explicitly preparing a final submission for Kaggle. Keep `main.py` clean or synchronized with your top-performing agent.

2. **Jupyter Notebook testing**:
   - Test all new algorithms locally using the Jupyter notebook **`wdstf.ipynb`**.
   - Import and test agents against each other to evaluate performance, visualize matches, and run experiments.
   - Do NOT commit large generated output cells or intermediate outputs back to the remote repository. Keep the notebook clean.
   - The file `wdstf.ipynb` is Git-ignored (`.gitignore`) to keep the repository size small and fast. Do NOT force-track it.

3. **Agent Interface**:
   - Every agent file must define a function `agent(obs)` that takes an observation (either a dictionary or object) and returns a list of moves.
   - Example Move format: `[[from_planet_id, direction_angle, num_ships], ...]`.
   - Utilize standard named tuples from `kaggle_environments.envs.orbit_wars.orbit_wars` for clean code:
     ```python
     from kaggle_environments.envs.orbit_wars.orbit_wars import Planet, Fleet
     ```

---

## Benchmark Agents List

Here are the trivial and baseline agents available in this repository:

- **`main.py`**: Nearest Planet Sniper (baseline). Captures the nearest planet we don't own if we have enough ships.
- **`agent_random.py`**: A fully random agent useful as a baseline lower bound.
- **`agent_nearest_neutral.py`**: Focuses on quick, uncontested expansion by targeting neutral planets (`owner == -1`) first.
- **`agent_aggressive_production.py`**: Targets high-production rate planets first to maximize ship production capacity quickly.
- **`agent_turtle.py`**: Defensive agent that hoards ships at home, only launching attacks when a planet has a massive surplus (garrison > 50).

---

## Quick Start & Verification

### Install Orbit Wars Environment
```bash
pip install "kaggle-environments>=1.28.0"
```

### Run a Local Match
You can run a local match between two agents from your shell:
```bash
python -c "
from kaggle_environments import make
env = make('orbit_wars', debug=True)
env.run(['agent_nearest_neutral.py', 'main.py'])
print([(i, s.reward) for i, s in enumerate(env.steps[-1])])
"
```
