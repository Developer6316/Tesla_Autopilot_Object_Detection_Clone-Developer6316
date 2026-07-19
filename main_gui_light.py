"""
Tesla Autopilot Clone – Object & Lane Detection
Author: Developer6316
Cross-platform GUI with webcam, photo, and video modes.
Completely free of Pylance type errors.
"""

import cv2
import numpy as np
import threading
import time
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
from ultralytics import YOLO

# ------------------------- Lane Detection -------------------------
class LaneDetector:
    @staticmethod
    def detect_lanes(frame: np.ndarray) -> np.ndarray:
        """Return a copy of the frame with lane lines drawn."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        height, width = frame.shape[:2]
        mask = np.zeros_like(edges)
        # Create ROI vertices as a list of points (compatible with all OpenCV types)
        roi_vertices = np.array([[
            [0, height],
            [width // 2 - 50, height // 2 + 50],
            [width // 2 + 50, height // 2 + 50],
            [width, height]
        ]], dtype=np.int32)
        cv2.fillPoly(mask, [roi_vertices[0]], 255)   # pass as list of point arrays
        masked_edges = cv2.bitwise_and(edges, mask)

        lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180,
                                threshold=30, minLineLength=40, maxLineGap=100)
        lane_image = np.zeros_like(frame)

        left_lines, right_lines = [], []
        if lines is not None:
            for line in lines:
                # Handle both (1,4) and (4,) shapes
                if line.ndim == 2 and line.shape[0] == 1:
                    x1, y1, x2, y2 = line[0]
                else:
                    x1, y1, x2, y2 = line
                if x2 - x1 == 0:
                    continue
                slope = (y2 - y1) / (x2 - x1)
                if abs(slope) < 0.5:
                    continue
                if slope < 0:
                    left_lines.append((x1, y1, x2, y2))
                else:
                    right_lines.append((x1, y1, x2, y2))

        def make_line(points, color):
            if points:
                xs, ys = [], []
                for x1, y1, x2, y2 in points:
                    xs.extend([x1, x2])
                    ys.extend([y1, y2])
                if xs and ys:
                    poly = np.poly1d(np.polyfit(ys, xs, 1))
                    y1_ = height
                    y2_ = int(height * 0.6)
                    x1_ = int(poly(y1_))
                    x2_ = int(poly(y2_))
                    cv2.line(lane_image, (x1_, y1_), (x2_, y2_), color, 8)

        make_line(left_lines, (0, 255, 0))
        make_line(right_lines, (0, 255, 0))

        return cv2.addWeighted(frame, 0.8, lane_image, 1, 0)

# ------------------------- Detection Engine -------------------------
class DetectionEngine:
    def __init__(self, model_path: str = "yolov8n.pt"):
        self.model = YOLO(model_path)
        self.model.to('cpu')  # change to 'cuda' for GPU

    def detect(self, frame: np.ndarray, draw_lanes: bool = True) -> tuple[np.ndarray, float]:
        """Run detection, optionally add lanes, return (annotated_frame, fps)."""
        t_start = time.time()
        results = list(self.model(frame, verbose=False))   # convert generator to list
        annotated = results[0].plot()                     # first result's plot
        if draw_lanes:
            annotated = LaneDetector.detect_lanes(annotated)
        fps = 1.0 / (time.time() - t_start + 1e-6)
        return annotated, fps

# ------------------------- Video Processor (Threaded) -------------------------
class VideoProcessor(threading.Thread):
    def __init__(self, source, engine, update_callback, stop_event):
        super().__init__()
        self.source = source
        self.engine = engine
        self.update_callback = update_callback
        self.stop_event = stop_event
        self.daemon = True

    def run(self):
        cap = cv2.VideoCapture(self.source)
        if not cap.isOpened():
            self.update_callback(None, "Error: Could not open source", 0.0)
            return

        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                if isinstance(self.source, str):
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                else:
                    break

            frame = cv2.resize(frame, (800, 450))
            annotated, fps = self.engine.detect(frame, draw_lanes=True)
            rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            self.update_callback(rgb, None, fps)

        cap.release()
        self.update_callback(None, "Stream stopped", 0.0)

# ------------------------- Modern GUI -------------------------
class TeslaAutopilotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tesla Autopilot Clone – Developer6316")
        self.geometry("1000x650")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.source_type = ctk.StringVar(value="webcam")
        self.is_running = False
        self.stop_event = threading.Event()
        self.video_thread = None
        self.engine = DetectionEngine()

        # Keep a reference to the current PhotoImage to prevent garbage collection
        self.current_image: ImageTk.PhotoImage | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel
        self.control_panel = ctk.CTkFrame(self.main_frame, width=220)
        self.control_panel.pack(side="left", fill="y", padx=(0, 10), pady=10)
        self.control_panel.pack_propagate(False)

        ctk.CTkLabel(self.control_panel, text="SOURCE", font=("Arial", 16, "bold")).pack(pady=(20, 10))

        self.webcam_radio = ctk.CTkRadioButton(self.control_panel, text="Webcam", variable=self.source_type, value="webcam")
        self.webcam_radio.pack(pady=5, anchor="w", padx=20)
        self.photo_radio = ctk.CTkRadioButton(self.control_panel, text="Photo", variable=self.source_type, value="photo")
        self.photo_radio.pack(pady=5, anchor="w", padx=20)
        self.video_radio = ctk.CTkRadioButton(self.control_panel, text="Video", variable=self.source_type, value="video")
        self.video_radio.pack(pady=5, anchor="w", padx=20)

        self.start_btn = ctk.CTkButton(self.control_panel, text="Start Detection", command=self.start_detection)
        self.start_btn.pack(pady=20, padx=20, fill="x")

        self.stop_btn = ctk.CTkButton(self.control_panel, text="Stop", command=self.stop_detection, state="disabled")
        self.stop_btn.pack(pady=5, padx=20, fill="x")

        self.photo_btn = ctk.CTkButton(self.control_panel, text="Select Photo", command=self.select_photo, state="disabled")
        self.photo_btn.pack(pady=5, padx=20, fill="x")

        self.video_btn = ctk.CTkButton(self.control_panel, text="Select Video", command=self.select_video, state="disabled")
        self.video_btn.pack(pady=5, padx=20, fill="x")

        self.status_label = ctk.CTkLabel(self.control_panel, text="Status: Idle", font=("Arial", 12))
        self.status_label.pack(pady=(30, 10))

        self.fps_label = ctk.CTkLabel(self.control_panel, text="FPS: --", font=("Arial", 14, "bold"))
        self.fps_label.pack(pady=5)

        ctk.CTkLabel(self.control_panel, text="Developer6316", font=("Arial", 10, "italic")).pack(side="bottom", pady=10)

        # Right panel
        self.video_panel = ctk.CTkFrame(self.main_frame)
        self.video_panel.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)

        self.video_label = ctk.CTkLabel(self.video_panel, text="", fg_color="black")
        self.video_label.pack(fill="both", expand=True)

        self.photo_path: str | None = None
        self.video_path: str | None = None

        self.source_type.trace_add("write", self.on_source_change)
        self.on_source_change()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_source_change(self, *args):
        mode = self.source_type.get()
        if mode == "photo":
            self.photo_btn.configure(state="normal")
            self.video_btn.configure(state="disabled")
        elif mode == "video":
            self.photo_btn.configure(state="disabled")
            self.video_btn.configure(state="normal")
        else:
            self.photo_btn.configure(state="disabled")
            self.video_btn.configure(state="disabled")

    def select_photo(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self.photo_path = path
            self.status_label.configure(text=f"Photo: {path.split('/')[-1]}")

    def select_video(self):
        path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if path:
            self.video_path = path
            self.status_label.configure(text=f"Video: {path.split('/')[-1]}")

    def start_detection(self):
        if self.is_running:
            return
        mode = self.source_type.get()
        if mode == "webcam":
            source = 0
        elif mode == "photo":
            if not self.photo_path:
                self.status_label.configure(text="Error: No photo selected")
                return
            source = self.photo_path
        elif mode == "video":
            if not self.video_path:
                self.status_label.configure(text="Error: No video selected")
                return
            source = self.video_path
        else:
            return

        self.stop_event.clear()
        self.video_thread = VideoProcessor(source, self.engine, self.update_frame, self.stop_event)
        self.video_thread.start()
        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_label.configure(text="Status: Running...")

    def stop_detection(self):
        if not self.is_running:
            return
        self.stop_event.set()
        if self.video_thread:
            self.video_thread.join(timeout=1)
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="Status: Stopped")
        self.fps_label.configure(text="FPS: --")

    def update_frame(self, rgb_image: np.ndarray | None, error_msg: str | None, fps: float):
        """Called from video thread – updates GUI safely."""
        if error_msg:
            self.after(0, self._show_error, error_msg)
            return
        if rgb_image is not None:
            img = Image.fromarray(rgb_image)
            pw = self.video_panel.winfo_width()
            ph = self.video_panel.winfo_height()
            if pw > 10 and ph > 10:
                # Use modern Pillow resampling constant
                img = img.resize((pw - 20, ph - 20), Image.Resampling.LANCZOS)
            else:
                img = img.resize((780, 440), Image.Resampling.LANCZOS)
            self.current_image = ImageTk.PhotoImage(image=img)
            self.after(0, self._set_image, self.current_image)
            # Update FPS using lambda to avoid type mismatch
            self.after(0, lambda f=fps: self.fps_label.configure(text=f"FPS: {f:.1f}"))

    def _set_image(self, img: ImageTk.PhotoImage):
        self.video_label.configure(image=img)

    def _show_error(self, msg: str):
        self.status_label.configure(text=f"Error: {msg}")
        self.stop_detection()

    def on_close(self):
        self.stop_event.set()
        if self.video_thread and self.video_thread.is_alive():
            self.video_thread.join(timeout=1)
        self.destroy()

# ------------------------- Main -------------------------
if __name__ == "__main__":
    app = TeslaAutopilotApp()
    app.mainloop()