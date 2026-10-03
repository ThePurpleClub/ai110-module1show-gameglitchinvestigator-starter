# Architecture

Game Glitch Investigator is a number-guessing game built with Streamlit. The code is split into a UI layer that Streamlit renders and a logic layer of plain Python functions that can be tested without a browser.

## File layout

| File | Role |
|------|------|
| `app.py` | Streamlit UI, session state, and the turn-by-turn game flow |
| `logic_utils.py` | Pure game rules: ranges, input parsing, hint checking, scoring |
| `tests/test_game_logic.py` | pytest tests for `logic_utils.py` |
| `requirements.txt` | Python dependencies (Streamlit, pytest) |
| `README.md` | Setup, bugs found, fixes and test results |
| `reflection.md` | Process reflection |
| `ai_interactions.md` | Log of how AI was used |

## Layers

```
┌──────────────────────────────────────────┐
│ Browser (Streamlit page)                 │
│ sidebar, text box, buttons, messages     │
└───────────────────┬──────────────────────┘
                    │ every click or edit re-runs app.py
┌───────────────────▼──────────────────────┐
│ app.py (UI + flow)                       │
│ reads/writes st.session_state            │
└───────────────────┬──────────────────────┘
                    │ plain function calls
┌───────────────────▼──────────────────────┐
│ logic_utils.py (rules)                   │
│ no Streamlit imports, no state           │
└──────────────────────────────────────────┘
```

`logic_utils.py` never touches Streamlit or session state. It takes values in and returns values out, which is why `tests/test_game_logic.py` can exercise it directly.

## logic_utils.py

| Function | Input | Output |
|----------|-------|--------|
| `get_range_for_difficulty(difficulty)` | "Easy", "Normal" or "Hard" | `(low, high)`: 1-20, 1-100, 1-200 (default 1-100) |
| `parse_guess(raw, low, high)` | text typed by the player, plus the range | `(ok, value, error_message)`. Rejects empty input, non-integers (including decimals) and out-of-range numbers |
| `check_guess(guess, secret)` | two ints | `(outcome, message)` where outcome is "Win", "Too High" or "Too Low" |
| `update_score(current_score, outcome, attempt_number)` | current score, outcome, attempt count | new score |

Scoring rules:
- **Win:** adds `100 - 10 * attempt_number`, with a minimum of 10 points.
- **Too High or Too Low:** subtracts 5.

## app.py

### Settings in the UI layer
- `attempt_limit_map` holds attempts per difficulty: Easy 6, Normal 8, Hard 5. The ranges live in `logic_utils.py`, so a difficulty's settings are split across two files.

### Session state

Streamlit re-runs the whole script on each interaction, so anything that must survive is kept in `st.session_state`.

| Key | Meaning |
|-----|---------|
| `difficulty` | The difficulty the current game was started with |
| `secret` | The number to guess |
| `attempts` | Valid guesses used so far |
| `score` | Current score |
| `status` | "playing", "won" or "lost" |
| `history` | Every submitted guess, in order |

`reset_game(low, high)` sets all of these except `difficulty` back to fresh values and picks a new secret. It is the single place that defines a new game.

### What happens on each run, in order

1. Draw the title and sidebar, and read the selected difficulty.
2. Get `low`, `high` and `attempt_limit` for that difficulty.
3. If the stored `difficulty` differs from the selection (including the first load), store it and call `reset_game`.
4. Draw the prompt, the debug panel, the guess box and the buttons.
5. If **New Game** was clicked, call `reset_game` and re-run.
6. If `status` is not "playing", show the win or game-over message and stop.
7. If **Submit Guess** was clicked:
   - `parse_guess` validates the text. If invalid, show the error and do not count an attempt.
   - If valid, increment `attempts`, call `check_guess`, show the hint if enabled, and update the score with `update_score`.
   - If the outcome is "Win", set `status` to "won". Otherwise, if `attempts` has reached the limit, set `status` to "lost".

## State transitions

```
          New Game / difficulty change
        ┌─────────────────────────────┐
        ▼                             │
   [ playing ] ── correct guess ──▶ [ won ]
        │                             │
        └── attempts reach limit ──▶ [ lost ]
```

From "won" or "lost", only **New Game** (or changing difficulty) resets the game. Further guesses are blocked.

## Testing

`tests/test_game_logic.py` runs with `python3 -m pytest` and covers `logic_utils.py` only: hint direction and wording, numeric (not string) comparison, scoring, and input validation. The Streamlit UI and the flow in `app.py` are checked by running the app and playing it.

## Known limitations

- The "Attempts left" line is drawn before the submit handler runs, so it shows the previous count until the next interaction.
- Invalid guesses are still appended to `history`.
- Difficulty settings are split between `logic_utils.py` (ranges) and `app.py` (attempt limits).
- There are no automated tests for the UI layer.
