# ==========================================
# BREAKOUT CONFIRMATION
# ==========================================

def breakout_confirmed(

    df,
    breakout_level,
    direction="bullish"

):

    # ==========================================
    # SAFE FLOAT CONVERSION
    # ==========================================

    breakout_level = float(
        breakout_level
    )

    latest_close = float(

        df["Close"]

        .squeeze()

        .iloc[-1]

    )

    latest_volume = float(

        df["Volume"]

        .squeeze()

        .iloc[-1]

    )

    average_volume = float(

        df["Volume"]

        .squeeze()

        .tail(20)

        .mean()

    )

    latest_atr = float(

        df["ATR"]

        .squeeze()

        .iloc[-1]

    )

    average_atr = float(

        df["ATR"]

        .squeeze()

        .tail(20)

        .mean()

    )

    # ==========================================
    # VOLUME CONFIRMATION
    # ==========================================

    volume_confirmed = (

        latest_volume >

        average_volume * 1.5

    )

    # ==========================================
    # VOLATILITY CONFIRMATION
    # ==========================================

    volatility_confirmed = (

        latest_atr >

        average_atr * 1.2

    )

    # ==========================================
    # BULLISH BREAKOUT
    # ==========================================

    if direction == "bullish":

        breakout = (

            latest_close >

            breakout_level

        )

    # ==========================================
    # BEARISH BREAKOUT
    # ==========================================

    else:

        breakout = (

            latest_close <

            breakout_level

        )

    # ==========================================
    # FINAL CONFIRMATION
    # ==========================================

    return (

        breakout

        and

        volume_confirmed

        and

        volatility_confirmed

    )