import os
import requests


def post_to_telegram(text, image_path=None):
    token = ""
    chat_id = ""

    if not token or not chat_id:
        return False, "Telegram token/chat_id تنظیم نشده"

    try:
        if image_path and os.path.exists(image_path):
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            with open(image_path, "rb") as f:
                resp = requests.post(
                    url,
                    data={
                        "chat_id": chat_id,
                        "caption": text
                    },
                    files={"photo": f},
                    timeout=60
                )
        else:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            resp = requests.post(
                url,
                data={
                    "chat_id": chat_id,
                    "text": text
                },
                timeout=60
            )

        return resp.ok, resp.text

    except Exception as e:
        return False, str(e)