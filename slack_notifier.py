import os
import requests

# ==========================================
# SEND TEXT MESSAGE
# ==========================================

def send_slack_message(
    webhook_url,
    message
):
    response = requests.post(
        webhook_url,
        json={
            "text": message
        }
    )

    print(
        f"📨 Slack Status Code: {response.status_code}"
    )

    print(
        f"📨 Slack Response: {response.text}"
    )


# ==========================================
# SEND IMAGE USING HARDCODED CHANNEL ID
# ==========================================

def send_slack_image(
    bot_token,
    image_path
):
    # 💥 PASTE YOUR ACTUAL CHANNEL ID HERE (e.g., "C07B66UASAG")
    CHANNEL_ID = "C0B6Q7W2KFB"
    
    headers = {"Authorization": f"Bearer {bot_token}"}

    # ------------------------------------------
    # STEP 1: GET EXTERNAL UPLOAD URL
    # ------------------------------------------
    file_size = os.path.getsize(image_path)
    file_name = os.path.basename(image_path)

    url_alloc_api = "https://slack.com/api/files.getUploadURLExternal"
    alloc_payload = {
        "filename": file_name,
        "length": file_size
    }

    alloc_res = requests.get(url_alloc_api, headers=headers, params=alloc_payload).json()

    if not alloc_res.get("ok"):
        print(f"❌ Failed to get upload URL: {alloc_res.get('error')}")
        return

    upload_url = alloc_res.get("upload_url")
    file_id = alloc_res.get("file_id")

    # ------------------------------------------
    # STEP 2: UPLOAD BINARY TO SLACK STORAGE
    # ------------------------------------------
    with open(image_path, "rb") as image_file:
        upload_res = requests.post(upload_url, files={"file": image_file})

    if upload_res.status_code != 200:
        print(f"❌ Storage host upload failed with code: {upload_res.status_code}")
        return

    # ------------------------------------------
    # STEP 3: SHARE UPLOADED FILE TO CHANNEL
    # ------------------------------------------
    url_complete_api = "https://slack.com/api/files.completeUploadExternal"
    complete_payload = {
        "files": f"[{{'id': '{file_id}', 'title': 'Trading Chart'}}]",
        "channel_id": CHANNEL_ID,
        "initial_comment": "📸 Trading Pattern Chart"
    }

    final_res = requests.post(url_complete_api, headers=headers, data=complete_payload)

    print(
        f"📸 Image Upload Status: {final_res.status_code}"
    )

    print(
        f"📸 Image Upload Response: {final_res.text}"
    )