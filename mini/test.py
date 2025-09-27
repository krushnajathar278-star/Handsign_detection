import tkinter as tk
from PIL import Image, ImageTk
import threading
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import os
import cv2

# -------------------------------------------
# 🌟 Constants and Globals
# -------------------------------------------
running = True
offset = 20
imgSize = 300
labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M","N","O","P","Q","R","S","T","U","V","W","X","Y"]

detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")


# -------------------------------------------
# 🎥 Camera Loop
# -------------------------------------------
def camera_loop(cam_canvas, result_label):
    global running
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while running:
        success, img = cap.read()
        if not success:
            print("Webcam error.")
            break

        imgOutput = img.copy()
        hands, img = detector.findHands(img)

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
            x1, y1 = max(x - offset, 0), max(y - offset, 0)
            x2, y2 = min(x + w + offset, img.shape[1]), min(y + h + offset, img.shape[0])
            imgCrop = img[y1:y2, x1:x2]

            if imgCrop.size > 0:
                imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
                aspectRatio = h / w

                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize

                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                if 0 <= index < len(labels):
                    label = labels[index]
                    confidence = max(prediction) * 100
                    result_label.config(text=f"{label}\n{confidence:.2f}%", justify="center")

        img = cv2.cvtColor(imgOutput, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (640, 480))
        img_pil = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        cam_canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        cam_canvas.imgtk = img_tk

    cap.release()
    cv2.destroyAllWindows()


# -------------------------------------------
# 🖼️ GUI Layout (Based on your sketch)
# -------------------------------------------
def main():
    global running
    running = True

    window = tk.Tk()
    window.title("Hand Sign Gesture Recognition")
    window.geometry("1000x600")
    window.configure(bg="#2C3E50")  # Background: professional dark blue

    # ---------- Header ----------
    header = tk.Label(window, text="Hand Sign Gesture Recognition",
                      font=("Helvetica", 20, "bold"), fg="white", bg="#34495E", pady=10)
    header.pack(fill=tk.X)

    # ---------- Main Section ----------
    main_frame = tk.Frame(window, bg="#2C3E50")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Left: Webcam canvas
    cam_frame = tk.Frame(main_frame, bg="white", width=700, height=500)
    cam_frame.pack(side=tk.LEFT, padx=10, pady=10)
    cam_frame.pack_propagate(False)

    cam_canvas = tk.Canvas(cam_frame, width=640, height=480, bg="black")
    cam_canvas.pack()

    # Right: Gesture label + Close button
    right_panel = tk.Frame(main_frame, bg="#ECF0F1", width=300, height=500)
    right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
    right_panel.pack_propagate(False)

    # Gesture label
    result_label = tk.Label(right_panel, text="Gestures", font=("Helvetica", 18, "bold"),
                            fg="#2C3E50", bg="#ECF0F1")
    result_label.pack(pady=(100, 20), expand=True)

    # Close button
    def close_window():
        global running
        running = False
        window.destroy()

    close_btn = tk.Button(right_panel, text="Close", font=("Helvetica", 14, "bold"),
                          bg="#A9CCE3", fg="#154360", padx=20, pady=10,
                          relief="raised", bd=2, command=close_window, cursor="hand2")
    close_btn.pack(pady=(0, 50))

    # ---------- Start webcam in thread ----------
    threading.Thread(target=camera_loop, args=(cam_canvas, result_label), daemon=True).start()

    window.mainloop()


if __name__ == "__main__":
    main()
