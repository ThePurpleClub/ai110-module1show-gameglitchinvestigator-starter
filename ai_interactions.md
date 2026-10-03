# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I used Claude Code in VS Code. I asked it to find the bugs in `app.py`, explain how to fix them without changing my code, and review my edits after each round. Later I asked it to write regression tests, add comments next to each fix, fill in the README and write a commit message.

**What did the agent do?**

- Read `app.py` and `logic_utils.py` and listed the bugs (reversed hints, string secret, scoring, Hard range, state resets).
- Reviewed my edits several times, ran `py_compile` to catch syntax errors, and found problems such as a missing `if submit:` line and an unused `reset_game` helper.
- Wrote 7 regression tests in `tests/test_game_logic.py`, installed pytest, and ran it (10 passed).
- Added fix comments in `app.py` and `logic_utils.py`, filled in the README sections, and committed the changes.

**What did you have to verify or fix manually?**

- I made the code edits myself, and several of them broke the app (an indentation error and a deleted `if new_game:` line) until I fixed them.
- The agent first said the string conversion meant you could not win on even attempts. That was inaccurate: a correct guess still matched, but the hints were wrong because numbers were compared as text.
- The agent could not push to GitHub because it had no login, so I pushed from VS Code with Sync Changes.
- I checked the game by running Streamlit and playing it, because the tests only cover `logic_utils.py`.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Hint direction (guess above secret) | "can you generate a pytest case in test/test_game_logic.py that specifically targets the bug you just fixed." | `test_too_high_hint_says_go_lower`: `check_guess(60, 50)` message contains "LOWER" | Yes | The hints were reversed originally, so the message text needs its own check, not just the outcome label. |
| Numbers compared as text | Same prompt | `test_numeric_not_string_comparison`: `check_guess(9, 10)` returns "Too Low" | Yes | "9" > "10" as strings, so this fails if the secret ever becomes a string again. |
| Win scoring | Same prompt | `test_win_scores_positive_points`: `update_score(0, "Win", 1) == 90` | Yes | Win points were off by one and could subtract points. |
| Wrong guess penalty | Same prompt | `test_wrong_guess_costs_five_points`: Too High and Too Low both subtract 5 | Yes | "Too High" used to add 5 on even attempts. |
| Decimal input | Same prompt | `test_parse_rejects_decimal`: `parse_guess("7.9", 1, 100)` is rejected | Yes | "7.9" used to be silently truncated to 7. |
| Out-of-range input | Same prompt | `test_parse_rejects_out_of_range`: `parse_guess("500", 1, 100)` is rejected | Yes | Guesses outside the range were accepted. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
