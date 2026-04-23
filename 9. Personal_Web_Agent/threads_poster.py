import os
import json
import time
import requests

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, "threads_token.json")

# =========================
# THREADS CONFIG
# =========================
THREADS_USER_ID = ""
THREADS_SHORT_LIVED_TOKEN = ""
THREADS_APP_SECRET = ""

# =========================
# CLOUDINARY CONFIG
# =========================
CLOUDINARY_CLOUD_NAME = ""
CLOUDINARY_UPLOAD_PRESET = ""

# =========================
# SETTINGS
# =========================
REFRESH_BEFORE_EXPIRY_SECONDS = 7 * 24 * 60 * 60


def save_token_data(token_data: dict):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, ensure_ascii=False, indent=2)


def load_token_data():
    if not os.path.exists(TOKEN_FILE):
        return None

    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def exchange_short_lived_to_long_lived():
    if not THREADS_SHORT_LIVED_TOKEN.strip():
        return False, "SHORT_LIVED_TOKEN خالی است"

    if not THREADS_APP_SECRET.strip():
        return False, "THREADS_APP_SECRET خالی است"

    try:
        resp = requests.get(
            "https://graph.threads.net/access_token",
            params={
                "grant_type": "th_exchange_token",
                "client_secret": THREADS_APP_SECRET,
                "access_token": THREADS_SHORT_LIVED_TOKEN.strip(),
            },
            timeout=60
        )

        data = resp.json()
        access_token = data.get("access_token")
        expires_in = int(data.get("expires_in", 0))

        if not access_token:
            return False, f"Exchange failed: {data}"

        token_data = {
            "access_token": access_token,
            "token_type": data.get("token_type", "bearer"),
            "expires_in": expires_in,
            "issued_at": int(time.time()),
            "expires_at": int(time.time()) + expires_in
        }

        save_token_data(token_data)
        return True, token_data

    except Exception as e:
        return False, str(e)


def refresh_long_lived_token(current_token: str):
    try:
        resp = requests.get(
            "https://graph.threads.net/refresh_access_token",
            params={
                "grant_type": "th_refresh_token",
                "access_token": current_token,
            },
            timeout=60
        )

        data = resp.json()
        access_token = data.get("access_token")
        expires_in = int(data.get("expires_in", 0))

        if not access_token:
            return False, f"Refresh failed: {data}"

        token_data = {
            "access_token": access_token,
            "token_type": data.get("token_type", "bearer"),
            "expires_in": expires_in,
            "issued_at": int(time.time()),
            "expires_at": int(time.time()) + expires_in
        }

        save_token_data(token_data)
        return True, token_data

    except Exception as e:
        return False, str(e)


def get_valid_threads_token():
    now = int(time.time())
    token_data = load_token_data()

    if not token_data:
        ok, result = exchange_short_lived_to_long_lived()
        if not ok:
            return False, f"Initial exchange failed: {result}"
        return True, result["access_token"]

    access_token = token_data.get("access_token", "").strip()
    issued_at = int(token_data.get("issued_at", 0))
    expires_at = int(token_data.get("expires_at", 0))

    if not access_token or not expires_at:
        ok, result = exchange_short_lived_to_long_lived()
        if not ok:
            return False, f"Re-exchange failed: {result}"
        return True, result["access_token"]

    if now >= expires_at:
        ok, result = exchange_short_lived_to_long_lived()
        if not ok:
            return False, f"Token expired and re-exchange failed: {result}"
        return True, result["access_token"]

    age_seconds = now - issued_at
    time_left = expires_at - now

    if age_seconds >= 24 * 60 * 60 and time_left <= REFRESH_BEFORE_EXPIRY_SECONDS:
        ok, result = refresh_long_lived_token(access_token)
        if ok:
            return True, result["access_token"]
        return True, access_token

    return True, access_token


def upload_to_cloudinary(image_path):
    if not CLOUDINARY_CLOUD_NAME.strip() or not CLOUDINARY_UPLOAD_PRESET.strip():
        return False, "Cloudinary تنظیم نشده"

    if not image_path or not os.path.exists(image_path):
        return False, "فایل عکس پیدا نشد"

    try:
        with open(image_path, "rb") as f:
            resp = requests.post(
                f"https://api.cloudinary.com/v1_1/{CLOUDINARY_CLOUD_NAME}/image/upload",
                data={"upload_preset": CLOUDINARY_UPLOAD_PRESET},
                files={"file": f},
                timeout=60
            )

        data = resp.json()
        secure_url = data.get("secure_url")

        if secure_url:
            return True, secure_url

        return False, str(data)

    except Exception as e:
        return False, str(e)


def post_to_threads(text, image_path=None):
    user_id = THREADS_USER_ID.strip()

    if not user_id:
        return False, "THREADS_USER_ID تنظیم نشده"

    ok, token_result = get_valid_threads_token()
    if not ok:
        return False, token_result

    access_token = token_result.strip()

    try:
        image_url = None

        if image_path:
            ok, result = upload_to_cloudinary(image_path)
            if not ok:
                return False, f"Cloudinary upload failed: {result}"
            image_url = result

        create_url = f"https://graph.threads.net/v1.0/{user_id}/threads"

        # پست متنی
        if not image_url:
            data = {
                "media_type": "TEXT",
                "text": text,
                "auto_publish_text": "true",
                "access_token": access_token
            }

            resp = requests.post(create_url, data=data, timeout=60)

            try:
                create_data = resp.json()
            except Exception:
                create_data = {"raw": resp.text}

            if resp.ok:
                return True, str(create_data)
            return False, str(create_data)

        # پست تصویری
        data = {
            "media_type": "IMAGE",
            "image_url": image_url,
            "text": text,
            "access_token": access_token
        }

        resp = requests.post(create_url, data=data, timeout=60)

        try:
            create_data = resp.json()
        except Exception:
            create_data = {"raw": resp.text}

        creation_id = create_data.get("id")
        if not creation_id:
            return False, str(create_data)

        publish_url = f"https://graph.threads.net/v1.0/{user_id}/threads_publish"

        last_error = None

        for _ in range(4):
            time.sleep(3)

            publish_resp = requests.post(
                publish_url,
                data={
                    "creation_id": creation_id,
                    "access_token": access_token
                },
                timeout=60
            )

            try:
                publish_data = publish_resp.json()
            except Exception:
                publish_data = {"raw": publish_resp.text}

            if publish_resp.ok:
                return True, str(publish_data)

            last_error = publish_data

        return False, str(last_error)

    except Exception as e:
        return False, str(e)


if __name__ == "__main__":
    ok, msg = post_to_threads("تست مستقیم از سرور سی‌پنل")
    print("OK:", ok)
    print("MSG:", msg)