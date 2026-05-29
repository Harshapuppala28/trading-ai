def detect_volume_spike(df):

    latest = df.iloc[-1]

    if latest['Volume'] > (
        latest['Volume_MA'] * 1.5
    ):

        return True

    return False


def detect_high_volatility(df):

    latest = df.iloc[-1]

    average_atr = df['ATR'].mean()

    if latest['ATR'] > (
        average_atr * 1.5
    ):

        return True

    return False