import os

from dotenv import load_dotenv

import requests


# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# GET WEBHOOK FROM .env
# ==========================================

WEBHOOK_URL = os.getenv(
    "SLACK_WEBHOOK_URL"
)


# ==========================================
# SEND CHART MESSAGE
# ==========================================

def send_slack_chart_message(
    message,
    image_url=None
):

    payload = {
        "text": message
    }

    if image_url:

        payload["attachments"] = [
            {
                "image_url": image_url,
                "text": "Market Chart"
            }
        ]

    response = requests.post(
        WEBHOOK_URL,
        json=payload
    )

    if response.status_code == 200:

        print(
            "✅ SLACK IMAGE ALERT SENT"
        )

    else:

        print(
            "❌ FAILED TO SEND SLACK IMAGE"
        )