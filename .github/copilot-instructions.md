# Copilot instructions for PYc-Man

Short summary
- Single-file Pygame Pac-Man clone: the entire game logic lives in `pacman.py`.
- No build system or tests. Runtime is Python + pygame. Scores are stored in `ranking.txt`.

Entrypoint / how to run
- Ensure Python 3.8+ is installed and `pygame` is available: `pip install pygame`.
- From the project root (where `pacman.py` is), run (PowerShell):

```powershell
python .\pacman.py
```

High-level architecture (big picture)
- `pacman.py` contains all components: configuration constants, maze data, utility helpers, entity classes (Pacman and RedGhost), drawing/HUD, and the main loop.
- The maze is defined as `raw` (list of strings). `1` = wall, `0` = floor. `maze` is a 2D list derived from `raw`.
- Pellets are computed by `build_pellets()` and stored as a set of tile coordinates `{(x,y), ...}`.
- Movement and collision are handled in pixel space using helper functions: `tile_center`, `px_to_tile`, and `point_is_wall`.

Key files and symbols
- `pacman.py` — everything. Key functions/classes to inspect:
  - `build_pellets()` — creates the pellets set from the `maze`.
  - `tile_center(tx,ty)`, `px_to_tile(px,py)`, `point_is_wall(px,py)` — coordinate helpers used across movement and collision checks.
  - `Pacman` class — `move`, `tile`, `draw` methods; uses a circle-radii-based collision test against walls.
  - `RedGhost` class — `bfs(start,goal)`, `update(pac_pos)`, `draw`; BFS runs on tiles (uses `collections.deque`).
  - `game_loop()` — main tick/update/draw loop; also does pellet pickup and collision (life loss) handling.
  - `start_screen()` / `game_over_screen()` — simple blocking menus using Pygame event loop.

Project-specific patterns and gotchas (do not assume defaults)
- Maze size and constants: `WIDTH`, `HEIGHT`, `TILE`, `COLS`, `ROWS`, and `raw` must be consistent. `raw` currently defines 20 columns × 16 rows; changing TILE without updating WIDTH/HEIGHT or `raw` will break layout.
- Coordinates: the code mixes tile coordinates (integers) and pixel coordinates (float). Use `px_to_tile` and `tile_center` to convert reliably.
- Collision checks use four corner points of the entity's bounding circle (see `Pacman.move` and `RedGhost.update`). When adjusting `radius` or `speed`, be mindful of these checks — too-large radii will block movement in corridors.
- Ghost pathfinding: `RedGhost.bfs` computes a full tile path but `update` truncates it to at most 2 tiles (`if len(self.path) > 2: self.path = self.path[:2]`) and recomputes at most once per second (`self.last_calc`). To change ghost behavior, edit `last_calc` threshold and/or truncation.
- Reset logic: when Pac-Man loses a life, the code searches for the first `0` tile from top-left for Pac and bottom-right for ghost to place them. This is deterministic and simple — modifying startup positions should follow the same pattern.

Developer workflows and debugging tips
- Run quickly: `python .\pacman.py`. No tests or CI configured.
- To debug movement or pathfinding:
  - Print helpers: log `pac.tile()`, `ghost.path` inside `RedGhost.update` to observe tile targets.
  - Toggle FPS: modify `FPS` at the top to slow the game for step-through debugging.
  - Temporarily increase `RedGhost.last_calc` or set `RedGhost.speed` to 0 to inspect BFS output without movement.
- To edit maze layout: update `raw` (list of strings). Each string must use only `1` (wall) and `0` (floor) and match the expected column count (currently 20).

Integration points / external dependencies
- Only external dependency: `pygame`. No network or database integrations.
- `ranking.txt` stores simple plain-text score entries (example: `gloria | Score:52 | Tempo:24.51s`). Any feature that writes scores must preserve the file format or update other code that reads it (no reader exists in project code).

Conventions to follow when changing code
- Keep single-file structure unless you intentionally refactor: split files only if you update imports and verify `python pacman.py` still runs.
- Preserve coordinate helpers (`tile_center`, `px_to_tile`, `point_is_wall`) as the canonical conversions; callers across the file depend on their behavior.
- Any change to `TILE`, `WIDTH`, or `HEIGHT` should be accompanied by validating `COLS` and `ROWS` computed values and checking `raw` dimensions.

Examples (quick reference)
- Check pellet hit: in `game_loop` the code does `if (ptx, pty) in pellets:` then compares `abs(pac.x-cx) < TILE*0.45` to ensure Pac-Man has collected the pellet.
- Ghost pathing sample: `RedGhost.update` converts pixel positions into tiles with `start = px_to_tile(self.x, self.y)` and `goal = px_to_tile(*pac_pos)` then calls `bfs(start,goal)`.

If anything here is unclear or you want more detail (e.g., split into modules, add tests, or change AI), tell me which area to expand and I will update this file.
