
# ==========================================
# PATTERN PRIORITY ENGINE
# ==========================================

def rank_patterns(patterns):

    pattern_scores = {

        # ==========================================
        # HIGH PRIORITY REVERSALS
        # ==========================================

        "📈 DOUBLE BOTTOM": 90,

        "📉 HEAD AND SHOULDERS": 95,

        "☕ CUP AND HANDLE": 92,

        "🌙 ROUNDING BOTTOM": 88,

        # ==========================================
        # TRIANGLES
        # ==========================================

        "📈 ASCENDING TRIANGLE": 85,

        "🔻 DESCENDING TRIANGLE": 85,

        "🔺 SYMMETRICAL TRIANGLE BULLISH": 82,

        "🔻 SYMMETRICAL TRIANGLE BEARISH": 82,

        # ==========================================
        # WEDGES
        # ==========================================

        "📈 FALLING WEDGE": 84,

        "📉 RISING WEDGE": 84,

        # ==========================================
        # CANDLESTICKS
        # ==========================================

        "🚀 BULLISH ENGULFING": 75,

        "📉 BEARISH ENGULFING": 75,

        "🔨 HAMMER": 70,

        "🌠 SHOOTING STAR": 70,

        "🌅 MORNING STAR": 78,

        "🌇 EVENING STAR": 78,

        "⚖️ DOJI": 50,

        # ==========================================
        # SUPPORT / RESISTANCE
        # ==========================================

        "🟩 SUPPORT ZONE": 60,

        "🟥 RESISTANCE ZONE": 60

    }

    ranked_patterns = []

    # ==========================================
    # SCORE EACH PATTERN
    # ==========================================

    for pattern in patterns:

        score = pattern_scores.get(

            pattern,

            40

        )

        ranked_patterns.append(

            (

                pattern,

                score

            )

        )

    # ==========================================
    # SORT HIGHEST FIRST
    # ==========================================

    ranked_patterns.sort(

        key=lambda x: x[1],

        reverse=True

    )

    return ranked_patterns

