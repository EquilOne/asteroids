# AGENTS.md - Asteroids Game Development Guidelines

Guidelines for agentic coding agents working on this Asteroids pygame game.

## Project Overview

- **Type**: Python pygame game (Asteroids clone)
- **Python**: 3.13 (see `.python-version`)
- **Dependencies**: pygame==2.6.1; dev: ruff>=0.15.4
- **Package manager**: uv
- **Entry point**: `main.py`
- **Structure**: one class per file, flat directory

## Build/Lint/Test Commands

### Running the Game
```bash
uv run python main.py
```
Sets `SDL_VIDEODRIVER=wayland` at runtime.

### Linting & Formatting
```bash
uv run ruff check .              # Check for lint errors
uv run ruff check --fix .        # Auto-fix errors
uv run ruff format .             # Format files
uv run ruff format --check .     # Check without writing
```

### Testing
No test framework configured. If adding tests, use pytest:
```bash
uv add --dev pytest
uv run pytest                               # Run all tests
uv run pytest tests/test_player.py          # Specific file
uv run pytest tests/test_player.py::test_shoot  # Single test
uv run pytest -k "test_shoot"               # Match pattern
```

### Known Lint Issues (Pre-existing — Do Not Add More)
- `asteroidfield.py`: wildcard import (F403/F405) — replace with explicit imports
- `main.py`: unused variables (F841) — `asteroid_field`, `score` are WIP

## Code Style Guidelines

### General Principles
- Simple, readable code
- Follow existing patterns
- No comments unless non-obvious
- Explicit over implicit
- Guard clauses over nested conditionals

### Naming Conventions
- **Classes**: PascalCase (`Player`, `Asteroid`)
- **Functions/variables**: snake_case (`shot_cooldown`)
- **Constants**: UPPER_SNAKE_CASE (`SCREEN_WIDTH`)
- **Files**: snake_case (`asteroid.py`)

### Imports
Use explicit named imports. Never use `from module import *`.
```python
# Standard library → Third-party → Local
import os
import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, SCREEN_WIDTH
```

### Type Annotations
Minimal annotations. Annotate function signatures only:
```python
def move(self, dt: float) -> None: ...
def rotate(self, dt: float) -> float: return self.rotation
```

### Class Patterns

**Sprite Inheritance**: Game objects inherit `CircleShape` → `pygame.sprite.Sprite`.
HUD elements inherit directly from `pygame.sprite.Sprite`.
Every class must implement `draw(self, screen)` and `update(self, dt)`.

**Container Pattern**: Set class-level `containers` before instantiation in `main.py`:
```python
Player.containers = (updatable, drawable)

# In __init__ of direct pygame.sprite.Sprite subclasses:
if hasattr(self, "containers"):
    super().__init__(self.containers)
else:
    super().__init__()
```

**HUD Elements**: Subclass `HUDElement`. Position using `screen.get_rect()` anchors:
```python
screen_rect = screen.get_rect()
text_surface, text_rect = self.font.render(self.text, self.color)
setattr(text_rect, self.anchor, getattr(screen_rect, self.anchor))
screen.blit(text_surface, text_rect)
```
Note: `pygame.freetype.Font.render()` returns `(Surface, Rect)`, not just Surface.

### Constants
All game-wide constants in `constants.py`. `LazyFont` defers initialization:
```python
DEFAULT_FONT = LazyFont(32)  # Correct — deferred
# Wrong: pygame.freetype.Font(None, 32)  # Crashes before pygame.init()
```

### Pygame Patterns
- Use `pygame.Vector2` for 2D positions/velocities
- Screen origin `(0, 0)` is top-left; Y increases downward
- Delta time `dt` in seconds: `clock.tick(60) / 1000`
- `draw()` receives screen Surface; use `pygame.draw.*` for shapes, `blit()` for text

```python
self.position += self.velocity * dt
forward = pygame.Vector2(0, 1).rotate(self.rotation)
```

### Logging & Error Handling
`log_state()` and `log_event(event_type)` in `logger.py`. `log_state()` auto-reads
locals from `main()`. Use guard clauses:
```python
def shoot(self) -> None:
    if self.shot_cooldown > 0: return
    shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
    shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    self.shot_cooldown = PLAYER_SHOT_COOLDOWN_SECONDS
```

### Git Practices
- Atomic, focused commits
- Imperative mood: "Add feature" not "Added feature"
- Do not commit: `__pycache__/`, `*.pyc`, `.jsonl` logs, `.envrc`
