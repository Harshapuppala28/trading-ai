import os
import time
import traceback

import yfinance as yf

from indicators import add_indicators

from pattern_detector import detect_patterns

from confidence_score import calculate_confidence

from market_strength import analyze_market_strength

from pattern_ranker import rank_patterns

from market_bias import calculate_market_bias

from trade_decision import generate_trade_decision

from risk_manager import calculate_trade_levels

from slack_notifier import (

    send_slack_message,

    send_slack_image

)

from chart_generator import generate_chart

from trade_outcome_tracker import (
    evaluate_pending_trades
)

from mongodb_handler import save_pattern


# ==========================================
# ENV VARIABLES
# ==========================================

SLACK_WEBHOOK_URL = os.getenv(
    "SLACK_WEBHOOK_URL"
)

SLACK_BOT_TOKEN = os.getenv(
    "SLACK_BOT_TOKEN"
)



# ==========================================
# FETCH DATA
# ==========================================

def fetch_data():

    df_5m = yf.download(

        tickers="GC=F",

        interval="5m",

        period="1d",

        auto_adjust=True

    )

    df_15m = yf.download(

        tickers="GC=F",

        interval="15m",

        period="5d",

        auto_adjust=True

    )

    df_1h = yf.download(

        tickers="GC=F",

        interval="1h",

        period="1mo",

        auto_adjust=True

    )

    return (

        df_5m,
        df_15m,
        df_1h

    )

    # ==========================================
    # EMPTY DATA PROTECTION
    # ==========================================

    if (

        df_5m.empty

        or

        df_15m.empty

        or

        df_1h.empty

    ):

        print(

            "❌ No market data received. Retrying..."

        )

        return None, None, None

    return ( df_5m, df_15m, df_1h )    



