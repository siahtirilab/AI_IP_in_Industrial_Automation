import os
from flask import Flask, request, jsonify, render_template_string, redirect, session, url_for
from werkzeug.utils import secure_filename

from telegram_poster import post_to_telegram
from bale_poster import post_to_bale
from linkedin_poster import post_to_linkedin
from threads_poster import post_to_threads
import json

def shorten_text(text, max_len=280):
    text = str(text).replace("\n", " ").strip()
    if len(text) <= max_len:
        return text
    return text[:max_len] + " ..."


def format_platform_message(name, ok, msg):
    raw = str(msg)

    try:
        data = json.loads(raw.replace("'", '"'))
    except Exception:
        data = None

    if name == "telegram":
        if ok:
            return "ارسال به تلگرام با موفقیت انجام شد."
        return shorten_text(raw)

    if name == "bale":
        if ok:
            return "ارسال به بله با موفقیت انجام شد."
        return shorten_text(raw)

    if name == "threads":
        if ok:
            return "ارسال به تردز با موفقیت انجام شد."
        return shorten_text(raw)

    if name == "linkedin":
        if ok:
            return "ارسال به لینکدین با موفقیت انجام شد."
        return shorten_text(raw)

    return shorten_text(raw)




app = Flask(__name__)
app.secret_key = "CHANGE_THIS_SECRET_KEY"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

USERNAME = "admin"
PASSWORD = "admin"

LOGIN_HTML = """
<!doctype html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>ورود</title>
  <style>
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family:tahoma, Arial, sans-serif;
      background:linear-gradient(135deg,#0f172a,#1e293b);
      min-height:100vh;
      display:flex;
      align-items:center;
      justify-content:center;
      color:#fff;
    }
    .card{
      width:100%;
      max-width:380px;
      background:rgba(255,255,255,.08);
      backdrop-filter:blur(10px);
      border:1px solid rgba(255,255,255,.08);
      border-radius:18px;
      padding:28px;
      box-shadow:0 20px 60px rgba(0,0,0,.35);
    }
    h1{
      margin:0 0 8px;
      font-size:24px;
    }
    .sub{
      color:#cbd5e1;
      font-size:13px;
      margin-bottom:20px;
    }
    .field{
      margin-bottom:14px;
    }
    input{
      width:100%;
      padding:13px 14px;
      border:none;
      border-radius:12px;
      outline:none;
      background:#f8fafc;
      font-size:14px;
    }
    button{
      width:100%;
      border:none;
      border-radius:12px;
      padding:13px;
      cursor:pointer;
      font-size:15px;
      background:#22c55e;
      color:#fff;
      font-weight:bold;
    }
    .err{
      background:#7f1d1d;
      color:#fecaca;
      padding:10px 12px;
      border-radius:10px;
      margin-bottom:14px;
      font-size:13px;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>ورود به داشبورد</h1>
    <div class="sub">برای مدیریت انتشار محتوا وارد شوید</div>
    {% if error %}
      <div class="err">{{ error }}</div>
    {% endif %}
    <form method="post">
      <div class="field">
        <input name="username" placeholder="نام کاربری" autocomplete="username">
      </div>
      <div class="field">
        <input name="password" type="password" placeholder="رمز عبور" autocomplete="current-password">
      </div>
      <button type="submit">ورود</button>
    </form>
  </div>
</body>
</html>
"""

