# HUD System — Session Notes

A summary of everything covered in this session: pygame screen positioning,
the Rect system, and how it all connects to building a HUD using OOP in Python.

---

## 1. Pygame's Coordinate System

Pygame's screen origin `(0, 0)` is the **top-left** corner, not the center.
X increases to the right, Y increases **downward** — the opposite of math class.

```
(0, 0) ──────────────────────► X increases →
  │
  │
  │
  ▼
Y increases ↓
                    (SCREEN_WIDTH, SCREEN_HEIGHT)
```

The four corners of the screen:

```
(0, 0)                    (SCREEN_WIDTH, 0)
  ┌────────────────────────────┐
  │                            │
  │                            │
  └────────────────────────────┘
(0, SCREEN_HEIGHT)    (SCREEN_WIDTH, SCREEN_HEIGHT)
```

---

## 2. pygame.Rect and Named Anchors

A `pygame.Rect` is an object that stores a rectangular area.
It has **named anchor attributes** that give you meaningful coordinates:

```
topleft        midtop       topright
   ┌──────────────┬──────────────┐
   │                             │
midleft      center       midright
   │                             │
   └──────────────┴──────────────┘
bottomleft   midbottom   bottomright
```

You can both **read** and **set** these anchors:

```python
rect.topright = (100, 20)   # moves the rect so its top-right is at (100, 20)
rect.center = (960, 540)    # moves the rect so its center is at (960, 540)
```

Setting an anchor **moves** the rect — it does not resize it.
Pygame recalculates all other anchor positions automatically.

---

## 3. screen.get_rect()

After creating a pygame screen, call `screen.get_rect()` to get a `Rect`
representing the full screen bounds:

```python
pygame.init()
screen = pygame.display.set_mode((1280, 720))
screen_rect = screen.get_rect()

screen_rect.topleft      # (0, 0)
screen_rect.topright     # (1280, 0)
screen_rect.bottomleft   # (0, 720)
screen_rect.bottomright  # (1280, 720)
screen_rect.center       # (640, 360)
screen_rect.centerx      # 640
screen_rect.centery      # 360
```

### Why not use SCREEN_WIDTH / SCREEN_HEIGHT constants?

Constants are evaluated at **import time**, before `pygame.init()` is called
and before a window is created. `screen.get_rect()` reflects the **actual**
window size at runtime, which may differ from what you requested — especially
with Wayland, multi-monitor setups, or fullscreen mode.

Always use `screen.get_rect()` for positioning. Use constants only for things
that don't depend on the actual window size.

### Fullscreen

With fullscreen you don't know the screen size ahead of time.
`screen.get_rect()` handles this automatically:

```python
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# (0, 0) means "use native resolution"

screen_rect = screen.get_rect()
# screen_rect now has the correct dimensions for whatever monitor you're on
```

This is why `screen.get_rect()` is the correct tool for HUD positioning —
it works for windowed, fullscreen, and any resolution.

---

## 4. Positioning Text at Screen Corners

`pygame.freetype.Font.render()` returns a **tuple**: `(Surface, Rect)`.
- `Surface` — the actual image of the rendered text
- `Rect` — the bounding box of that image (also has anchor attributes)

To position text at a corner:

```python
PADDING = 20
screen_rect = screen.get_rect()

text_surface, text_rect = font.render("Score: 100", "white")

# Align the text's top-right corner to the screen's top-right, minus padding
text_rect.topright = (screen_rect.right - PADDING, screen_rect.top + PADDING)

# Draw the surface at the positioned rect
screen.blit(text_surface, text_rect)
```

Why this works — if text is 150px wide:

```
                text_rect.topright = (1260, 20)
                        │
         ┌──────────────┘
         │◄── 150px ───►│
    (1110, 20)       (1260, 20)
```

The text's right edge aligns to x=1260, and pygame calculates the left edge
automatically based on text width. You never need to know the text width.

Compare to the wrong approach:

```python
# ❌ Wrong — sets the LEFT edge at x=1260, text extends off screen
text_rect.topleft = (screen_rect.right - PADDING, PADDING)
```

---

## 5. Dynamic Anchor Positioning with getattr/setattr

Python builtins `getattr` and `setattr` let you read and write object
attributes **by name as a string**. This allows the anchor to be a variable:

```python
anchor = "topright"  # could be any anchor name

# Instead of: pos = screen_rect.topright
pos = getattr(screen_rect, anchor)   # reads the attribute by name

# Instead of: text_rect.topright = (x, y)
setattr(text_rect, anchor, (x, y))  # sets the attribute by name
```

This means a single block of positioning code works for **any** anchor,
without needing if/else branches for each corner.

---

## 6. OOP Design — HUDElement Base Class

### Why a Base Class?

A base class captures **shared behaviour** so subclasses don't repeat it.
Here, all HUD elements share:
- A screen position (anchor + screen_rect)
- A font and color
- The logic for rendering text at the correct position

Subclasses only need to define **what text to show**.

### OOP Concepts Demonstrated

