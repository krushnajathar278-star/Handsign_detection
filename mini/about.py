import tkinter as tk
from PIL import Image, ImageTk

def about_window():
    window = tk.Tk()
    window.title("About Us - Pearl Studio")
    window.geometry("1200x700")
    window.configure(bg="#0B0F2B")

    # -------------------------------
    # Left Image Panel
    # -------------------------------
    left_frame = tk.Frame(window, bg="#FFAF88", width=550, height=700)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    # Load and place image
    try:
        image_path = "D:/mini/about.jpg"  # Replace with your image name if different
        img = Image.open(image_path)
        img = img.resize((400, 500), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        img_label = tk.Label(left_frame, image=img_tk, bg="#FFAF88")
        img_label.image = img_tk
        img_label.pack(fill=tk.BOTH, expand=True)
    except Exception as e:
        print("Image not loaded:", e)

    # -------------------------------
    # Right Text Panel
    # -------------------------------
    right_frame = tk.Frame(window, bg="#0B0F2B")
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=40, pady=40)

    heading = tk.Label(right_frame, text="About us", font=("Helvetica", 12, "bold"),
                       bg="#0B0F2B", fg="#FFAF88", anchor="w")
    heading.pack(anchor="w")

    title = tk.Label(right_frame, text="About Pearl",
                     font=("Helvetica", 28, "bold"), bg="#0B0F2B", fg="white", justify="left")
    title.pack(anchor="w", pady=(10, 20))

    description = (
        "The Pearl Project is an intelligent and interactive Hand Sign Detection and Recognition System developed, "
        "using cutting-edge computer vision and deep learning technologies. It is designed to interpret American "
        "Sign Language (ASL) gestures in real-time using a webcam, allowing seamless communication between "
        "individuals with hearing or speech impairments and the digital world.\n\n"
        "At the heart of this system is a custom-trained deep learning model built with TensorFlow and Keras, "
        "supported by OpenCV for real-time video capture and hand tracking using cvzone’s HandTrackingModule."
        "The system is capable of recognizing and classifying hand gestures representing the English alphabets with"
        "high accuracy."
    )

    content = tk.Label(right_frame, text=description, font=("Helvetica", 12),
                       bg="#0B0F2B", fg="#AAB7C4", justify="left", wraplength=550)
    content.pack(anchor="w")

    window.mainloop()

if __name__ == "__main__":
    about_window()
