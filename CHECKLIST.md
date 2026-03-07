# Asteroids Codebase Analysis & Improvement Checklist

## Critical Bugs (Must Fix First)

### 1. Game Loop Timing Bug
- [ ] **Location**: `main.py:70-71`
- **Problem**: Double `clock.tick(60)` calls causing 30 FPS instead of 60 FPS
- **Fix**: Remove line 70, keep only line 71 for delta time calculation

### 2. Infinite Self-Collision Bug
- [ ] **Location**: `main.py:60`
- **Problem**: `asteroid.collides_with(asteroid)` always true, causes infinite recursion
- **Fix**: Remove this check or implement proper asteroid-asteroid collision

### 3. Missing Screen Wrapping
- [ ] **Problem**: Objects disappear when moving off-screen
- **Expected**: Implement `wrap_position()` method in `CircleShape` class
- **Reference**: Mentioned in AGENTS.md but not implemented

### 4. Score System Not Functional
- [ ] **Location**: `main.py:49`, `asteroid.py:21,23`, `hud.py`
- **Problem**: Hardcoded "Score: 0" displayed, `Score` class not instantiated
- **Fix**: Uncomment `score = HUDElement()` and use `Score` class properly

---

## Code Structure & Design Issues

### 5. Inconsistent Inheritance Patterns
- [ ] **Problem**: `AsteroidField` inherits directly from `pygame.sprite.Sprite` instead of `CircleShape`
- **Impact**: Breaks consistency, different container initialization pattern

### 6. Container Initialization Inconsistency
- [ ] **Problem**: `AsteroidField.__init__()` assumes `self.containers` exists without a `hasattr()` guard
- **Risk**: Could crash if containers not set before instantiation

### 7. Unused Variable
- [ ] **Location**: `main.py:38`
- **Problem**: `asteroid_field` created but never referenced
- **Fix**: Remove the variable assignment or reference it intentionally

---

## Game Logic Problems

### 8. Inefficient Collision Detection
- [ ] **Location**: `main.py:55-66`
- **Problem**: O(n×m) nested loops for asteroid-shot collisions
- **Improvement**: Use `pygame.sprite.groupcollide()` for better performance and cleaner code

### 9. Commented Code with Incomplete Refactoring
- [ ] **Location**: `asteroid.py:26-27`
- **Problem**: Lines 26-27 commented out but equivalent logic used on lines 31-32
- **Action**: Clean up the commented code

### 10. Missing Backward Movement Constant
- [ ] **Location**: `player.py:65`
- **Problem**: Uses `-dt` for backward movement with no speed constant, unlike forward movement
- **Improvement**: Add a `PLAYER_BACKWARD_SPEED_MULTIPLIER` constant or unify with `PLAYER_SPEED`

### 11. Abrupt Game Termination
- [ ] **Location**: `main.py:59`
- **Problem**: `sys.exit()` on player death — no game over screen
- **Improvement**: Implement game state management instead of hard exit

---

## Performance Issues

### 12. Expensive Logging Every Frame
- [ ] **Location**: `logger.py:18`, `main.py:43`
- **Problem**: `log_state()` called every frame, running `inspect.currentframe()` operations on each call
- **Optimization**: Move frame check to the top of `log_state()` and return early, or gate the call in `main.py`

### 13. Redundant Drawing Operations
- [ ] **Location**: `main.py:49-54`, `main.py:67-68`
- **Problem**: Score text drawn manually before the sprite group draw loop, resulting in double rendering
- **Fix**: Use sprite group drawing consistently; rely on `Score.draw()` via the drawable group

---

## Missing Features & Polish

### 14. No Game State Management
- [ ] **Missing**: Start screen, pause functionality, game over screen
- **Impact**: Poor user experience, abrupt transitions
- **Approach**: Implement a simple finite state machine (e.g. `MENU`, `PLAYING`, `PAUSED`, `GAME_OVER`)

### 15. No Audio Support
- [ ] **Missing**: Sound effects for shooting, explosions, background music
- **Enhancement**: Add `pygame.mixer` integration

### 16. No Visual Effects
- [ ] **Missing**: Explosion animations, particle effects on asteroid destruction
- **Enhancement**: Add sprite animations or a simple particle system

