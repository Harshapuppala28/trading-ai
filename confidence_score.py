def calculate_confidence(

    patterns,
    market_data

):

    bullish_score = 0

    bearish_score = 0


    # ==========================================
    # PATTERN SCORING
    # ==========================================

    for pattern in patterns:

        if (
            "BULLISH" in pattern
            or "SUPPORT" in pattern
        ):

            bullish_score += 25

        if (
            "BEARISH" in pattern
            or "DOUBLE TOP" in pattern
        ):

            bearish_score += 25

        if "DOJI" in pattern:

            bullish_score += 5
            bearish_score += 5


    # ==========================================
    # TREND CONFIRMATION
    # ==========================================

    if market_data["trend_15m"] == "BULLISH":

        bullish_score += 15

    else:

        bearish_score += 15


    if market_data["trend_1h"] == "BULLISH":

        bullish_score += 15

    else:

        bearish_score += 15


    # ==========================================
    # VOLUME
    # ==========================================

    if market_data["volume_spike"]:

        bullish_score += 10
        bearish_score += 10


    # ==========================================
    # VOLATILITY
    # ==========================================

    if market_data["high_volatility"]:

        bullish_score += 5
        bearish_score += 5


    # LIMIT TO 100
    bullish_score = min(
        bullish_score,
        100
    )

    bearish_score = min(
        bearish_score,
        100
    )
    
    return (

        bullish_score,
        bearish_score

    )