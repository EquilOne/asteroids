# AGENTS.md - Asteroids Game Development Guidelines

This file provides guidelines for agentic coding agents working on this Asteroids pygame game.

## Project Overview

- **Project type**: Python pygame game (Asteroids clone)
- **Python version**: 3.13 (see `.python-version`)
- **Main dependencies**: pygame==2.6.1
- **Dev dependencies**: ruff>=0.15.4
- **Package manager**: uv
- **Entry point**: `main.py`
- **Structure**: one class per file, flat directory (no src subdirectory)

## Build/Lint/Test Commands

### Running the Game

```bash
uv run python main.py
```

The game sets `SDL_VIDEODRIVER=wayland` at runtime in `main.py`.

### Linting and Formatting

```bash
# Check for lint errors
uv run ruff check .

# Auto-fix lint errors where possible
uv run ruff check --fix .

# Format all files
uv run ruff format .

# Check formatting without writing changes
uv run ruff format --check .
```

All files are pre-formatted. `ruff check .` currently reports 16 known errors —
see the **Known Lint Issues** section before adding to them.

### Testing

No test framework is configured. If adding tests, use pytest:

```bash
uv add --dev pytest

# Run all tests
uv run pytest

# Run a specific test file
uv run pytest tests/test_player.py

# Run a single test function
uv run pytest tests/test_player.py::test_player_shoot

# Run tests matching a name pattern
uv run pytest -k "test_shoot"
```

### Known Lint Issues

These are pre-existing — do not add more:

- `asteroidfield.py`: uses `from constants import *` (F403/F405) — should be
  replaced with explicit imports
- `main.py`: `asteroid_field` and `score` assigned but flagged as unused (F841)
  because they are WIP

## Code Style Guidelines

### General Principles

- Keep code simple and readable
- Follow existing patterns in the codebase
- No comments unless explaining non-obvious logic
- Prefer explicit over implicit
- Prefer guard clauses over nested conditionals

### Naming Conventions

- **Classes**: PascalCase (`Player`, `Asteroid`, `CircleShape`)
- **Functions/variables**: snake_case (`shot_cooldown`, `spawn_timer`)
- **Constants**: UPPER_SNAKE_CASE (`SCREEN_WIDTH`, `PLAYER_SPEED`)
- **Files**: snake_case (`asteroid.py`, `circleshape.py`)

### Import Ordering

Use explicit named imports. Never use wildcard imports (`from module import *`).
Ruff enforces import ordering — run `ruff check --fix .` to auto-sort.

```python
# 1. Standard library
import os
import random

# 2. Third-party
import pygame
import pygame.freetype

# 3. Local
from circleshape import CircleShape
from constants import PLAYER_RADIUS, SCREEN_WIDTH
from player import Player
```

### Type Annotations

The codebase has minimal type annotations. When adding them, annotate function
signatures but don't over-annotate obvious local variables:

```python
def move(self, dt: float) -> None:
    ...

def rotate(self, dt: float) -> float:
    return self.rotation
```

### Class Structure and Patterns

#### Sprite Inheritance

Game objects inherit from `CircleShape` → `pygame.sprite.Sprite`.
HUD elements inherit directly from `pygame.sprite.Sprite`.
Every game object class must implement `draw(self, screen)` and `update(self, dt)`.

#### Container Pattern

Sprite group membership is set via class-level `containers` before instantiation,
assigned in `main.py`. Classes that inherit directly from `pygame.sprite.Sprite`
(not via `CircleShape`) must replicate the `hasattr` guard in `__init__`:

```python
# In main.py before instantiating:
Player.containers = (updatable, drawable)

# In __init__ of direct pygame.sprite.Sprite subclasses:
if hasattr(self, "containers"):
    super().__init__(self.containers)
else:
    super().__init__()
```

#### HUD Elements

`HUDElement` is the base class for all on-screen UI (score, lives, etc.).
Subclass it for specific elements. Use `screen.get_rect()` and its named anchor
attributes for positioning — do not hardcode pixel coordinates:

```python
screen_rect = screen.get_rect()
# Available anchors: topleft, topright, bottomleft, bottomright,
#                    midtop, midbottom, midleft, midright, center

text_surface, text_rect = self.font.render(self.text, self.color)
setattr(text_rect, self.anchor, getattr(screen_rect, self.anchor))
screen.blit(text_surface, text_rect)
```

Note: `pygame.freetype.Font.render()` returns a `(Surface, Rect)` tuple, not
just a Surface.

### Constants (`constants.py`)

All game-wide constants live here. `LazyFont` defers font initialization until
after `pygame.init()` is called — never instantiate `pygame.freetype.Font` at
module level outside of `LazyFont`:

```python
# Correct — deferred initialization
DEFAULT_FONT = LazyFont(32)

# Wrong — crashes at import time if pygame not yet initialized
DEFAULT_FONT = pygame.freetype.Font(None, 32)
```

### Pygame-Specific Patterns

- Use `pygame.Vector2` for all 2D positions and velocities
- Screen origin `(0, 0)` is top-left; Y increases downward
- Delta time `dt` is in seconds: `clock.tick(60) / 1000`
- `draw(self, screen)` receives the screen `Surface` — use `pygame.draw.*` for
  shapes, `screen.blit(surface, rect)` for text/images

```python
# Movement with delta time
self.position += self.velocity * dt

# Direction vector from rotation angle
forward = pygame.Vector2(0, 1).rotate(self.rotation)
```

### Logging

`logger.py` exposes `log_state()` and `log_event(event_type)`. `log_state()` uses
stack inspection to read local variables from `main()` automatically — pass no
arguments. Logging stops after 16 seconds. Output files are gitignored.

```python
log_event("asteroid_shot")
log_event("player_hit")
```

### Error Handling

Catch specific exceptions. Use guard clauses to keep game logic flat:

```python
# Guard clause pattern
def shoot(self) -> None:
    if self.shot_cooldown > 0:
        return
    shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
    shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    self.shot_cooldown = PLAYER_SHOT_COOLDOWN_SECONDS
```

### Git Practices

- Atomic, focused commits
- Imperative mood: "Add score display" not "Added score display"
- Do not commit: `__pycache__/`, `*.pyc`, `game_state.jsonl`, `game_events.jsonl`, `.envrc`
