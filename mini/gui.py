import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os
import sys

# ----------------------------
# 🌟 Global Config
# ----------------------------
image_source = "D://mini//bg1.png"  # Your background image path
tutorial_image = "D://mini//handsign.png"  # Path to gesture tutorial image
gesture_process = None

# ----------------------------
# 🎥 Launch Gesture Window
# ----------------------------
def open_gesture_window():
    global gesture_process
    if gesture_process and gesture_process.poll() is None:
        gesture_process.terminate()
    try:
        python_interpreter = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")
        gesture_process = subprocess.Popen([python_interpreter, "test.py"])
    except Exception as e:
        print(f"Error: {e}")

# ----------------------------
# 🚦 Close Gesture Window
# ----------------------------
def close_gesture_window():
    global gesture_process
    if gesture_process and gesture_process.poll() is None:
        gesture_process.terminate()
        gesture_process = None

# ----------------------------
# 📍 Open About Page
# ----------------------------
def open_about_page():
    subprocess.Popen([sys.executable, "about.py"])

# ----------------------------
# 📖 Open Tutorials Page
# ----------------------------
def open_tutorial_page():
    tut_window = tk.Toplevel()
    tut_window.title("Gesture Images")
    tut_window.geometry("1000x700")
    tut_window.configure(bg="#0B0F2B")

    try:
        img = Image.open(tutorial_image)
        img = img.resize((950, 650), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        label = tk.Label(tut_window, image=img_tk, bg="#0B0F2B")
        label.image = img_tk
        label.pack(pady=20)
    except Exception as e:
        label = tk.Label(tut_window, text="Unable to load tutorial image.",
                         font=("Helvetica", 16), fg="white", bg="#0B0F2B")
        label.pack(pady=20)
        print("Tutorial image not loaded:", e)

# ----------------------------
# 🎨 Main GUI
# ----------------------------
def main():
    global root
    root = tk.Tk()
    root.title("The Pearl Project - Hand Gesture Recognition")
    root.state('zoomed')
    root.configure(bg='black')

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Load background image
    try:
        bg_img = Image.open(image_source)
        bg_img = bg_img.resize((screen_width, screen_height), Image.LANCZOS)
        bg_img_tk = ImageTk.PhotoImage(bg_img)
    except Exception as e:
        print("Background image not loaded:", e)
        bg_img_tk = None

    # Canvas for background
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    if bg_img_tk:
        canvas.create_image(0, 0, anchor=tk.NW, image=bg_img_tk)

    # Navigation Bar
    nav_bar = tk.Frame(root, bg="#0B0F2B", height=80)
    nav_bar.place(relx=0, rely=0, relwidth=1)

    logo = tk.Label(nav_bar, text="Pearl", font=("Helvetica", 28, "bold"), fg="white", bg="#0B0F2B")
    logo.pack(side=tk.LEFT, padx=30)

    menu_items = {
        "Home": None,
        "About": open_about_page,
        "Tutorials": open_tutorial_page,
    }

    for item, cmd in reversed(menu_items.items()):
        btn = tk.Button(nav_bar, text=item, font=("Helvetica", 20, "bold"), fg="white", bg="#0B0F2B",
                        bd=0, activebackground="#1C1F38", activeforeground="white", cursor="hand2",
                        command=cmd if cmd else lambda: None)
        btn.pack(side=tk.RIGHT, padx=12)

    # Start Button
    def on_hover(e):
        start_btn.config(bg="#FFAF88")

    def on_leave(e):
        start_btn.config(bg="#F5A46B")

    start_btn = tk.Button(root, text="Start", font=("Helvetica", 14, "bold"),
                          fg="black", bg="#F5A46B", padx=20, pady=10, bd=0,
                          relief="flat", command=open_gesture_window, cursor="hand2")
    start_btn.place(relx=0.5, rely=0.55, anchor="center")
    start_btn.bind("<Enter>", on_hover)
    start_btn.bind("<Leave>", on_leave)

    def on_close():
        close_gesture_window()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    main()