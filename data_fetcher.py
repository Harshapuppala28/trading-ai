import os
import time
import pytz
import pandas as pd
import yfinance as yf

from datetime import datetime

from indicators import add_indicators

from mongodb_handler import save_pattern

from slack_notifier import (
    send_slack_image
)

from confidence_score import (
    calculate_bullish_score,
    calculate_bearish_score
)

from market_strength import (
    detect_volume_spike,
    detect_high_volatility
)

from pattern_detector import (

    detect_double_bottom,
    detect_double_top,

    detect_bullish_rsi_divergence,
    detect_bearish_rsi_divergence,

    detect_bullish_engulfing,
    detect_bearish_engulfing,

    detect_support,
    detect_resistance,

    detect_shooting_star,

    detect_hammer,
    detect_doji,

    detect_head_and_shoulders,
    detect_inverse_head_and_shoulders
)

from trade_outcome_tracker import (
    evaluate_pending_trades
)

from chart_generator import (
    generate_chart
)

pd.set_option(
    'display.max_columns',
    None
)

symbol = "GC=F"

india = pytz.timezone(
    'Asia/Kolkata'
)


# ==========================================
# TREND DETECTION
# ==========================================

def get_trend(df):

    latest = df.iloc[-1]

    if latest['EMA_9'] > latest['EMA_21']:

        return "BULLISH"

    return "BEARISH"


# ==========================================
# CREATE CHART FOLDER
# ==========================================

