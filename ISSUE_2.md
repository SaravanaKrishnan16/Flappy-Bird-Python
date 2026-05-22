# Issue #2 — Backend/Logic: Add Bird Wing-Flap Animation

## Labels
`good first issue` `enhancement` `game-logic` `beginner-friendly`

---

## Problem Description

The bird currently uses a **single static image** throughout the entire game — it never flaps its wings:

```python
# flappy.py — line 13 (global)
player = 'assets/sprites/bluebird-midflap.png'

# flappy.py — __main__ block
game_sprites['player'] = pygame.image.load(player).convert_alpha()
```

Only `bluebird-midflap.png` is ever loaded. But the `assets/sprites/` folder already contains **all 3 animation frames** for every bird color:

```
assets/sprites/bluebird-downflap.png
assets/sprites/bluebird-midflap.png
assets/sprites/bluebird-upflap.png
```

The bird should cycle through these 3 frames to look like it is actually flapping its wings — exactly like the original Flappy Bird game.

---

## Why It Matters

- The bird looks stiff and lifeless with a single frozen frame
- All 3 sprite frames already exist in the repo — they just aren't used
- Wing animation is one of the most iconic visual features of Flappy Bird
- This is a pure logic addition with no new assets needed

---

## Expected Behavior

- The bird cycles through `downflap → midflap → upflap → midflap → downflap ...` continuously
- The frame changes every few game ticks (e.g., every 5 ticks)
- The animation runs during both the welcome screen and the main game loop
- The correct animated frame is drawn wherever `game_sprites['player']` is blitted

---

## Files to Modify

- `flappy.py` only

---

## Step-by-Step Implementation Guide

### Step 1 — Load all 3 bird frames in `__main__`
Replace the single player image load:
```python
# BEFORE (line in __main__)
game_sprites['player'] = pygame.image.load(player).convert_alpha()
```
With a tuple of all 3 frames:
```python
# AFTER
game_sprites['player'] = (
    pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
    pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
    pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha(),
)
```

### Step 2 — Add a frame index tracker
Inside `main_game()` (and `welcome_screen()`), add two variables before the `while True` loop:
```python
player_index = 0        # current frame index (0, 1, or 2)
player_index_gen = 0    # tick counter to control animation speed
```

### Step 3 — Advance the frame each tick
Inside the `while True` game loop, before drawing, add:
```python
player_index_gen += 1
if player_index_gen % 5 == 0:   # change frame every 5 ticks
    player_index = (player_index + 1) % 3
```

### Step 4 — Draw the correct frame
Wherever the player is blitted, use the indexed frame instead of the whole sprite:
```python
# BEFORE
screen.blit(game_sprites['player'], (playerx, playery))

# AFTER
screen.blit(game_sprites['player'][player_index], (playerx, playery))
```

### Step 5 — Fix width/height references
Any place that calls `.get_width()` or `.get_height()` on `game_sprites['player']` must now index into the tuple:
```python
# BEFORE
game_sprites['player'].get_width()
game_sprites['player'].get_height()

# AFTER
game_sprites['player'][player_index].get_width()
game_sprites['player'][player_index].get_height()
```
Search for all occurrences of `game_sprites['player']` in the file and update them.

---

## Acceptance Criteria

- [ ] All 3 bird frames (`upflap`, `midflap`, `downflap`) are loaded into a tuple
- [ ] The bird visibly cycles through wing frames during gameplay
- [ ] Animation also plays on the welcome screen
- [ ] No `AttributeError` from calling `.get_width()` / `.get_height()` on the tuple
- [ ] Collision detection still works correctly (uses correct frame dimensions)

---

## Suggested Commit Message
```
feat(animation): add bird wing-flap animation using all 3 sprite frames
```

## Suggested PR Title
`feat: animate bird wing flap by cycling through upflap/midflap/downflap sprites`
