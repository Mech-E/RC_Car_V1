import threading
import time
import sys
from picamera2 import Picamera2
from picamera2.previews import DrmPreview
from ultralytics import YOLO


class YOLODetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)
        self.latest_result = None
        self.frame = None
        self.running = True

        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()

    def update_frame(self, frame):
        self.frame = frame

    def run(self):
        while self.running:
            if self.frame is None:
                time.sleep(0.01)
                continue

            # Run YOLO inference
            results = self.model(self.frame, verbose=False)
            self.latest_result = results[0]

    def stop(self):
        self.running = False
        self.thread.join()


class CameraWithPreviewAndYOLO:
    def __init__(self):
        self.picam2 = Picamera2()

        config = self.picam2.create_preview_configuration()
        self.picam2.configure(config)

        # Use the preview backend your system supports
        self.preview = DrmPreview()

        # Start YOLO detector thread
        self.detector = YOLODetector()

    def run(self):
        self.picam2.start(show_preview=self.preview)

        try:
            print("Camera + YOLO running. Press Ctrl+C to quit.")
            while True:
                # Grab frame for YOLO (does not affect preview)
                frame = self.picam2.capture_array()
                self.detector.update_frame(frame)

                # You can use detections here for logic
                result = self.detector.latest_result
                if result is not None:
                    for box in result.boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        print(f"Detected {result.names[cls]} ({conf:.2f})")

                time.sleep(0.01)

        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        self.detector.stop()
        self.picam2.stop()
        sys.exit()


if __name__ == "__main__":
    CameraWithPreviewAndYOLO().run()