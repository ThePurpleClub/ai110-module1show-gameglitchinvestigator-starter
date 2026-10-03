from logic_utils import check_guess, parse_guess, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result, _ = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result, _ = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result, _ = check_guess(40, 50)
    assert result == "Too Low"


# Regression tests for the original bugs

def test_too_high_hint_says_go_lower():
    # Bug: hints were reversed. A guess above the secret must say LOWER.
    _, message = check_guess(60, 50)
    assert "LOWER" in message
    assert "HIGHER" not in message

def test_too_low_hint_says_go_higher():
    # Bug: hints were reversed. A guess below the secret must say HIGHER.
    _, message = check_guess(40, 50)
    assert "HIGHER" in message
    assert "LOWER" not in message

def test_numeric_not_string_comparison():
    # Bug: the secret was sometimes a string, so "9" > "10" compared wrongly.
    # 9 is lower than 10 numerically.
    outcome, _ = check_guess(9, 10)
    assert outcome == "Too Low"

def test_win_scores_positive_points():
    # Bug: win points were off by one and could subtract points.
    assert update_score(0, "Win", 1) == 90

def test_wrong_guess_costs_five_points():
    # Bug: Too High sometimes added points on even attempts.
    assert update_score(20, "Too High", 2) == 15
    assert update_score(20, "Too Low", 2) == 15

def test_parse_rejects_out_of_range():
    ok, _, err = parse_guess("500", 1, 100)
    assert ok is False
    assert err

def test_parse_rejects_decimal():
    # Bug: "7.9" was silently truncated to 7.
    ok, _, _ = parse_guess("7.9", 1, 100)
    assert ok is False
