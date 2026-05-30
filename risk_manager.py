
# ==========================================
# RISK MANAGEMENT ENGINE
# ==========================================

def calculate_trade_levels(

    df,
    trade_decision

):

    latest_close = float(

        df["Close"]

        .squeeze()

        .iloc[-1]

    )

    latest_atr = float(

        df["ATR"]

        .squeeze()

        .iloc[-1]

    )

    # ==========================================
    # BUY SETUP
    # ==========================================

    if "BUY" in trade_decision:

        entry = latest_close

        stop_loss = (

            latest_close -

            (latest_atr * 1.5)

        )

        take_profit = (

            latest_close +

            (latest_atr * 3)

        )

    # ==========================================
    # SELL SETUP
    # ==========================================

    elif "SELL" in trade_decision:

        entry = latest_close

        stop_loss = (

            latest_close +

            (latest_atr * 1.5)

        )

        take_profit = (

            latest_close -

            (latest_atr * 3)

        )

    # ==========================================
    # NO TRADE
    # ==========================================

    else:

        return {

            "entry": None,

            "stop_loss": None,

            "take_profit": None,

            "risk_reward": None

        }

    # ==========================================
    # RISK / REWARD
    # ==========================================

    risk = abs(

        entry - stop_loss

    )

    reward = abs(

        take_profit - entry

    )

    rr_ratio = round(

        reward / risk,

        2

    )

    return {

        "entry": round(entry, 2),

        "stop_loss": round(stop_loss, 2),

        "take_profit": round(take_profit, 2),

        "risk_reward": rr_ratio

    }

