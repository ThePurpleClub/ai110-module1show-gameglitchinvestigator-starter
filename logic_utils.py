def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # Fix: Hard was 1-50 (easier than Normal). Claude spotted it; I set 1-200.
        return 1, 200
    return 1, 100

def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    # Fix: decimals like "7.9" used to be truncated to 7. Claude explained
    # the issue; I removed the float branch so they are rejected.
    try:
        value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # Fix: no range check before. Claude suggested passing low/high in; I wired it up.
    if not (low <= value <= high):
        return False, None, f"Enter a number between {low} and {high}."


    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # Fix: hints were reversed and a str/int fallback broke comparisons.
    # Claude found both; I swapped the messages and removed the fallback.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # Fix: win points were off by one and Too High gave +5 on even attempts.
    # Claude flagged the scoring bugs; I corrected the formula and made both -5.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number)
        if points < 10:
            points = 10
        return current_score + points

    elif outcome in ("Too High", "Too Low"): 
        return current_score - 5

    return current_score