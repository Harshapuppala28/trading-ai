import os

from dotenv import load_dotenv

from slack_sdk import WebClient


# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()


# ==========================================
# SLACK CONFIG
# ==========================================

SLACK_BOT_TOKEN = os.getenv(
    "SLACK_BOT_TOKEN"
)

CHANNEL_NAME = "trading_alerts"


client = WebClient(
    token=SLACK_BOT_TOKEN
)


# ==========================================
# SEND CHART IMAGE
# ==========================================

def send_chart_to_slack(
    chart_path,
    message
):

    try:

        response = client.files_upload_v2(

            channel=CHANNEL_NAME,

            file=chart_path,

            initial_comment=message

        )

        print(
            "✅ Chart Sent To Slack"
        )

    except Exception as e:

        print(
            f"❌ Slack Chart Upload Error: {e}"
        )