import os

from dotenv import load_dotenv

from slack_sdk import WebClient

from slack_sdk.errors import SlackApiError


load_dotenv()


SLACK_BOT_TOKEN = os.getenv(
    "SLACK_BOT_TOKEN"
)

CHANNEL_ID = "trading_alerts"


client = WebClient(
    token=SLACK_BOT_TOKEN
)


def send_slack_message(message):

    try:

        client.chat_postMessage(
            channel=CHANNEL_ID,
            text=message
        )

        print("✅ SLACK ALERT SENT")

    except SlackApiError as e:

        print(
            f"❌ Slack Error: "
            f"{e.response['error']}"
        )


def send_slack_image(
    message,
    image_path
):

    try:

        client.files_upload_v2(

            channel=CHANNEL_ID,

            file=image_path,

            title="Trading Setup Chart",

            initial_comment=message
        )

        print(
            "✅ SLACK IMAGE ALERT SENT"
        )

    except SlackApiError as e:

        print(
            f"❌ Slack Upload Error: "
            f"{e.response['error']}"
        )