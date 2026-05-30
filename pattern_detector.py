import pandas as pd

from swing_detector import detect_swings

from breakout_confirmation import (
    breakout_confirmed
)


# ==========================================
# DETECT SWING HIGHS
# ==========================================

def is_swing_high(high_series, i):

    return (

        high_series.iloc[i]

        >

        high_series.iloc[i - 1]

        and

        high_series.iloc[i]

        >

        high_series.iloc[i + 1]

    )


# ==========================================
# DETECT SWING LOWS
# ==========================================

def is_swing_low(low_series, i):

    return (

        low_series.iloc[i]

        <

        low_series.iloc[i - 1]

        and

        low_series.iloc[i]

        <

        low_series.iloc[i + 1]

    )


# ==========================================
# MAIN PATTERN DETECTOR
# ==========================================

def detect_patterns(df):

    patterns = []

    # ==========================================
    # FIX MULTI INDEX
    # ==========================================

    close_series = df["Close"].squeeze()

    open_series = df["Open"].squeeze()

    high_series = df["High"].squeeze()

    low_series = df["Low"].squeeze()

    rsi_series = df["RSI"].squeeze()

    # ==========================================
    # LATEST VALUES
    # ==========================================

    latest_close = float(
        close_series.iloc[-1]
    )

    latest_open = float(
        open_series.iloc[-1]
    )

    latest_high = float(
        high_series.iloc[-1]
    )

    latest_low = float(
        low_series.iloc[-1]
    )

    latest_rsi = float(
        rsi_series.iloc[-1]
    )

    # ==========================================
    # SWING DETECTION
    # ==========================================

    swing_highs, swing_lows = (
        detect_swings(df)
    )

    # ==========================================
    # CANDLE DETAILS
    # ==========================================

    candle_size = abs(
        latest_close - latest_open
    )

    wick_size = (
        latest_high - latest_low
    )

    upper_wick = (
        latest_high -
        max(latest_close, latest_open)
    )

    lower_wick = (
        min(latest_close, latest_open)
        - latest_low
    )

    # ==========================================
    # DOJI
    # ==========================================

    if candle_size < (wick_size * 0.1):

        patterns.append(
            "⚖️ DOJI"
        )

    # ==========================================
    # HAMMER
    # ==========================================

    if (

        lower_wick >
        candle_size * 2

        and

        upper_wick < candle_size

    ):

        patterns.append(
            "🔨 HAMMER"
        )

    # ==========================================
    # SHOOTING STAR
    # ==========================================

    if (

        upper_wick >
        candle_size * 2

        and

        lower_wick < candle_size

    ):

        patterns.append(
            "🌠 SHOOTING STAR"
        )

    # ==========================================
    # RSI
    # ==========================================

    if latest_rsi < 30:

        patterns.append(
            "🚀 BULLISH RSI DIVERGENCE"
        )

    if latest_rsi > 70:

        patterns.append(
            "📉 BEARISH RSI DIVERGENCE"
        )

    # ==========================================
    # DOUBLE TOP
    # ==========================================

    if len(swing_highs) >= 2:

        top1 = swing_highs[-1][1]

        top2 = swing_highs[-2][1]

        if abs(top1 - top2) < 5:

            patterns.append(
                "📉 DOUBLE TOP"
            )

    # ==========================================
    # DOUBLE BOTTOM
    # ==========================================

    if len(swing_lows) >= 2:

        low1 = swing_lows[-2][1]

        low2 = swing_lows[-1][1]

        difference = abs(
            low1 - low2
        )

        if difference < 3:

            middle_high = float(

                df["High"]
                .squeeze()
                .iloc[
                    swing_lows[-2][0]:
                    swing_lows[-1][0]
                ]
                .max()

            )

            if breakout_confirmed(

                df,
                middle_high,
                "bullish"

            ):

                patterns.append(
                    "📈 DOUBLE BOTTOM"
                )

    # ==========================================
    # HEAD AND SHOULDERS
    # ==========================================

    if len(swing_highs) >= 3:

        left_shoulder = swing_highs[-3][1]

        head = swing_highs[-2][1]

        right_shoulder = swing_highs[-1][1]

        shoulder_difference = abs(
            left_shoulder -
            right_shoulder
        )

        if shoulder_difference < 5:

            if (

                head > left_shoulder

                and

                head > right_shoulder

            ):

                neckline = float(

                    df["Low"]
                    .squeeze()
                    .iloc[
                        swing_highs[-3][0]:
                        swing_highs[-1][0]
                    ]
                    .min()

                )

                if breakout_confirmed(

                    df,
                    neckline,
                    "bearish"

                ):

                    patterns.append(
                        "📉 HEAD AND SHOULDERS"
                    )

    # ==========================================
    # INVERSE HEAD AND SHOULDERS
    # ==========================================

    if len(swing_lows) >= 3:

        left_shoulder = swing_lows[-3][1]

        head = swing_lows[-2][1]

        right_shoulder = swing_lows[-1][1]

        if (

            head < left_shoulder

            and

            head < right_shoulder

            and

            abs(
                left_shoulder -
                right_shoulder
            ) < 5

        ):

            patterns.append(
                "🔄 INVERSE HEAD AND SHOULDERS"
            )

    # ==========================================
    # SUPPORT ZONE
    # ==========================================

    support = float(

        low_series
        .tail(20)
        .min()

    )

    if latest_close <= support * 1.01:

        patterns.append(
            "🟩 SUPPORT ZONE"
        )

    # ==========================================
    # ASCENDING TRIANGLE
    # ==========================================

    if (

        len(swing_highs) >= 2

        and

        len(swing_lows) >= 2

    ):

        high1 = swing_highs[-2][1]

        high2 = swing_highs[-1][1]

        low1 = swing_lows[-2][1]

        low2 = swing_lows[-1][1]

        resistance_difference = abs(
            high1 - high2
        )

        if (

            resistance_difference < 3

            and

            low2 > low1

        ):

            breakout_level = float(
                max(high1, high2)
            )

            if breakout_confirmed(

                df,
                breakout_level,
                "bullish"

            ):

                patterns.append(
                    "📈 ASCENDING TRIANGLE"
                )

    # ==========================================
    # DESCENDING TRIANGLE
    # ==========================================

    if (

        len(swing_highs) >= 2

        and

        len(swing_lows) >= 2

    ):

        high1 = swing_highs[-2][1]

        high2 = swing_highs[-1][1]

        low1 = swing_lows[-2][1]

        low2 = swing_lows[-1][1]

        support_difference = abs(
            low1 - low2
        )

        if (

            support_difference < 3

            and

            high2 < high1

        ):

            breakout_level = float(
                min(low1, low2)
            )

            if breakout_confirmed(

                df,
                breakout_level,
                "bearish"

            ):

                patterns.append(
                    "🔻 DESCENDING TRIANGLE"
                )

    # ==========================================
    # SYMMETRICAL TRIANGLE
    # ==========================================

    if (

        len(swing_highs) >= 2

        and

        len(swing_lows) >= 2

    ):

        high1 = swing_highs[-2][1]

        high2 = swing_highs[-1][1]

        low1 = swing_lows[-2][1]

        low2 = swing_lows[-1][1]

        if (

            high2 < high1

            and

            low2 > low1

        ):

            if latest_close > high2:

                if breakout_confirmed(

                    df,
                    high2,
                    "bullish"

                ):

                    patterns.append(
                        "🔺 SYMMETRICAL TRIANGLE BULLISH"
                    )

            elif latest_close < low2:

                if breakout_confirmed(

                    df,
                    low2,
                    "bearish"

                ):

                    patterns.append(
                        "🔻 SYMMETRICAL TRIANGLE BEARISH"
                    )

    # ==========================================
    # RISING WEDGE
    # ==========================================

    if (

        len(swing_highs) >= 2

        and

        len(swing_lows) >= 2

    ):

        high1 = swing_highs[-2][1]

        high2 = swing_highs[-1][1]

        low1 = swing_lows[-2][1]

        low2 = swing_lows[-1][1]

        if (

            high2 > high1

            and

            low2 > low1

        ):

            high_slope = high2 - high1

            low_slope = low2 - low1

            if low_slope > high_slope:

                breakout_level = float(
                    min(low1, low2)
                )

                if breakout_confirmed(

                    df,
                    breakout_level,
                    "bearish"

                ):

                    patterns.append(
                        "📉 RISING WEDGE"
                    )

    # ==========================================
    # FALLING WEDGE
    # ==========================================

    if (

        len(swing_highs) >= 2

        and

        len(swing_lows) >= 2

    ):

        high1 = swing_highs[-2][1]

        high2 = swing_highs[-1][1]

        low1 = swing_lows[-2][1]

        low2 = swing_lows[-1][1]

        if (

            high2 < high1

            and

            low2 < low1

        ):

            high_slope = abs(
                high2 - high1
            )

            low_slope = abs(
                low2 - low1
            )

            if high_slope > low_slope:

                breakout_level = float(
                    max(high1, high2)
                )

                if breakout_confirmed(

                    df,
                    breakout_level,
                    "bullish"

                ):

                    patterns.append(
                        "📈 FALLING WEDGE"
                    )

    # ==========================================
    # CUP AND HANDLE
    # ==========================================

    closes = (
        close_series
        .tail(30)
        .values
    )

    if len(closes) >= 30:

        left_side = closes[:10]

        bottom_zone = closes[10:20]

        right_side = closes[20:25]

        handle_zone = closes[25:]

        left_avg = sum(left_side) / len(left_side)

        bottom_avg = sum(bottom_zone) / len(bottom_zone)

        right_avg = sum(right_side) / len(right_side)

        handle_avg = sum(handle_zone) / len(handle_zone)

        if (

            bottom_avg < left_avg

            and

            bottom_avg < right_avg

        ):

            if right_avg > bottom_avg:

                if handle_avg < right_avg:

                    if latest_close > right_avg:

                        breakout_level = float(
                            max(right_side)
                        )

                        if breakout_confirmed(

                            df,
                            breakout_level,
                            "bullish"

                        ):

                            patterns.append(
                                "☕ CUP AND HANDLE"
                            )

    # ==========================================
    # ROUNDING BOTTOM
    # ==========================================

    closes = (
        close_series
        .tail(40)
        .values
    )

    if len(closes) >= 40:

        first_part = closes[:10]

        middle_part = closes[10:30]

        last_part = closes[30:]

        first_avg = sum(first_part) / len(first_part)

        middle_avg = sum(middle_part) / len(middle_part)

        last_avg = sum(last_part) / len(last_part)

        if (

            middle_avg < first_avg

            and

            middle_avg < last_avg

        ):

            if last_avg > middle_avg:

                if latest_close > first_avg:

                    patterns.append(
                        "🌙 ROUNDING BOTTOM"
                    )

    # ==========================================
    # LAST 3 CANDLES
    # ==========================================

    latest = df.tail(3)

    open1 = float(
        latest["Open"].squeeze().iloc[-3]
    )

    close1 = float(
        latest["Close"].squeeze().iloc[-3]
    )

    open2 = float(
        latest["Open"].squeeze().iloc[-2]
    )

    close2 = float(
        latest["Close"].squeeze().iloc[-2]
    )

    open3 = float(
        latest["Open"].squeeze().iloc[-1]
    )

    close3 = float(
        latest["Close"].squeeze().iloc[-1]
    )

    high3 = float(
        latest["High"].squeeze().iloc[-1]
    )

    low3 = float(
        latest["Low"].squeeze().iloc[-1]
    )

    # ==========================================
    # ENGULFING
    # ==========================================

    if (

        close2 < open2

        and

        close3 > open3

        and

        open3 < close2

        and

        close3 > open2

    ):

        patterns.append(
            "🚀 BULLISH ENGULFING"
        )

    if (

        close2 > open2

        and

        close3 < open3

        and

        open3 > close2

        and

        close3 < open2

    ):

        patterns.append(
            "📉 BEARISH ENGULFING"
        )

    # ==========================================
    # MORNING STAR
    # ==========================================

    if (

        close1 < open1

        and

        abs(close2 - open2)
        < abs(close1 - open1)

        and

        close3 > open3

    ):

        patterns.append(
            "🌅 MORNING STAR"
        )

    # ==========================================
    # EVENING STAR
    # ==========================================

    if (

        close1 > open1

        and

        abs(close2 - open2)
        < abs(close1 - open1)

        and

        close3 < open3

    ):

        patterns.append(
            "🌇 EVENING STAR"
        )

    # ==========================================
    # BULL FLAG
    # ==========================================

    if len(close_series) >= 10:

        recent_move = (

            close_series.iloc[-5]
            -
            close_series.iloc[-10]

        )

        pullback = (

            close_series.iloc[-1]
            -
            close_series.iloc[-5]

        )

        if (

            recent_move > 15

            and

            pullback < 0

            and

            abs(pullback)
            < recent_move * 0.5

        ):

            patterns.append(
                "🚩 BULL FLAG"
            )

    # ==========================================
    # BEAR FLAG
    # ==========================================

    if len(close_series) >= 10:

        recent_move = (

            close_series.iloc[-10]
            -
            close_series.iloc[-5]

        )

        pullback = (

            close_series.iloc[-1]
            -
            close_series.iloc[-5]

        )

        if (

            recent_move > 15

            and

            pullback > 0

            and

            pullback < recent_move * 0.5

        ):

            patterns.append(
                "🚩 BEAR FLAG"
            )

    # ==========================================
    # PENNANT
    # ==========================================

    if (

        len(swing_highs) >= 2

        and

        len(swing_lows) >= 2

    ):

        high1 = swing_highs[-2][1]

        high2 = swing_highs[-1][1]

        low1 = swing_lows[-2][1]

        low2 = swing_lows[-1][1]

        if (

            high2 < high1

            and

            low2 > low1

        ):

            patterns.append(
                "🎯 PENNANT"
            )

    # ==========================================
    # RESISTANCE ZONE
    # ==========================================

    resistance = float(

        high_series
        .tail(20)
        .max()

    )

    if latest_close >= resistance * 0.99:

        patterns.append(
            "🟥 RESISTANCE ZONE"
        )

    # ==========================================
    # PRIORITY
    # ==========================================

    priority_patterns = [

        "📉 HEAD AND SHOULDERS",

        "🔄 INVERSE HEAD AND SHOULDERS",

        "📉 DOUBLE TOP",

        "📈 DOUBLE BOTTOM",

        "📈 ASCENDING TRIANGLE",

        "🔻 DESCENDING TRIANGLE",

        "🔺 SYMMETRICAL TRIANGLE BULLISH",

        "🔻 SYMMETRICAL TRIANGLE BEARISH",

        "📉 RISING WEDGE",

        "📈 FALLING WEDGE",

        "☕ CUP AND HANDLE",

        "🌙 ROUNDING BOTTOM",

        "🚩 BULL FLAG",

        "🚩 BEAR FLAG",

        "🎯 PENNANT"

    ]

    primary_pattern = None

    confirmations = []

    for p in priority_patterns:

        if p in patterns:

            primary_pattern = p

            break

    for p in patterns:

        if p != primary_pattern:

            confirmations.append(p)

    # ==========================================
    # FINAL OUTPUT
    # ==========================================

    final_patterns = []

    if primary_pattern:

        final_patterns.append(
            primary_pattern
        )

    final_patterns.extend(
        confirmations
    )

    return final_patterns