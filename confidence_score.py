def calculate_bullish_score(
    double_bottom,
    bullish_div,
    support,
    bullish_engulf,
    volume_spike,
    high_volatility,
    trend_15m,
    trend_1h
):

    score = 0

    if double_bottom:
        score += 25

    if bullish_div:
        score += 30

    if support:
        score += 20

    if bullish_engulf:
        score += 15

    if volume_spike:
        score += 15

    if trend_15m == "BULLISH":
        score += 15

    if trend_1h == "BULLISH":
        score += 15

    if high_volatility:
        score -= 10

    return max(min(score, 100), 0)


def calculate_bearish_score(
    double_top,
    bearish_div,
    resistance,
    bearish_engulf,
    volume_spike,
    high_volatility,
    trend_15m,
    trend_1h
):

    score = 0

    if double_top:
        score += 25

    if bearish_div:
        score += 30

    if resistance:
        score += 20

    if bearish_engulf:
        score += 15

    if volume_spike:
        score += 15

    if trend_15m == "BEARISH":
        score += 15

    if trend_1h == "BEARISH":
        score += 15

    if high_volatility:
        score -= 10

    return max(min(score, 100), 0)