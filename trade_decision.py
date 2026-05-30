
# ==========================================
# TRADE DECISION ENGINE
# ==========================================

def generate_trade_decision(

    market_bias,
    bullish_score,
    bearish_score,
    primary_pattern

):

    # ==========================================
    # STRONG BUY
    # ==========================================

    if (

        "BULLISH" in market_bias

        and

        bullish_score >= 70

    ):

        return {

            "decision": "🚀 BUY",

            "strength": "HIGH",

            "reason": f"""

Strong bullish environment detected.

Primary Pattern:
{primary_pattern}

Bullish momentum aligned
across trend + volatility
+ pattern structure.

"""

        }

    # ==========================================
    # STRONG SELL
    # ==========================================

    if (

        "BEARISH" in market_bias

        and

        bearish_score >= 70

    ):

        return {

            "decision": "🔻 SELL",

            "strength": "HIGH",

            "reason": f"""

Strong bearish environment detected.

Primary Pattern:
{primary_pattern}

Bearish momentum aligned
across trend + volatility
+ pattern structure.

"""

        }

    # ==========================================
    # HOLD
    # ==========================================

    if abs(

        bullish_score -

        bearish_score

    ) < 15:

        return {

            "decision": "⚖️ HOLD",

            "strength": "LOW",

            "reason": """

Market direction unclear.

Conflicting signals detected.

"""

        }

    # ==========================================
    # WAIT
    # ==========================================

    return {

        "decision": "⏳ WAIT",

        "strength": "MEDIUM",

        "reason": """

No high-quality setup detected.

Waiting for stronger confirmation.

"""

    }

