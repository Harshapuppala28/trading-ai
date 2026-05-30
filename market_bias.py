
# ==========================================
# MARKET BIAS ENGINE
# ==========================================

def calculate_market_bias(

    ranked_patterns,
    market_data

):

    bullish_points = 0

    bearish_points = 0

    # ==========================================
    # PATTERN ANALYSIS
    # ==========================================

    bullish_patterns = [

        "📈 DOUBLE BOTTOM",

        "☕ CUP AND HANDLE",

        "🌙 ROUNDING BOTTOM",

        "📈 ASCENDING TRIANGLE",

        "📈 FALLING WEDGE",

        "🚀 BULLISH ENGULFING",

        "🔨 HAMMER",

        "🌅 MORNING STAR"

    ]

    bearish_patterns = [

        "📉 HEAD AND SHOULDERS",

        "🔻 DESCENDING TRIANGLE",

        "📉 RISING WEDGE",

        "📉 BEARISH ENGULFING",

        "🌠 SHOOTING STAR",

        "🌇 EVENING STAR"

    ]

    for pattern, score in ranked_patterns:

        if pattern in bullish_patterns:

            bullish_points += score

        if pattern in bearish_patterns:

            bearish_points += score

    # ==========================================
    # TREND ANALYSIS
    # ==========================================

    if market_data["trend_15m"] == "BULLISH":

        bullish_points += 25

    else:

        bearish_points += 25

    if market_data["trend_1h"] == "BULLISH":

        bullish_points += 35

    else:

        bearish_points += 35

    # ==========================================
    # VOLUME ANALYSIS
    # ==========================================

    if market_data["volume_spike"]:

        bullish_points += 10

        bearish_points += 10

    # ==========================================
    # VOLATILITY ANALYSIS
    # ==========================================

    if market_data["high_volatility"]:

        bullish_points += 5

        bearish_points += 5

    # ==========================================
    # FINAL BIAS
    # ==========================================

    difference = abs(

        bullish_points -

        bearish_points

    )

    # strong bullish

    if bullish_points > bearish_points:

        if difference > 40:

            return "🚀 STRONG BULLISH"

        else:

            return "📈 MODERATE BULLISH"

    # strong bearish

    elif bearish_points > bullish_points:

        if difference > 40:

            return "🔻 STRONG BEARISH"

        else:

            return "📉 MODERATE BEARISH"

    # neutral

    return "⚖️ NEUTRAL MARKET"

