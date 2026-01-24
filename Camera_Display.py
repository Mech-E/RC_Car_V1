import threading
import time
import pygame
import cv2
import sys
from picamera2 import Picamera2
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


class CameraDisplay:
    def __init__(self):
        # Init camera
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration()
        self.picam2.configure(config)
        self.picam2.start()

        self.width, self.height = config["main"]["size"]

        # Init pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption("YOLOv8n Object Detection")
        self.clock = pygame.time.Clock()
        self.fps = 30

        # Start YOLO detector thread
        self.detector = YOLODetector()

    def draw_boxes(self, frame, result):
        if result is None:
            return frame

        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            label = f"{result.names[cls]} {conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        return frame

    def run(self):
        while True:
            frame = self.picam2.capture_array()

            # Send frame to YOLO thread
            self.detector.update_frame(frame)

            # Draw YOLO results
            annotated = self.draw_boxes(frame.copy(), self.detector.latest_result)

            # Convert for pygame
            annotated = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            surface = pygame.surfarray.make_surface(annotated.swapaxes(0, 1))

            self.screen.blit(surface, (0, 0))
            pygame.display.update()

            # Handle quit
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.shutdown()

            self.clock.tick(self.fps)

    def shutdown(self):
        self.detector.stop()
        self.picam2.stop()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    CameraDisplay().run()