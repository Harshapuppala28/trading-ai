import pandas as pd


def calculate_rsi(data, period=14):

    delta = data['Close'].diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()

    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_atr(data, period=14):

    high_low = data['High'] - data['Low']

    high_close = (
        data['High'] - data['Close'].shift()
    ).abs()

    low_close = (
        data['Low'] - data['Close'].shift()
    ).abs()

    ranges = pd.concat(
        [
            high_low,
            high_close,
            low_close
        ],
        axis=1
    )

    true_range = ranges.max(axis=1)

    atr = true_range.rolling(period).mean()

    return atr


def add_indicators(df):

    df['RSI'] = calculate_rsi(df)

    df['EMA_9'] = (
        df['Close']
        .ewm(span=9, adjust=False)
        .mean()
    )

    df['EMA_21'] = (
        df['Close']
        .ewm(span=21, adjust=False)
        .mean()
    )

    df['ATR'] = calculate_atr(df)

    df['Volume_MA'] = (
        df['Volume']
        .rolling(20)
        .mean()
    )

    return df