### 17. No Difficulty Progression
- [ ] **Missing**: Increasing spawn rates, faster asteroids over time
- **Enhancement**: Implement progressive difficulty using elapsed time or score thresholds

### 18. No Power-ups or Bonuses
- [ ] **Missing**: Classic asteroids features like shields, multi-shot, etc.
- **Enhancement**: Add a power-up system for extended gameplay variety

---

## Code Quality Improvements

### 19. Magic Numbers in Game Logic
- [ ] **Examples**:
  - `Player.triangle()`: `1.5` divisor (`player.py:25`)
  - `Asteroid.split()`: `1.2` velocity multiplier (`asteroid.py:31-32`)
  - `AsteroidField`: Speed range `40-100`, angle range `-30, 30` (`asteroidfield.py:55,57`)
- **Action**: Extract all to named constants in `constants.py`

### 20. Inconsistent Return Patterns
- [ ] **Location**: `player.py:44-52`
- **Problem**: `shoot()` has an explicit `return` on cooldown but implicitly returns `None` on success
- **Improvement**: Remove the redundant `else: return` — a guard clause makes the intent clearer

### 21. LazyFont Descriptor Pattern Confusion
- [ ] **Location**: `constants.py:18-19`
- **Problem**: `LazyFont.__get__()` returns `self` — the purpose of this descriptor protocol method is unclear
- **Clarification**: Document the intent or simplify if the method is not needed

### 22. Multiple LazyDimensions Instances
- [ ] **Location**: `main.py:24-25`, `asteroidfield.py:19-20`
- **Issue**: New instances created each time instead of sharing a single cached instance
- **Optimization**: Implement a module-level singleton or pass dimensions as arguments

---

## Testing & Documentation

### 23. No Unit Tests
- [ ] **Missing**: Test files for game logic, collision detection, player movement, etc.
- **Action**: Create a `tests/` directory with pytest tests (see AGENTS.md for setup commands)

### 24. No Integration Tests
- [ ] **Missing**: End-to-end game flow testing
- **Action**: Add game state validation tests for key interactions

### 25. Empty README.md
- [ ] **Location**: `README.md` (0 bytes)
- **Action**: Add basic project documentation — controls, how to run, dependencies

### 26. Missing Docstrings
- [ ] **Problem**: Most classes and methods lack docstrings
- **Improvement**: Add at minimum one-line docstrings for all public methods

---

## Configuration & Environment

### 27. Hardcoded SDL Video Driver
- [ ] **Location**: `main.py:19`
- **Problem**: `os.environ["SDL_VIDEODRIVER"] = "wayland"` is platform-specific and will break on non-Wayland systems
- **Improvement**: Make configurable via environment variable or detect the platform at runtime

### 28. No Error Handling for Pygame Init
- [ ] **Risk**: Game crashes with an unhelpful traceback if pygame initialization fails
- **Improvement**: Wrap `pygame.init()` in a try-except with an informative error message

---

## Prioritization Guide

### P0 — Critical (Game Breaking)
1. Fix double `clock.tick()` bug
2. Fix self-collision infinite recursion
3. Implement screen wrapping
4. Fix score system

### P1 — High Priority (Core Functionality)
5. Implement proper collision detection with `groupcollide()`
6. Fix container initialization consistency
7. Add game state management (pause / game over)
8. Clean up commented and unused code

### P2 — Medium Priority (Polish & UX)
9. Add audio support
10. Add visual effects
11. Extract magic numbers to constants
12. Implement difficulty progression

### P3 — Low Priority (Nice-to-have)
13. Add power-up system
14. Comprehensive unit tests
15. Performance optimizations
16. Enhanced HUD elements

---

## Learning Points

1. **Game Timing**: Understand the relationship between delta time, `clock.tick()`, and frame rate
2. **Collision Detection**: Learn how pygame's sprite group collision helpers work and when to use spatial partitioning
3. **State Management**: Implement finite state machines for clean game flow control
4. **Code Consistency**: Patterns that work for small codebases (e.g. container init) need to be applied uniformly
5. **Performance Awareness**: Identify hot paths (every-frame calls) early and keep them lean
