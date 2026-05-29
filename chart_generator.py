import mplfinance as mpf


def generate_chart(
    df,
    filename
):

    chart_data = df.tail(50)

    mpf.plot(
        chart_data,

        type='candle',

        mav=(9, 21),

        volume=True,

        style='yahoo',

        title='LIVE GOLD MARKET',

        savefig=filename
    )

    print(
        f"✅ Chart Saved: {filename}"
    )