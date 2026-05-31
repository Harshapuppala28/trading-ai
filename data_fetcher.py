import os
import time
import traceback
import datetime
import pytz
import pandas as pd  # Imported to handle multi-index checking

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
from trade_outcome_tracker import evaluate_pending_trades
from mongodb_handler import save_pattern

# ==========================================
# ENV VARIABLES
# ==========================================
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# ==========================================
# WEEKEND CHECKER FOR GOLD (GC=F)
# ==========================================
def is_market_open():
    """
    Returns True if Gold Markets (GC=F) are open, False if closed.
    Gold futures trade from Sunday 6:00 PM EST to Friday 5:00 PM EST.
    """
    tz = pytz.timezone('US/Eastern')
    now = datetime.datetime.now(tz)
    
    day = now.weekday()  # 0=Monday, 4=Friday, 5=Saturday, 6=Sunday
    hour = now.hour

    if day == 5:  # Saturday
        return False
    if day == 6 and hour < 18:  # Sunday before 6:00 PM EST
        return False
    if day == 4 and hour >= 17:  # Friday after 5:00 PM EST
        return False
    return True

# ==========================================
# FETCH DATA
# ==========================================
def fetch_data():
    try:
        # Weekend-safe adjustments: pulling at least 5 days for short intervals
        df_5m = yf.download(
            tickers="GC=F",
            interval="5m",
            period="5d",  # Changed from 1d to 5d so it has data on weekends
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

        # Fix yfinance Multi-Index Header issue for Pandas
        for df in [df_5m, df_15m, df_1h]:
            if df is not None and not df.empty and isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

        # ==========================================
        # EMPTY DATA PROTECTION (Moved above return)
        # ==========================================
        if df_5m is None or df_5m.empty or df_15m is None or df_15m.empty or df_1h is None or df_1h.empty:
            print("❌ No market data received from Yahoo Finance.")
            return None, None, None

        return df_5m, df_15m, df_1h   

    except Exception as e:
        print(f"❌ Error during yfinance download: {e}")
        return None, None, None

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
        # STOP LOOP IF MARKET IS CLOSED (Fixes Rate Limits)
        # ==========================================
        if not is_market_open():
            print("🛑 Gold market is closed for the weekend (EST).")
            print("⏳ Sleeping for 15 minutes to respect API rate limits...")
            time.sleep(900)  # Check back in 15 minutes
            continue

        # ==========================================
        # FETCH DATA
        # ==========================================
        df_5m, df_15m, df_1h = fetch_data()
        
        if df_5m is None or df_15m is None or df_1h is None:
            print("⏳ Data is empty or rate-limited. Retrying in 5 minutes...")
            time.sleep(300)
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
        detected_patterns = detect_patterns(df_5m)

        # ==========================================
        # RANK PATTERNS
        # ==========================================
        ranked_patterns = rank_patterns(detected_patterns)

        primary_pattern = (
            ranked_patterns[0][0]
            if ranked_patterns
            else "NONE"
        )

        # ==========================================
        # MARKET STRENGTH
        # ==========================================
        market_data = analyze_market_strength(df_5m, df_15m, df_1h)

        # ==========================================
        # CONFIDENCE SCORE
        # ==========================================
        bullish_score, bearish_score = calculate_confidence(detected_patterns, market_data)

        # ==========================================
        # MARKET BIAS
        # ==========================================
        market_bias = calculate_market_bias(ranked_patterns, market_data)

        # ==========================================
        # TRADE DECISION
        # ==========================================
        trade_decision = generate_trade_decision(
            market_bias,
            bullish_score,
            bearish_score,
            primary_pattern
        )

        # ==========================================
        # RISK LEVELS
        # ==========================================
        trade_levels = calculate_trade_levels(df_5m, trade_decision['decision'])

        # ==========================================
        # DISPLAY DATA
        # ==========================================
        print("📊 Latest 5m Market Data:\n")
        print(df_5m.tail())

        print(f"\n📈 15m Trend: {market_data['trend_15m']}")
        print(f"📈 1h Trend: {market_data['trend_1h']}")
        print(f"\n📊 Volume Spike: {market_data['volume_spike']}")
        print(f"⚡ High Volatility: {market_data['high_volatility']}")
        print(f"\n🧠 MARKET BIAS: {market_bias}")
        print(f"\n🎯 TRADE DECISION: {trade_decision['decision']}")
        print(f"📊 Signal Strength: {trade_decision['strength']}")
        print(f"\n💰 Entry: {trade_levels['entry']}")
        print(f"🛑 Stop Loss: {trade_levels['stop_loss']}")
        print(f"🎯 Take Profit: {trade_levels['take_profit']}")
        print(f"⚖️ Risk/Reward: {trade_levels['risk_reward']}")
        
        print("\n🎯 PRIMARY PATTERN:\n")
        print(primary_pattern)

        print("\n📌 ALL DETECTED PATTERNS:\n")
        for pattern, score in ranked_patterns:
            print(f"{pattern} | Score: {score}")

        print("\n========================\n")
        print(f"🔥 BULLISH CONFIDENCE: {bullish_score}%")
        print(f"⚠️ BEARISH CONFIDENCE: {bearish_score}%")

        # ==========================================
        # ALERTS
        # ==========================================
        if (bullish_score >= 80 or bearish_score >= 80) and primary_pattern != last_alert_pattern:
            latest_price = float(df_5m["Close"].squeeze().iloc[-1])

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

            chart_path = generate_chart(df_5m, primary_pattern)

            send_slack_message(SLACK_WEBHOOK_URL, alert_message)
            send_slack_image(SLACK_BOT_TOKEN, chart_path)
            last_alert_pattern = primary_pattern

            print(f"\n📸 Chart Saved: {chart_path}")

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
            print("\n❌ NO ELITE HIGH CONFIDENCE SETUP")

        print("\n========================\n")
        
        # Track previous open trades
        evaluate_pending_trades()

        print("\n⏳ Waiting 5 minutes for next candle...")
        time.sleep(300)

    except Exception:
        print("\n❌ FULL ERROR TRACE:\n")
        traceback.print_exc()
        time.sleep(30)