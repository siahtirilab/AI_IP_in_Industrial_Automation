import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox


def select_folder():
    folder = filedialog.askdirectory()
    path_var.set(folder)


def calculate_videos():
    path = path_var.get()

    if not path:
        messagebox.showerror("Error", "Please select a folder first!")
        return

    mp4_files = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.mp4'):
                mp4_files.append(os.path.join(root, file))

    result_text.delete(1.0, tk.END)

    total_hours = 0.0

    if not mp4_files:
        result_text.insert(tk.END, "No MP4 files found.\n")
        return

    for file in mp4_files:
        cap = cv2.VideoCapture(file)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        if fps == 0:
            continue

        duration = frames / fps
        hours = duration / 3600.0
        total_hours += hours

        result_text.insert(tk.END, f"{os.path.basename(file)} → {hours:.2f} hours\n")

        cap.release()

    result_text.insert(tk.END, "\n-------------------------\n")
    result_text.insert(tk.END, f"Total time: {total_hours:.2f} hours\n")
    result_text.insert(tk.END, f"Total videos: {len(mp4_files)}\n")


# UI
root = tk.Tk()
root.title("Video Duration Calculator")
root.geometry("600x400")

path_var = tk.StringVar()

# انتخاب مسیر
frame_top = tk.Frame(root)
frame_top.pack(pady=10)

entry = tk.Entry(frame_top, textvariable=path_var, width=50)
entry.pack(side=tk.LEFT, padx=5)

btn_browse = tk.Button(frame_top, text="Browse", command=select_folder)
btn_browse.pack(side=tk.LEFT)

# دکمه محاسبه
btn_calc = tk.Button(root, text="Calculate", command=calculate_videos, bg="green", fg="white")
btn_calc.pack(pady=10)

# نمایش نتایج
result_text = tk.Text(root, wrap=tk.WORD)
result_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

root.mainloop()