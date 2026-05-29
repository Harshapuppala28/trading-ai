from scipy.signal import find_peaks

import numpy as np


# ==========================================
# DOUBLE BOTTOM
# ==========================================

def detect_double_bottom(df):

    prices = df['Close'].values

    inverted = -prices

    valleys, _ = find_peaks(
        inverted,
        distance=10
    )

    if len(valleys) < 2:

        return False

    v1 = valleys[-1]

    v2 = valleys[-2]

    p1 = prices[v1]

    p2 = prices[v2]

    similarity = abs(p1 - p2) / p1

    if similarity < 0.005:

        return True

    return False


# ==========================================
# DOUBLE TOP
# ==========================================

def detect_double_top(df):

    prices = df['Close'].values

    peaks, _ = find_peaks(
        prices,
        distance=10
    )

    if len(peaks) < 2:

        return False

    p1 = peaks[-1]

    p2 = peaks[-2]

    price1 = prices[p1]

    price2 = prices[p2]

    similarity = abs(
        price1 - price2
    ) / price1

    if similarity < 0.005:

        return True

    return False


# ==========================================
# BULLISH RSI DIVERGENCE
# ==========================================

def detect_bullish_rsi_divergence(df):

    recent = df.tail(10)

    price1 = recent['Close'].iloc[-5]

    price2 = recent['Close'].iloc[-1]

    rsi1 = recent['RSI'].iloc[-5]

    rsi2 = recent['RSI'].iloc[-1]

    if (
        price2 < price1
        and rsi2 > rsi1
    ):

        return True

    return False


# ==========================================
# BEARISH RSI DIVERGENCE
# ==========================================

def detect_bearish_rsi_divergence(df):

    recent = df.tail(10)

    price1 = recent['Close'].iloc[-5]

    price2 = recent['Close'].iloc[-1]

    rsi1 = recent['RSI'].iloc[-5]

    rsi2 = recent['RSI'].iloc[-1]

    if (
        price2 > price1
        and rsi2 < rsi1
    ):

        return True

    return False


# ==========================================
# BULLISH ENGULFING
# ==========================================

def detect_bullish_engulfing(df):

    latest = df.iloc[-1]

    previous = df.iloc[-2]

    if (
        previous['Close'] < previous['Open']
        and latest['Close'] > latest['Open']
        and latest['Open'] < previous['Close']
        and latest['Close'] > previous['Open']
    ):

        return True

    return False


# ==========================================
# BEARISH ENGULFING
# ==========================================

def detect_bearish_engulfing(df):

    latest = df.iloc[-1]

    previous = df.iloc[-2]

    if (
        previous['Close'] > previous['Open']
        and latest['Close'] < latest['Open']
        and latest['Open'] > previous['Close']
        and latest['Close'] < previous['Open']
    ):

        return True

    return False


# ==========================================
# SUPPORT
# ==========================================

def detect_support(df):

    latest = df.iloc[-1]

    recent_low = df['Low'].tail(20).min()

    distance = abs(
        latest['Close'] - recent_low
    ) / latest['Close']

    if distance < 0.003:

        return True

    return False


# ==========================================
# RESISTANCE
# ==========================================

def detect_resistance(df):

    latest = df.iloc[-1]

    recent_high = df['High'].tail(20).max()

    distance = abs(
        latest['Close'] - recent_high
    ) / latest['Close']

    if distance < 0.003:

        return True

    return False


# ==========================================
# SHOOTING STAR
# ==========================================

def detect_shooting_star(df):

    latest = df.iloc[-1]

    body = abs(
        latest['Close'] - latest['Open']
    )

    upper_wick = (
        latest['High']
        - max(
            latest['Close'],
            latest['Open']
        )
    )

    lower_wick = (
        min(
            latest['Close'],
            latest['Open']
        )
        - latest['Low']
    )

    if (
        upper_wick > body * 2
        and lower_wick < body
        and latest['Close'] < latest['Open']
    ):

        return True

    return False


# ==========================================
# HAMMER
# ==========================================

def detect_hammer(df):

    latest = df.iloc[-1]

    body = abs(
        latest['Close'] - latest['Open']
    )

    lower_wick = (
        min(
            latest['Close'],
            latest['Open']
        )
        - latest['Low']
    )

    upper_wick = (
        latest['High']
        - max(
            latest['Close'],
            latest['Open']
        )
    )

    if (
        lower_wick > body * 2
        and upper_wick < body
    ):

        return True

    return False


# ==========================================
# DOJI
# ==========================================

def detect_doji(df):

    latest = df.iloc[-1]

    body = abs(
        latest['Close'] - latest['Open']
    )

    candle_range = (
        latest['High'] - latest['Low']
    )

    if candle_range == 0:

        return False

    if body / candle_range < 0.1:

        return True

    return False


# ==========================================
# HEAD AND SHOULDERS
# ==========================================

def detect_head_and_shoulders(df):

    prices = df['Close'].values

    peaks, _ = find_peaks(
        prices,
        distance=5
    )

    if len(peaks) < 3:

        return False

    p1 = prices[peaks[-3]]

    p2 = prices[peaks[-2]]

    p3 = prices[peaks[-1]]

    if (
        p2 > p1
        and p2 > p3
        and abs(p1 - p3) / p1 < 0.02
    ):

        return True

    return False


# ==========================================
# INVERSE HEAD AND SHOULDERS
# ==========================================

def detect_inverse_head_and_shoulders(df):

    prices = df['Close'].values

    inverted = -prices

    valleys, _ = find_peaks(
        inverted,
        distance=5
    )

    if len(valleys) < 3:

        return False

    v1 = prices[valleys[-3]]

    v2 = prices[valleys[-2]]

    v3 = prices[valleys[-1]]

    if (
        v2 < v1
        and v2 < v3
        and abs(v1 - v3) / v1 < 0.02
    ):

        return True

    return False