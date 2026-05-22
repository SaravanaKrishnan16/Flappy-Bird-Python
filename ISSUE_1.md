# Issue #1 — UI/Frontend: Replace Console Game Over Prompt with Pygame Game Over Screen

## Labels
`good first issue` `UI` `enhancement` `beginner-friendly`

---

## Problem Description

When the player dies, the game currently breaks out of the pygame window and asks the user to type `Y` or `N` in the **terminal/console**:

```python
# flappy.py — bottom of __main__ block (last 6 lines)
game_over, final_score = main_game()
print(f"Game Over! Your Score: {final_score}")
print("Do you want to play again? (Y/N): ", end="")
ans = input().strip().lower()
if ans != 'y':
    pygame.quit()
    sys.exit()
```

This is a bad user experience — the game window freezes, focus shifts to the terminal, and it feels broken. The project already has a `gameover.png` sprite sitting unused in `assets/sprites/gameover.png` that was clearly intended for this purpose.

---

## Why It Matters

- The game window goes unresponsive on death — looks like a crash to new players
- `input()` inside a pygame game loop is an anti-pattern and blocks the event loop
- The `gameover.png` asset exists but is never loaded or used anywhere in the code
- Every real Flappy Bird clone shows a proper in-window game over screen

---

## Expected Behavior

After the bird dies:
1. The pygame window stays open and active
2. A `game_over_screen(score)` function is shown **inside the pygame window** displaying:
   - The `gameover.png` sprite centered on screen
   - The final score
   - A hint like `"Press SPACE to replay or ESC to quit"`
3. Pressing `SPACE` restarts the game
4. Pressing `ESC` exits cleanly

---

## Files to Modify

- `flappy.py` only

---

## Step-by-Step Implementation Guide

### Step 1 — Load the `gameover.png` sprite
In the `__main__` block where all sprites are loaded, add:
```python
game_sprites['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
```

### Step 2 — Create a new `game_over_screen(score)` function
Add a new function (place it between `is_collide` and `get_random_pipe`):
```python
def game_over_screen(score):
    # center the gameover sprite on screen
    # render the score using pygame.font.SysFont
    # render a hint text "SPACE to replay | ESC to quit"
    # run a while True loop:
    #   - draw background, gameover sprite, score, hint
    #   - on SPACE keydown → return (so the main loop replays)
    #   - on ESC or QUIT → pygame.quit() + sys.exit()
```

### Step 3 — Replace the console block in `__main__`
Remove these lines at the bottom:
```python
print(f"Game Over! Your Score: {final_score}")
print("Do you want to play again? (Y/N): ", end="")
ans = input().strip().lower()
if ans != 'y':
    pygame.quit()
    sys.exit()
```
Replace with:
```python
game_over_screen(final_score)
```
The outer `while True` loop already handles replaying, so just calling `game_over_screen` and returning from it is enough to restart.

---

## Acceptance Criteria

- [ ] `gameover.png` is loaded into `game_sprites['gameover']`
- [ ] A `game_over_screen(score)` function exists and renders inside the pygame window
- [ ] Final score is displayed on the game over screen
- [ ] Pressing `SPACE` on the game over screen restarts the game
- [ ] Pressing `ESC` on the game over screen exits cleanly
- [ ] The `input()` and `print()` console lines are removed
- [ ] Game window never freezes or loses focus on death

---

## Suggested Commit Message
```
feat(ui): replace console game over prompt with pygame game over screen
```

## Suggested PR Title
`feat(ui): add in-window game over screen using gameover.png sprite`
