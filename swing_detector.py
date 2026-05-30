
import pandas as pd


# ==========================================
# DETECT SWING HIGHS & LOWS
# ==========================================

def detect_swings(df):

    swing_highs = []

    swing_lows = []

    highs = df["High"].squeeze()

    lows = df["Low"].squeeze()

    # ==========================================
    # SWING HIGH
    # ==========================================

    for i in range(2, len(df) - 2):

        if (

            highs.iloc[i] >

            highs.iloc[i - 1]

            and

            highs.iloc[i] >

            highs.iloc[i - 2]

            and

            highs.iloc[i] >

            highs.iloc[i + 1]

            and

            highs.iloc[i] >

            highs.iloc[i + 2]

        ):

            swing_highs.append(

                (

                    i,

                    float(highs.iloc[i])

                )

            )

    # ==========================================
    # SWING LOW
    # ==========================================

    for i in range(2, len(df) - 2):

        if (

            lows.iloc[i] <

            lows.iloc[i - 1]

            and

            lows.iloc[i] <

            lows.iloc[i - 2]

            and

            lows.iloc[i] <

            lows.iloc[i + 1]

            and

            lows.iloc[i] <

            lows.iloc[i + 2]

        ):

            swing_lows.append(

                (

                    i,

                    float(lows.iloc[i])

                )

            )

    return (

        swing_highs,

        swing_lows

    )