| Concept | Where it appears |
|---------|-----------------|
| **Inheritance** | `Score` inherits from `HUDElement`, `HUDElement` from `pygame.sprite.Sprite` |
| **Encapsulation** | Score value lives inside `Score`; rendering logic lives inside `HUDElement` |
| **Polymorphism** | `drawable` group calls `draw(screen)` on every object — each handles it differently |
| **Separation of concerns** | `HUDElement` handles *how* to draw; `Score` handles *what* to draw |

### The Class

```python
# hud.py

import pygame
import pygame.freetype

from constants import LazyFont

PADDING = 20
default_font = LazyFont(24)


class HUDElement(pygame.sprite.Sprite):
    # OOP NOTE: Class-level attribute shared by all instances.
    # main.py sets HUDElement.containers = (drawable, updatable) before
    # instantiating, so every instance automatically joins those groups.
    PADDING = 20

    def __init__(self, screen_rect, anchor="topleft", font=default_font):
        # OOP NOTE: The hasattr guard lets this class work with or without
        # containers being set — a defensive pattern used throughout this codebase.
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        # OOP NOTE: These are instance attributes — each HUDElement instance
        # gets its own copy. They're set once at init and don't change.
        self.screen_rect = screen_rect  # stored once — doesn't change
        self.anchor = anchor            # "topleft", "topright", etc.
        self.font = font
        self.color = "#FFFFFF"
        self.text = ""                  # will be updated by subclasses

    def draw(self, screen):
        # OOP NOTE: draw() is called every frame by the drawable sprite group.
        # text_surface and text_rect are created fresh here — NOT in __init__ —
        # because self.text changes, and the text width changes with it.
        if not self.text:
            return

        text_surface, text_rect = self.font.render(self.text, self.color)

        screen_anchor = getattr(self.screen_rect, self.anchor)

        # Nudge inward from the edge based on which side the anchor is on
        x = screen_anchor[0] + self.PADDING if "left" in self.anchor else screen_anchor[0] - self.PADDING
        y = screen_anchor[1] + self.PADDING if "top" in self.anchor else screen_anchor[1] - self.PADDING

        setattr(text_rect, self.anchor, (x, y))
        screen.blit(text_surface, text_rect)

    def update(self, dt):
        # OOP NOTE: Base class provides an empty update() so subclasses
        # can override only what they need. This is the Template Method pattern.
        pass
```

---

## 7. OOP Design — Score Subclass

```python
class Score(HUDElement):
    # OOP NOTE: Score inherits everything from HUDElement.
    # It only overrides what's different: where to anchor, and what text to show.

    def __init__(self, screen_rect):
        # OOP NOTE: super().__init__() calls the parent class constructor.
        # We pass anchor="topleft" because Score always lives in the top-left.
        super().__init__(screen_rect, anchor="topleft")
        self.score = 0  # Score owns this value

    def update(self, dt):
        # OOP NOTE: Overrides the parent's empty update().
        # Called every frame by the updatable group.
        # Keeps self.text in sync with self.score so draw() always has fresh text.
        self.text = f"Score: {self.score}"
```

---

## 8. Wiring It Together in main.py

```python
def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_rect = screen.get_rect()  # get actual dimensions once

    # Sprite groups
    drawable = pygame.sprite.Group()
    updatable = pygame.sprite.Group()

    # OOP NOTE: Setting containers on the class (not the instance) means
    # every new instance of HUDElement (and its subclasses) automatically
    # joins these groups when instantiated.
    HUDElement.containers = (drawable, updatable)

    score = Score(screen_rect)  # automatically joins drawable and updatable

    # Use screen_rect for player spawn position — not the constants
    player = Player(x=screen_rect.centerx, y=screen_rect.centery)

    while True:
        # ...

        # When an asteroid is shot:
        if shot.collides_with(asteroid):
            score.score += 100  # reach into Score instance to update value
            shot.kill()
            asteroid.split()

        updatable.update(dt)    # calls score.update(dt) → updates self.text
        for obj in drawable:
            obj.draw(screen)    # calls score.draw(screen) → renders self.text
```

---

## 9. What Lives Where and Why

| Data | Where | Why |
|------|-------|-----|
| `screen_rect` | `__init__` | Set once at creation, never changes |
| `anchor` | `__init__` | Set once at creation, never changes |
| `font`, `color` | `__init__` | Set once at creation, never changes |
| `text` | `__init__` as `""`, updated in `update()` | Changes as game state changes |
| `score` | `Score.__init__`, mutated in `main.py` | The value being tracked |
| `text_surface` | `draw()` local variable | Recreated every frame — text changes |
| `text_rect` | `draw()` local variable | Recreated every frame — width changes with text |

---

## 10. Key Takeaways

- **`screen.get_rect()`** gives you named anchor points for the actual screen
  size at runtime — more reliable than constants
- **`pygame.Rect` anchors** let you position elements relative to corners and
  edges without knowing their width/height in advance
- **`font.render()`** returns `(Surface, Rect)` — a tuple, not just a surface
- **Render text in `draw()`**, not `__init__`  — text content and width change
- **Base class handles how to draw; subclass handles what to draw** — that
  separation keeps each class focused on one responsibility
- **`getattr`/`setattr`** let you use attribute names as strings, making
  positioning logic work for any anchor without branching
