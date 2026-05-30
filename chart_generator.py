
import mplfinance as mpf

import pandas as pd


# ==========================================
# GENERATE CHART IMAGE
# ==========================================

def generate_chart(

    df,
    primary_pattern

):

    # ==========================================
    # FIX MULTI-INDEX COLUMNS
    # ==========================================

    chart_df = pd.DataFrame({

        "Open": df["Open"].squeeze(),

        "High": df["High"].squeeze(),

        "Low": df["Low"].squeeze(),

        "Close": df["Close"].squeeze(),

        "Volume": df["Volume"].squeeze()

    })

    # ==========================================
    # FORCE NUMERIC TYPES
    # ==========================================

    chart_df["Open"] = pd.to_numeric(

        chart_df["Open"]

    )

    chart_df["High"] = pd.to_numeric(

        chart_df["High"]

    )

    chart_df["Low"] = pd.to_numeric(

        chart_df["Low"]

    )

    chart_df["Close"] = pd.to_numeric(

        chart_df["Close"]

    )

    chart_df["Volume"] = pd.to_numeric(

        chart_df["Volume"]

    )

    # ==========================================
    # CHART STYLE
    # ==========================================

    style = mpf.make_mpf_style(

        base_mpf_style="charles",

        gridstyle=""

    )

    # ==========================================
    # FILE NAME
    # ==========================================

    file_name = "latest_chart.png"

    # ==========================================
    # GENERATE CHART
    # ==========================================

    mpf.plot(

        chart_df.tail(50),

        type="candle",

        style=style,

        volume=True,

        mav=(9, 21),

        title=f"{primary_pattern}",

        savefig=file_name

    )

    return file_name

