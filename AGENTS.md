# AGENTS.md - Asteroids Game Development Guidelines

Guidelines for agentic coding agents working on this Asteroids pygame game.

## Project Overview
- **Type**: Python pygame game (Asteroids clone)
- **Python**: 3.13 | **Dependencies**: pygame==2.6.1; dev: ruff>=0.15.4
- **Package manager**: uv | **Entry point**: `main.py`
- **Structure**: one class per file, flat directory

## Build/Lint/Test Commands
```bash
uv run python main.py           # Run game (sets SDL_VIDEODRIVER=wayland)
uv run ruff check .             # Check lint errors
uv run ruff check --fix .       # Auto-fix errors
uv run ruff format .            # Format files
uv run ruff format --check .   # Check without writing
# Testing (requires pytest installation):
uv add --dev pytest
uv run pytest --version        # Verify installation
uv run pytest tests/test_player.py::test_shoot  # Single test
```

### Known Lint Issues (Pre-existing — Do Not Add More)
- `asteroidfield.py`: wildcard import (F403/F405) — replace with explicit imports
- `main.py`: unused variables (F841) — `asteroid_field`, `score` are WIP

## Code Style Guidelines

Simple, readable code | Follow existing patterns | No comments unless non-obvious
Explicit over implicit | Guard clauses over nested conditionals

### Naming Conventions
- **Classes**: PascalCase (`Player`, `Asteroid`)
- **Functions/variables**: snake_case (`shot_cooldown`)
- **Constants**: UPPER_SNAKE_CASE (`SCREEN_WIDTH`)
- **Files**: snake_case (`asteroid.py`)

### Imports
Use explicit named imports. Never use `from module import *`.
```python
import os
import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, SCREEN_WIDTH
```

### Type Annotations
Minimal annotations on function signatures:
```python
def move(self, dt: float) -> None: ...
def rotate(self, dt: float) -> float: return self.rotation
```

### Class Patterns
Game objects inherit `CircleShape` → `pygame.sprite.Sprite`.
Set class-level `containers` before instantiation:
```python
Player.containers = (updatable, drawable)
if hasattr(self, "containers"):
    super().__init__(self.containers)
else:
    super().__init__()
```
Every class must implement `draw(self, screen)` and `update(self, dt)`.

**HUD Elements**: Subclass `HUDElement`. Use `screen.get_rect()` anchors:
```python
screen_rect = screen.get_rect()
text_surface, text_rect = self.font.render(self.text, "white")
setattr(text_rect, self.anchor, getattr(screen_rect, self.anchor))
screen.blit(text_surface, text_rect)
```
Note: `pygame.freetype.Font.render()` returns `(Surface, Rect)`.

### Constants
All game-wide constants in `constants.py`. Use `LazyFont` to defer initialization:
```python
DEFAULT_FONT = LazyFont(32)  # Correct — deferred
# Wrong: pygame.freetype.Font(None, 32)  # Crashes before pygame.init()
```

### Pygame Patterns
- Use `pygame.Vector2` for 2D positions/velocities
- Screen origin `(0, 0)` is top-left; Y increases downward
- Delta time `dt` in seconds: `clock.tick(60) / 1000`
```python
self.position += self.velocity * dt
forward = pygame.Vector2(0, 1).rotate(self.rotation)
```

### Logging, Sprite Groups, Collision
`log_state()` and `log_event(event_type)` in `logger.py`. Use guard clauses:
```python
def shoot(self) -> None:
    if self.shot_cooldown > 0: return
    shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
    shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
    self.shot_cooldown = PLAYER_SHOT_COOLDOWN_SECONDS
```

Sprite groups in `main.py`:
```python
asteroids = pygame.sprite.Group()
drawable = pygame.sprite.Group()
shots = pygame.sprite.Group()
updatable = pygame.sprite.Group()

Asteroid.containers = (asteroids, updatable, drawable)
Shot.containers = (drawable, shots, updatable)
Player.containers = (updatable, drawable)
```

Collision detection via `CircleShape`:
```python
def collides_with(self, other):
    return self.position.distance_to(other.position) < (self.radius + other.radius)
# Usage: if asteroid.collides_with(player): player.kill()
if shot.collides_with(asteroid):
    shot.kill()
    asteroid.split()
```

### Screen Wrapping
```python
def wrap_position(self, screen_width, screen_height):
    if self.position.x > screen_width: self.position.x = 0
    elif self.position.x < 0: self.position.x = screen_width
    if self.position.y > screen_height: self.position.y = 0
    elif self.position.y < 0: self.position.y = screen_height
```

### Input Handling
Use `pygame.key.get_pressed()` for continuous input:
```python
def update(self, dt):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: self.move(dt)
    if keys[pygame.K_a]: self.rotate(-dt)
    if keys[pygame.K_SPACE]: self.shoot()
```

### Game Loop
```python
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: return
    screen.fill("black")
    updatable.update(dt)
    for obj in drawable: obj.draw(screen)
    pygame.display.flip()
    dt = clock.tick(60) / 1000
```

### Git Practices
Atomic, focused commits in imperative mood: "Add feature" not "Added feature"
Do not commit: `__pycache__/`, `*.pyc`, `.jsonl` logs, `.envrc`
