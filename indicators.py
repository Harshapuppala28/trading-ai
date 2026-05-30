import pandas as pd


def add_indicators(df):

    # EMA
    df["EMA_9"] = (
        df["Close"]
        .ewm(span=9, adjust=False)
        .mean()
    )

    df["EMA_21"] = (
        df["Close"]
        .ewm(span=21, adjust=False)
        .mean()
    )

    # RSI
    delta = df["Close"].diff()

    gain = delta.where(
        delta > 0,
        0
    )

    loss = -delta.where(
        delta < 0,
        0
    )

    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = (
        100 - (100 / (1 + rs))
    )

    # ATR
    high_low = (
        df["High"] - df["Low"]
    )

    high_close = (
        (df["High"] - df["Close"].shift())
        .abs()
    )

    low_close = (
        (df["Low"] - df["Close"].shift())
        .abs()
    )

    ranges = pd.concat(
        [
            high_low,
            high_close,
            low_close
        ],
        axis=1
    )

    true_range = ranges.max(axis=1)

    df["ATR"] = (
        true_range
        .rolling(14)
        .mean()
    )

    # REMOVE NaN ROWS
    df = df.dropna()

    return df