if not os.path.exists("charts"):

    os.makedirs("charts")


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    print("\n===================================")

    print("📈 LIVE GOLD PATTERN SCANNER")

    print("===================================")

    print(
        f"\n🕒 India Time: "
        f"{datetime.now(india)}"
    )

    ticker = yf.Ticker(symbol)

    # ==========================================
    # FETCH DATA
    # ==========================================

    df_5m = ticker.history(
        period="1d",
        interval="5m"
    )

    df_15m = ticker.history(
        period="5d",
        interval="15m"
    )

    df_1h = ticker.history(
        period="1mo",
        interval="1h"
    )

    # ==========================================
    # INDICATORS
    # ==========================================

    df_5m = add_indicators(df_5m)

    df_15m = add_indicators(df_15m)

    df_1h = add_indicators(df_1h)

    latest = df_5m.iloc[-1]

    # ==========================================
    # TRENDS
    # ==========================================

    trend_15m = get_trend(df_15m)

    trend_1h = get_trend(df_1h)

    # ==========================================
    # MARKET CONDITIONS
    # ==========================================

    volume_spike = detect_volume_spike(df_5m)

    high_volatility = detect_high_volatility(df_5m)

    # ==========================================
    # PRINT DATA
    # ==========================================

    print("\n📊 Latest 5m Market Data:\n")

    print(
        df_5m[
            [
                'Open',
                'High',
                'Low',
                'Close',
                'Volume',
                'RSI',
                'ATR',
                'EMA_9',
                'EMA_21'
            ]
        ].tail()
    )

    print("\n📈 15m Trend:", trend_15m)

    print("📈 1h Trend:", trend_1h)

    print(
        "\n📊 Volume Spike:",
        volume_spike
    )

    print(
        "⚡ High Volatility:",
        high_volatility
    )

    # ==========================================
    # PATTERNS
    # ==========================================

    double_bottom = detect_double_bottom(df_5m)

    double_top = detect_double_top(df_5m)

    bullish_div = detect_bullish_rsi_divergence(df_5m)

    bearish_div = detect_bearish_rsi_divergence(df_5m)

    bullish_engulf = detect_bullish_engulfing(df_5m)

    bearish_engulf = detect_bearish_engulfing(df_5m)

    support = detect_support(df_5m)

    resistance = detect_resistance(df_5m)

    shooting_star = detect_shooting_star(df_5m)

    hammer = detect_hammer(df_5m)

    doji = detect_doji(df_5m)

    head_shoulders = detect_head_and_shoulders(df_5m)

    inverse_head_shoulders = (
        detect_inverse_head_and_shoulders(df_5m)
    )

    # ==========================================
    # PRINT PATTERNS
    # ==========================================

    print("\n📌 DETECTED PATTERNS:\n")

    pattern_found = False

    if double_bottom:

        print("📈 DOUBLE BOTTOM")

        pattern_found = True

    if double_top:

        print("📉 DOUBLE TOP")

        pattern_found = True

    if bullish_div:

        print("🚀 BULLISH RSI DIVERGENCE")

        pattern_found = True

    if bearish_div:

        print("⚠️ BEARISH RSI DIVERGENCE")

        pattern_found = True

    if bullish_engulf:

        print("🟢 BULLISH ENGULFING")

        pattern_found = True

    if bearish_engulf:

        print("🔴 BEARISH ENGULFING")

        pattern_found = True

    if support:

        print("🟩 SUPPORT ZONE")

        pattern_found = True

    if resistance:

        print("🟥 RESISTANCE ZONE")

        pattern_found = True

    if shooting_star:

        print("⭐ SHOOTING STAR")

        pattern_found = True

    if hammer:

        print("🔨 HAMMER")

        pattern_found = True

    if doji:

        print("⚖️ DOJI")

        pattern_found = True

    if head_shoulders:

        print("👤 HEAD AND SHOULDERS")

        pattern_found = True

    if inverse_head_shoulders:

        print("🔄 INVERSE HEAD AND SHOULDERS")

        pattern_found = True

    if not pattern_found:

        print(
            "❌ NO MAJOR PATTERNS DETECTED"
        )

    # ==========================================
    # CONFIDENCE SCORING
    # ==========================================

    bullish_score = calculate_bullish_score(
        double_bottom,
        bullish_div,
        support,
        bullish_engulf,
        volume_spike,
        high_volatility,
        trend_15m,
        trend_1h
    )

    bearish_score = calculate_bearish_score(
        double_top,
        bearish_div,
        resistance,
        bearish_engulf,
        volume_spike,
        high_volatility,
        trend_15m,
        trend_1h
    )

    # ==========================================
    # EXTRA PATTERN BOOSTS
    # ==========================================

    if hammer:

        bullish_score += 10

    if inverse_head_shoulders:

        bullish_score += 15

    if head_shoulders:

        bearish_score += 15

    if shooting_star:

        bearish_score += 10

    if doji:

        bullish_score += 5

        bearish_score += 5

    bullish_score = min(
        bullish_score,
        100
    )

    bearish_score = min(
        bearish_score,
        100
    )

    print("\n========================")

    print(
        f"\n🔥 BULLISH CONFIDENCE: "
        f"{bullish_score}%"
    )

    print(
        f"⚠️ BEARISH CONFIDENCE: "
        f"{bearish_score}%"
    )

    # ==========================================
    # ELITE FILTERS
    # ==========================================

    bullish_allowed = (

        bullish_score >= 70

        and latest['RSI'] < 75

        and trend_15m == "BULLISH"

        and trend_1h == "BULLISH"

        and volume_spike is True

        and (
            hammer
            or bullish_div
            or bullish_engulf
            or inverse_head_shoulders
            or double_bottom
        )
    )

    bearish_allowed = (

        bearish_score >= 70

        and latest['RSI'] > 25

        and trend_15m == "BEARISH"

        and trend_1h == "BEARISH"

        and volume_spike is True

        and (
            shooting_star
            or bearish_div
            or bearish_engulf
            or head_shoulders
            or double_top
        )
    )

    # ==========================================
    # CONTRADICTION FILTER
    # ==========================================

    contradictory_patterns = (

        (double_bottom and double_top)

        or

        (bullish_engulf and bearish_engulf)

        or

        (head_shoulders and inverse_head_shoulders)
    )

    if contradictory_patterns:

        print(
            "\n❌ CONTRADICTORY PATTERNS DETECTED"
        )

        bullish_allowed = False

        bearish_allowed = False

    # ==========================================
    # BULLISH ALERT
    # ==========================================

    if bullish_allowed:

        print(
            "\n🚀 ELITE HIGH CONFIDENCE BULLISH SETUP"
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        chart_file = (
            f"charts/bullish_{timestamp}.png"
        )

        generate_chart(
            df_5m,
            chart_file
        )

        save_pattern(
            "ELITE HIGH CONFIDENCE BULLISH",
            latest,
            bullish_score,
            bearish_score,
            trend_15m,
            trend_1h,
            volume_spike,
            high_volatility
        )

        send_slack_image(

            "🚀 ELITE HIGH CONFIDENCE BULLISH SETUP\n\n"
            f"Bullish Score: {bullish_score}%\n"
            f"Price: {latest['Close']}\n"
            f"RSI: {latest['RSI']:.2f}\n"
            f"ATR: {latest['ATR']:.2f}\n"
            f"15m Trend: {trend_15m}\n"
            f"1h Trend: {trend_1h}",

            chart_file
        )

    # ==========================================
    # BEARISH ALERT
    # ==========================================

    if bearish_allowed:

        print(
            "\n⚠️ ELITE HIGH CONFIDENCE BEARISH SETUP"
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        chart_file = (
            f"charts/bearish_{timestamp}.png"
        )

        generate_chart(
            df_5m,
            chart_file
        )

        save_pattern(
            "ELITE HIGH CONFIDENCE BEARISH",
            latest,
            bullish_score,
            bearish_score,
            trend_15m,
            trend_1h,
            volume_spike,
            high_volatility
        )

        send_slack_image(

            "⚠️ ELITE HIGH CONFIDENCE BEARISH SETUP\n\n"
            f"Bearish Score: {bearish_score}%\n"
            f"Price: {latest['Close']}\n"
            f"RSI: {latest['RSI']:.2f}\n"
            f"ATR: {latest['ATR']:.2f}\n"
            f"15m Trend: {trend_15m}\n"
            f"1h Trend: {trend_1h}",

            chart_file
        )

    # ==========================================
    # NO ELITE SETUP
    # ==========================================

    if (
        not bullish_allowed
        and not bearish_allowed
    ):

        print(
            "\n❌ NO ELITE HIGH CONFIDENCE SETUP"
        )

    print("\n========================")

    # ==========================================
    # TRADE EVALUATION
    # ==========================================

    print(
        "\n📊 Evaluating Pending Trades..."
    )

    evaluate_pending_trades()

    # ==========================================
    # WAIT
    # ==========================================

    print(
        "\n⏳ Waiting 5 minutes "
        "for next candle...\n"
    )

    time.sleep(300)