# ==========================================
# MAIN LOOP
# ==========================================
last_alert_pattern = None
while True:

    try:

        print("\n===================================")

        print("📈 LIVE GOLD PATTERN SCANNER")

        print("===================================\n")

        # ==========================================
        # FETCH DATA
        # ==========================================

        df_5m, df_15m, df_1h = fetch_data()
        
        if (

              df_5m is None

              or

              df_15m is None

              or

              df_1h is None

            ):

              print(

                  "⏳ Retrying in 60 seconds..."

                )

        time.sleep(60)

        continue


        # ==========================================
        # ADD INDICATORS
        # ==========================================

        df_5m = add_indicators(df_5m)

        df_15m = add_indicators(df_15m)

        df_1h = add_indicators(df_1h)

        # ==========================================
        # DETECT PATTERNS
        # ==========================================

        detected_patterns = detect_patterns(
            df_5m
        )

        # ==========================================
        # RANK PATTERNS
        # ==========================================

        ranked_patterns = rank_patterns(
            detected_patterns
        )

        primary_pattern = (

            ranked_patterns[0][0]

            if ranked_patterns

            else "NONE"

        )

        # ==========================================
        # MARKET STRENGTH
        # ==========================================

        market_data = analyze_market_strength(

            df_5m,
            df_15m,
            df_1h

        )

        # ==========================================
        # CONFIDENCE SCORE
        # ==========================================

        bullish_score, bearish_score = (

            calculate_confidence(

                detected_patterns,

                market_data

            )

        )

        # ==========================================
        # MARKET BIAS
        # ==========================================

        market_bias = calculate_market_bias(

            ranked_patterns,

            market_data

        )

        # ==========================================
        # TRADE DECISION
        # ==========================================

        trade_decision = (

            generate_trade_decision(

                market_bias,

                bullish_score,

                bearish_score,

                primary_pattern

            )

        )

        # ==========================================
        # RISK LEVELS
        # ==========================================

        trade_levels = (

            calculate_trade_levels(

                df_5m,

                trade_decision['decision']

            )

        )

        # ==========================================
        # DISPLAY DATA
        # ==========================================

        print("📊 Latest 5m Market Data:\n")

        print(df_5m.tail())

        print(
            f"\n📈 15m Trend: {market_data['trend_15m']}"
        )

        print(
            f"📈 1h Trend: {market_data['trend_1h']}"
        )

        print(
            f"\n📊 Volume Spike: {market_data['volume_spike']}"
        )

        print(
            f"⚡ High Volatility: {market_data['high_volatility']}"
        )

        print(
            f"\n🧠 MARKET BIAS: {market_bias}"
        )

        print(

            f"\n🎯 TRADE DECISION: "

            f"{trade_decision['decision']}"

        )

        print(

            f"📊 Signal Strength: "

            f"{trade_decision['strength']}"

        )

        print(

            f"\n💰 Entry: "

            f"{trade_levels['entry']}"

        )

        print(

            f"🛑 Stop Loss: "

            f"{trade_levels['stop_loss']}"

        )

        print(

            f"🎯 Take Profit: "

            f"{trade_levels['take_profit']}"

        )

        print(

            f"⚖️ Risk/Reward: "

            f"{trade_levels['risk_reward']}"

        )

        print("\n🎯 PRIMARY PATTERN:\n")

        print(primary_pattern)

        print("\n📌 ALL DETECTED PATTERNS:\n")

        for pattern, score in ranked_patterns:

            print(
                f"{pattern} | Score: {score}"
            )

        print("\n========================\n")

        print(
            f"🔥 BULLISH CONFIDENCE: {bullish_score}%"
        )

        print(
            f"⚠️ BEARISH CONFIDENCE: {bearish_score}%"
        )

        # ==========================================
        # ALERTS
        # ==========================================

        if (

              (bullish_score >= 80 or bearish_score >= 80)

               and

               primary_pattern != last_alert_pattern

        ):

            latest_price = float(

                df_5m["Close"]

                .squeeze()

                .iloc[-1]

            )

            alert_message = f"""
🚨 ELITE TRADING SETUP DETECTED 🚨

🎯 PRIMARY PATTERN:
{primary_pattern}

📌 Ranked Patterns:
{chr(10).join([f"{p} ({s})" for p, s in ranked_patterns])}

🧠 Market Bias:
{market_bias}

🎯 Trade Decision:
{trade_decision['decision']}

📊 Signal Strength:
{trade_decision['strength']}

💰 Entry:
{trade_levels['entry']}

🛑 Stop Loss:
{trade_levels['stop_loss']}

🎯 Take Profit:
{trade_levels['take_profit']}

⚖️ Risk/Reward:
{trade_levels['risk_reward']}

🔥 Bullish Confidence:
{bullish_score}%

⚠️ Bearish Confidence:
{bearish_score}%

💰 Current Price:
{latest_price}
"""

            chart_path = generate_chart(

                df_5m,
                primary_pattern

            )

            send_slack_message(

                SLACK_WEBHOOK_URL,

                alert_message

            )

            
            send_slack_image(

                 SLACK_BOT_TOKEN,

                chart_path

            )
            last_alert_pattern = primary_pattern


            print(
                f"\n📸 Chart Saved: {chart_path}"
            )

            save_pattern({

                "primary_pattern": primary_pattern,

                "ranked_patterns": ranked_patterns,

                "bullish_score": bullish_score,

                "bearish_score": bearish_score,

                "market_bias": market_bias,

                "trade_decision": trade_decision,

                "trade_levels": trade_levels,

                "price": latest_price,

                "trend_15m": market_data["trend_15m"],

                "trend_1h": market_data["trend_1h"]

            })

        else:

            print(
                "\n❌ NO ELITE HIGH CONFIDENCE SETUP"
            )

        print("\n========================\n")

        evaluate_pending_trades()

        print(
            "\n⏳ Waiting 5 minutes for next candle..."
        )

        time.sleep(300)

    except Exception:

        print("\n❌ FULL ERROR TRACE:\n")

        traceback.print_exc()

        time.sleep(30)