DASHBOARD_HTML = """
<!doctype html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Social Dashboard</title>
  <style>
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family:tahoma, Arial, sans-serif;
      background:#0f172a;
      color:#e2e8f0;
    }
    .wrap{
      max-width:980px;
      margin:30px auto;
      padding:0 16px;
    }
    .topbar{
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:16px;
      margin-bottom:20px;
      flex-wrap:wrap;
    }
    .title{
      font-size:28px;
      font-weight:bold;
      color:#fff;
    }
    .subtitle{
      font-size:13px;
      color:#94a3b8;
      margin-top:6px;
    }
    .logout{
      text-decoration:none;
      color:#fff;
      background:#ef4444;
      padding:10px 14px;
      border-radius:12px;
      font-size:14px;
    }
    .grid{
      display:grid;
      grid-template-columns:1.2fr .8fr;
      gap:18px;
    }
    .card{
      background:#1e293b;
      border:1px solid rgba(255,255,255,.06);
      border-radius:20px;
      padding:18px;
      box-shadow:0 12px 30px rgba(0,0,0,.18);
    }
    .card h2{
      margin:0 0 14px;
      font-size:18px;
      color:#fff;
    }
    textarea{
      width:100%;
      min-height:210px;
      resize:vertical;
      border:none;
      outline:none;
      border-radius:16px;
      padding:16px;
      font-size:14px;
      line-height:1.8;
      background:#0f172a;
      color:#f8fafc;
    }
    textarea::placeholder{
      color:#64748b;
    }
    .meta{
      margin-top:10px;
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:10px;
      flex-wrap:wrap;
      font-size:12px;
      color:#94a3b8;
    }
    .upload-box{
      margin-top:14px;
      border:2px dashed #334155;
      border-radius:18px;
      padding:16px;
      text-align:center;
      background:#0f172a;
      transition:.2s;
    }
    .upload-box.dragover{
      border-color:#22c55e;
      background:#132238;
    }
    .upload-box input[type=file]{
      display:none;
    }
    .upload-btn{
      display:inline-block;
      background:#334155;
      color:#fff;
      padding:10px 14px;
      border-radius:12px;
      cursor:pointer;
      font-size:14px;
    }
    .preview-wrap{
      margin-top:14px;
      display:none;
    }
    .preview-wrap.show{
      display:block;
    }
    .preview-wrap img{
      max-width:100%;
      max-height:260px;
      border-radius:16px;
      display:block;
      margin-top:10px;
      border:1px solid rgba(255,255,255,.08);
    }
    .preview-name{
      font-size:12px;
      color:#cbd5e1;
      margin-top:8px;
      word-break:break-all;
    }
    .checks{
      display:grid;
      grid-template-columns:repeat(2,minmax(0,1fr));
      gap:10px;
      margin-top:8px;
    }
    .check{
      background:#0f172a;
      padding:12px;
      border-radius:14px;
      border:1px solid rgba(255,255,255,.06);
      display:flex;
      align-items:center;
      gap:10px;
    }
    .check input{
      width:18px;
      height:18px;
    }
    .actions{
      margin-top:16px;
      display:flex;
      gap:10px;
      flex-wrap:wrap;
    }
    .btn{
      border:none;
      border-radius:14px;
      padding:12px 18px;
      cursor:pointer;
      font-size:14px;
      font-weight:bold;
    }
    .btn-send{
      background:#22c55e;
      color:#fff;
    }
    .btn-reset{
      background:#334155;
      color:#fff;
    }
    .status{
      margin-top:12px;
      font-size:13px;
      color:#93c5fd;
      min-height:20px;
    }
    .logbox{
      background:#020617;
      border-radius:16px;
      padding:14px;
      min-height:460px;
      white-space:pre-wrap;
      line-height:1.8;
      font-size:13px;
      color:#d1fae5;
      overflow:auto;
    }
    .small{
      font-size:12px;
      color:#94a3b8;
      margin-bottom:12px;
    }
    .badge{
      display:inline-block;
      font-size:11px;
      padding:4px 8px;
      border-radius:999px;
      background:#0f172a;
      color:#cbd5e1;
      margin-left:6px;
    }
    .footer-note{
      margin-top:10px;
      font-size:12px;
      color:#64748b;
    }
    @media (max-width: 860px){
      .grid{
        grid-template-columns:1fr;
      }
      .logbox{
        min-height:240px;
      }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="topbar">
      <div>
        <div class="title">داشبورد انتشار محتوا</div>
        <div class="subtitle">ارسال هم‌زمان به تلگرام، بله، لینکدین و تردز</div>
      </div>
      <a class="logout" href="/logout">خروج</a>
    </div>

    <div class="grid">
      <div class="card">
        <h2>محتوا</h2>
        <form id="publishForm">
          <textarea id="text" name="text" placeholder="متن پست را اینجا بنویس..."></textarea>

          <div class="meta">
            <div>تعداد کاراکتر: <span id="charCount">0</span></div>
            <div>برای لینکدین بهتر است متن خیلی بلند نشود</div>
          </div>

          <div class="upload-box" id="dropZone">
            <label class="upload-btn" for="image">انتخاب عکس</label>
            <input type="file" id="image" name="image" accept="image/*">
            <div class="footer-note">یا فایل را بکش و اینجا رها کن</div>

            <div class="preview-wrap" id="previewWrap">
              <div class="preview-name" id="previewName"></div>
              <img id="previewImage" src="" alt="preview">
            </div>
          </div>

          <h2 style="margin-top:18px">پلتفرم‌ها</h2>
          <div class="checks">
            <label class="check"><input type="checkbox" name="platforms" value="telegram" checked> تلگرام</label>
            <label class="check"><input type="checkbox" name="platforms" value="bale" checked> بله</label>
            <label class="check"><input type="checkbox" name="platforms" value="linkedin" checked> لینکدین</label>
            <label class="check"><input type="checkbox" name="platforms" value="threads" checked> تردز</label>
          </div>

          <div class="actions">
            <button class="btn btn-send" type="submit" id="sendBtn">ارسال</button>
            <button class="btn btn-reset" type="button" id="clearBtn">پاک کردن</button>
          </div>

          <div class="status" id="statusText"></div>
        </form>
      </div>

      <div class="card">
        <h2>لاگ اجرا <span class="badge">زنده</span></h2>
        <div class="small">وضعیت هر پلتفرم اینجا نمایش داده می‌شود</div>
        <div class="logbox" id="logBox">آماده ارسال...</div>
      </div>
    </div>
  </div>

  <script>
    const textEl = document.getElementById("text");
    const charCount = document.getElementById("charCount");
    const imageInput = document.getElementById("image");
    const previewWrap = document.getElementById("previewWrap");
    const previewImage = document.getElementById("previewImage");
    const previewName = document.getElementById("previewName");
    const dropZone = document.getElementById("dropZone");
    const form = document.getElementById("publishForm");
    const logBox = document.getElementById("logBox");
    const statusText = document.getElementById("statusText");
    const sendBtn = document.getElementById("sendBtn");
    const clearBtn = document.getElementById("clearBtn");

    function updateCharCount() {
      charCount.textContent = textEl.value.length;
    }

    function showPreview(file) {
      if (!file) {
        previewWrap.classList.remove("show");
        previewImage.src = "";
        previewName.textContent = "";
        return;
      }

      previewName.textContent = file.name;
      const reader = new FileReader();
      reader.onload = function(e) {
        previewImage.src = e.target.result;
        previewWrap.classList.add("show");
      };
      reader.readAsDataURL(file);
    }

    textEl.addEventListener("input", updateCharCount);

    imageInput.addEventListener("change", function() {
      const file = this.files[0];
      showPreview(file);
    });

    ["dragenter", "dragover"].forEach(evt => {
      dropZone.addEventListener(evt, function(e){
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add("dragover");
      });
    });

    ["dragleave", "drop"].forEach(evt => {
      dropZone.addEventListener(evt, function(e){
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove("dragover");
      });
    });

    dropZone.addEventListener("drop", function(e){
      const files = e.dataTransfer.files;
      if (files && files.length > 0) {
        imageInput.files = files;
        showPreview(files[0]);
      }
    });

    clearBtn.addEventListener("click", function(){
      form.reset();
      updateCharCount();
      showPreview(null);
      logBox.textContent = "فرم پاک شد.";
      statusText.textContent = "";
    });

    form.addEventListener("submit", async function(e){
      e.preventDefault();

      const text = textEl.value.trim();
      if (!text) {
        statusText.textContent = "متن پست خالی است.";
        return;
      }

      const checked = document.querySelectorAll('input[name="platforms"]:checked');
      if (checked.length === 0) {
        statusText.textContent = "حداقل یک پلتفرم را انتخاب کن.";
        return;
      }

      const fd = new FormData(form);

      sendBtn.disabled = true;
      sendBtn.textContent = "در حال ارسال...";
      statusText.textContent = "در حال ارسال به پلتفرم‌های انتخاب‌شده...";
      logBox.textContent = "شروع ارسال...";

      try {
        const res = await fetch("/publish", {
          method: "POST",
          body: fd
        });

        const data = await res.json();

        if (!res.ok) {
          logBox.textContent = data.error || "خطا در ارسال";
          statusText.textContent = "ارسال ناموفق بود.";
          sendBtn.disabled = false;
          sendBtn.textContent = "ارسال";
          return;
        }

        let out = "";
        if (data.results) {
          for (const [name, info] of Object.entries(data.results)) {
            out += "========== " + name.toUpperCase() + " ==========" + "\\n";
            out += "STATUS: " + (info.ok ? "OK" : "ERROR") + "\\n";
            out += (info.msg || "") + "\\n\\n";
          }
        } else {
          out = "پاسخ معتبری دریافت نشد.";
        }

        logBox.textContent = out;
        statusText.textContent = "ارسال تمام شد.";
      } catch (err) {
        logBox.textContent = "خطای ارتباط با سرور:\\n" + err;
        statusText.textContent = "ارسال انجام نشد.";
      }

      sendBtn.disabled = false;
      sendBtn.textContent = "ارسال";
    });

    updateCharCount();
  </script>
</body>
</html>
"""


