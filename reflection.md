# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  The game loaded as a normal Streamlit page with a difficulty dropdown, a guess box, Submit and New Game buttons and a debug panel, so it looked finished. Once I played it, the rules were wrong: the hints pointed the wrong way, and the numbers did not behave like the settings said.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  1. The hints were backwards: a guess above the secret said "Go HIGHER" and a guess below said "Go LOWER".
  2. On even-numbered attempts the secret was turned into a string, so the guess was compared as text. That gave wrong hints, for example "9" counted as higher than "10".
  3. Hard difficulty used 1-50, which is a smaller range than Normal (1-100), so it was easier. The prompt also always said "1 and 100", and New Game ignored the difficulty's range.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Secret is 50, guess 60 | Hint says "Go LOWER" | Hint said "Go HIGHER" | No error, just a wrong message |
| Secret is 10, guess 9 on an even-numbered attempt (the 2nd guess) | "Too Low" / "Go HIGHER" | Treated as "Too High", because "9" > "10" as text | No error; the TypeError from comparing int and str was caught and hidden by a fallback |
| Select Hard difficulty | A larger range than Normal | Range was 1-50, smaller than Normal's 1-100 | None; the sidebar showed "Range: 1 to 50" |
| Select Easy, then click New Game | New secret within 1-20 | Secret was picked from 1-100 | None; visible in Developer Debug Info |
| Type "abc" and submit | Error message, no attempt used | Error shown, but an attempt was still used up | None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  the check_guess hints were reversed, and the secret was turned into a string on even attempts, so a correct guess couldn't win.
  How you could say you verified it: you ran the app and played rounds, and you ran the pytest regression tests (test_too_high_hint_says_go_lower, test_numeric_not_string_comparison), which pass after the fix.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

  AI's suggestion of ombining attempt_limit_map and the ranges into one DIFFICULTY dict. I did not change or accept as it is kind of optional.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Reading the code: you checked that the line now matches what I described.
  Playing the game: I ran the app and tried the behaviour, for example a high guess, and saw whether the hint said "Go LOWER".
  Automated tests: the pytest tests fail if the bug comes back.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  pytest: python3 -m pytest gave 10 passed. test_numeric_not_string_comparison, which checks that 9 is lower than 10 and guards the string-comparison bug. What it showed you: the logic in logic_utils.py works without needing Streamlit.
- Did AI help you design or understand any tests? How?
  Yes,the AI wrote the regression tests in tests/test_game_logic.py, each aimed at one original bug.
  It explained the unpacking line ok, _, _ = parse_guess("7.9", 1, 100) when you asked what it meant.
  and it told me on how to run pytest and why the first three tests were failing.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Reruns
Normally a Python program runs once. Streamlit works differently: every time you click a button, type in a box or change a setting, it runs your whole script again from the first line to the last. The page you see is just the result of the latest run.

The problem it creates
Because the script starts over each time, ordinary variables are wiped each time. If you write score = 0 and add 10 when someone wins, the next click re-runs score = 0, and the score is gone.

Session state
st.session_state is a notebook that Streamlit keeps for your visit, and it survives the reruns. You write things in it, like the secret number, the score and how many attempts are used. On each rerun, the script reads from the notebook instead of starting blank.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  Keep logic separate from the UI.
Moving the rules into logic_utils.py meant you could test them without launching Streamlit. It also made app.py shorter and easier to read.
  
- What is one thing you would do differently next time you work with AI on a coding task?
  Ask for a small change, not a big list.
  The AI gave me many fixes at once, and some were missed or applied wrongly. Asking for one fix at a time, with a check after each, would keep errors easy to find.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  I used to assume code that looks complete and runs is correct, but this game was full of subtle bugs, so now I treat AI code as a draft I have to test and understand before trusting it.
