import customtkinter as ctk
from tkinter import messagebox

# تنظیمات ظاهری
ctk.set_appearance_mode("dark")   # "light" هم میتونی بذاری
ctk.set_default_color_theme("blue")

def check_age():
    try:
        age = int(entry.get())

        if age > 18:
            result_label.configure(text="You are old enough to go ahead!")
        elif age == 18:
            result_label.configure(text="You are okay to go ahead!")
        else:
            result_label.configure(text="You are young to go ahead!")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number!")

# ساخت پنجره
root = ctk.CTk()
root.title("Age Checker")
root.geometry("400x300")

# عنوان
title_label = ctk.CTkLabel(root, text="Age Checker", font=("Arial", 22, "bold"))
title_label.pack(pady=20)

# ورودی
entry = ctk.CTkEntry(root, placeholder_text="Enter your age", width=200)
entry.pack(pady=10)

# دکمه
button = ctk.CTkButton(root, text="Check Age", command=check_age)
button.pack(pady=15)

# نتیجه
result_label = ctk.CTkLabel(root, text="", wraplength=300)
result_label.pack(pady=10)

# اجرا
root.mainloop()