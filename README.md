# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

**Game's purpose**

A Streamlit number-guessing game. The player picks a difficulty, guesses a secret number within a range, and gets "Go HIGHER" or "Go LOWER" hints. They have a limited number of attempts, and a score rewards winning quickly.

**Bugs found**

- Hints were reversed (a high guess said "Go HIGHER").
- On even attempts the secret was converted to a string, so comparisons were wrong and you couldn't win.
- Scoring was inconsistent: win points were off by one, and "Too High" sometimes added points.
- Hard (1-50) was easier than Normal (1-100).
- The prompt always said "1 and 100", and New Game ignored the difficulty's range.
- The secret was not regenerated when difficulty changed.
- Attempts started at 1 at first load but 0 after New Game, and invalid input cost an attempt.
- New Game didn't reset score, status or history.
- Decimals like "7.9" were truncated, and out-of-range guesses were accepted.

**Fixes applied**

- Corrected the hint messages and always compare ints.
- Fixed the scoring formula, with -5 for every wrong guess.
- Hard is now 1-200, and the prompt uses the real range.
- The secret and state reset when difficulty changes, using a shared `reset_game` helper.
- Attempts are counted only for valid guesses, starting at 0.
- `parse_guess` rejects decimals and out-of-range numbers.
- Moved the game logic into `logic_utils.py` and added pytest regression tests.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py` and choose a difficulty in the sidebar (the range and attempt limit update).
2. Type a whole number in the range and click **Submit Guess**.
3. Read the hint: a guess above the secret says "Go LOWER", below says "Go HIGHER".
4. Each wrong guess costs 5 points and uses an attempt; "Attempts left" counts down.
5. Guess the secret to win and see the balloons and final score, or run out of attempts and see the game-over message.
6. Click **New Game** to reset the score, history and secret.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python3 -m pytest tests/
============================= test session starts ==============================
collected 10 items

tests/test_game_logic.py ..........                                      [100%]

============================== 10 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
