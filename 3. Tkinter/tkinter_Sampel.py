import tkinter as tk
from tkinter import messagebox


def check_age():
    age = int(entry.get())

    if age > 18:
        result_label.config(text="You are old enough to go ahead!")
    elif age == 18:
        result_label.config(text="You are okay to go ahead!")
    else:
        result_label.config(text="You are young to go ahead!")



# ساخت پنجره اصلی
root = tk.Tk()
root.title("Age Checker Poweren")
root.geometry("750x200")

# لیبل
label = tk.Label(root, text="What is your age dud?")
label.pack(pady=10)

# اینپوت
entry = tk.Entry(root)
entry.pack(pady=5)

# دکمه
button = tk.Button(root, text="Check age", command=check_age)
button.pack(pady=10)

# نمایش نتیجه
result_label = tk.Label(root, text="")
result_label.pack(pady=10)

# اجرای برنامه
root.mainloop()