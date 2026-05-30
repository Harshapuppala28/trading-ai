id="r6"
# ==========================================
# ANALYZE MARKET STRENGTH
# ==========================================

def analyze_market_strength(

    df_5m,
    df_15m,
    df_1h

):

    # ==========================================
    # FIX MULTI-INDEX COLUMNS
    # ==========================================

    close_15m = df_15m["Close"].squeeze()

    close_1h = df_1h["Close"].squeeze()

    volume_5m = df_5m["Volume"].squeeze()

    atr_5m = df_5m["ATR"].squeeze()

    ema9_15m_series = df_15m["EMA_9"].squeeze()

    ema21_15m_series = df_15m["EMA_21"].squeeze()

    ema9_1h_series = df_1h["EMA_9"].squeeze()

    ema21_1h_series = df_1h["EMA_21"].squeeze()

    # ==========================================
    # 15M TREND
    # ==========================================

    ema9_15m = float(

        ema9_15m_series.iloc[-1]

    )

    ema21_15m = float(

        ema21_15m_series.iloc[-1]

    )

    if ema9_15m > ema21_15m:

        trend_15m = "BULLISH"

    else:

        trend_15m = "BEARISH"

    # ==========================================
    # 1H TREND
    # ==========================================

    ema9_1h = float(

        ema9_1h_series.iloc[-1]

    )

    ema21_1h = float(

        ema21_1h_series.iloc[-1]

    )

    if ema9_1h > ema21_1h:

        trend_1h = "BULLISH"

    else:

        trend_1h = "BEARISH"

    # ==========================================
    # VOLUME SPIKE DETECTION
    # ==========================================

    latest_volume = float(

        volume_5m.iloc[-1]

    )

    average_volume = float(

        volume_5m.tail(20).mean()

    )

    volume_spike = (

        latest_volume >

        average_volume * 1.5

    )

    # ==========================================
    # VOLATILITY DETECTION
    # ==========================================

    latest_atr = float(

        atr_5m.iloc[-1]

    )

    average_atr = float(

        atr_5m.tail(20).mean()

    )

    high_volatility = (

        latest_atr >

        average_atr * 1.2

    )

    # ==========================================
    # RETURN DATA
    # ==========================================

    return {

        "trend_15m": trend_15m,

        "trend_1h": trend_1h,

        "volume_spike": volume_spike,

        "high_volatility": high_volatility

    }

