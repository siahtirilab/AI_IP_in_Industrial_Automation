import os
import mimetypes
import requests


def post_to_linkedin(text, image_path=None):
    access_token = ""
    author_urn = ""

    if not access_token or not author_urn:
        return False, "LinkedIn token/author_urn تنظیم نشده"

    headers_json = {
        "Authorization": f"Bearer {access_token}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }

    try:
        # =========================
        # فقط متن
        # =========================
        if not image_path or not os.path.exists(image_path):
            payload = {
                "author": author_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            resp = requests.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers=headers_json,
                json=payload,
                timeout=60
            )
            return resp.ok, resp.text

        # =========================
        # 1) register upload
        # =========================
        register_payload = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": author_urn,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }

        register_resp = requests.post(
            "https://api.linkedin.com/v2/assets?action=registerUpload",
            headers=headers_json,
            json=register_payload,
            timeout=60
        )

        if not register_resp.ok:
            return False, register_resp.text

        register_data = register_resp.json()

        upload_url = register_data["value"]["uploadMechanism"][
            "com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"
        ]["uploadUrl"]

        asset = register_data["value"]["asset"]

        # =========================
        # 2) upload image binary
        # =========================
        mime_type = mimetypes.guess_type(image_path)[0] or "application/octet-stream"

        with open(image_path, "rb") as f:
            upload_resp = requests.put(
                upload_url,
                data=f,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": mime_type
                },
                timeout=120
            )

        if upload_resp.status_code not in (200, 201):
            return False, upload_resp.text

        # =========================
        # 3) create post with image
        # =========================
        post_payload = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "IMAGE",
                    "media": [
                        {
                            "status": "READY",
                            "media": asset
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        post_resp = requests.post(
            "https://api.linkedin.com/v2/ugcPosts",
            headers=headers_json,
            json=post_payload,
            timeout=60
        )

        return post_resp.ok, post_resp.text

    except Exception as e:
        return False, str(e)