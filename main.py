import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class BodyPartDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Body Part Detection App")

        self.video_source = 0  
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(root, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_browse = tk.Button(root, text="Browse", command=self.browse_video)
        self.btn_browse.pack(pady=10)

        self.btn_start = tk.Button(root, text="Start", command=self.start_detection)
        self.btn_start.pack(pady=10)

        self.btn_stop = tk.Button(root, text="Stop", command=self.stop_detection)
        self.btn_stop.pack(pady=10)

        self.delay = 10
        self.update()

        self.root.mainloop()

    def browse_video(self):
        self.video_source = filedialog.askopenfilename()
        self.vid = cv2.VideoCapture(self.video_source)

    def start_detection(self):
        self.vid = cv2.VideoCapture(self.video_source)
        self.update()

    def stop_detection(self):
        self.vid.release()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = self.detect_body_parts(frame)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.root.after(self.delay, self.update)
        else:
            self.vid.release()

    def detect_body_parts(self, frame):
        # Use OpenPose or other body part detection logic here
        # This example will draw a wider and larger circle around the head and write "Head" as text

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            center = (int(x + w / 2), int(y + h / 2))
            radius = 70  # Increase the radius to make the circle larger
            cv2.circle(frame, center, radius, (255, 0, 0), 2)

            # Write "Head" as text
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text = "Head"
            text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
            text_position = (center[0] - text_size[0] // 2, center[1] - radius - 10)
            cv2.putText(frame, text, text_position, font, font_scale, (255, 0, 0), font_thickness, cv2.LINE_AA)

        return frame

if __name__ == "__main__":
    root = tk.Tk()
    app = BodyPartDetectionApp(root)