def is_logged_in():
    return session.get("login") is True


@app.route("/login", methods=["GET", "POST"])
def login():
    if is_logged_in():
        return redirect(url_for("index"))

    error = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == USERNAME and password == PASSWORD:
            session["login"] = True
            return redirect(url_for("index"))
        error = "نام کاربری یا رمز عبور اشتباه است."

    return render_template_string(LOGIN_HTML, error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/", methods=["GET"])
def index():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template_string(DASHBOARD_HTML)


@app.route("/publish", methods=["POST"])
def publish():
    if not is_logged_in():
        return jsonify({"ok": False, "error": "Unauthorized"}), 401

    text = request.form.get("text", "").strip()
    selected = request.form.getlist("platforms")

    if not text:
        return jsonify({"ok": False, "error": "متن خالی است"}), 400

    if not selected:
        return jsonify({"ok": False, "error": "هیچ پلتفرمی انتخاب نشده"}), 400

    image = request.files.get("image")
    image_path = None

    if image and image.filename:
        filename = secure_filename(image.filename)
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image.save(image_path)

    results = {}

    def run_platform(name, func):
        try:
            ok, msg = func(text, image_path)
            results[name] = {
                "ok": ok,
                "msg": format_platform_message(name, ok, msg)
            }
        except Exception as e:
            results[name] = {
                "ok": False,
                "msg": shorten_text(str(e))
            }

    if "telegram" in selected:
        run_platform("telegram", post_to_telegram)

    if "bale" in selected:
        run_platform("bale", post_to_bale)

    if "linkedin" in selected:
        run_platform("linkedin", post_to_linkedin)

    if "threads" in selected:
        run_platform("threads", post_to_threads)

    return jsonify({
        "ok": True,
        "results": results
    })


if __name__ == "__main__":
    app.run(debug=True)