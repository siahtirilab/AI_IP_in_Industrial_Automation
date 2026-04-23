import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import yt_dlp

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_var.set(folder)


def download_video():
    url = url_entry.get().strip()
    path = path_var.get().strip()

    if not url:
        messagebox.showerror("Error", "URL رو وارد کن")
        return

    if not path:
        messagebox.showerror("Error", "مسیر ذخیره رو انتخاب کن")
        return

    if not os.path.isdir(path):
        messagebox.showerror("Error", "مسیر معتبر نیست")
        return

    status_label.configure(text="Wait... downloading ⏳")
    app.update_idletasks()

    try:
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        status_label.configure(text="Download finished ✅")

    except Exception as e:
        status_label.configure(text="Error ❌")
        messagebox.showerror("Error", str(e))


# UI
app = ctk.CTk()
app.title("YT Downloader")
app.geometry("600x320")

# URL
url_label = ctk.CTkLabel(app, text="Your Link")
url_label.pack(pady=(20, 5))

url_entry = ctk.CTkEntry(app, width=400)
url_entry.pack(pady=5)

url_entry.bind("<Control-c>", lambda e: url_entry.event_generate("<<Copy>>"))
url_entry.bind("<Control-v>", lambda e: url_entry.event_generate("<<Paste>>"))
url_entry.bind("<Control-x>", lambda e: url_entry.event_generate("<<Cut>>"))

url_entry.focus()

# Path
path_var = ctk.StringVar()

path_label = ctk.CTkLabel(app, text="Save to:")
path_label.pack(pady=(15, 5))

path_frame = ctk.CTkFrame(app)
path_frame.pack(pady=5)

path_entry = ctk.CTkEntry(path_frame, textvariable=path_var, width=300)
path_entry.pack(side="left", padx=5, pady=5)

path_entry.bind("<Control-c>", lambda e: path_entry.event_generate("<<Copy>>"))
path_entry.bind("<Control-v>", lambda e: path_entry.event_generate("<<Paste>>"))
path_entry.bind("<Control-x>", lambda e: path_entry.event_generate("<<Cut>>"))

browse_btn = ctk.CTkButton(path_frame, text="Browse", command=browse_folder)
browse_btn.pack(side="left", padx=5)

# Download Button
download_btn = ctk.CTkButton(app, text="Download", command=download_video)
download_btn.pack(pady=20)

# Status
status_label = ctk.CTkLabel(app, text="")
status_label.pack()

app.mainloop()