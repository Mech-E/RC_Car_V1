from picamera2 import Picamera2
from picamera2.previews import DrmPreview
import sys


class CameraDisplayGL:
    def __init__(self):
        self.picam2 = Picamera2()

        config = self.picam2.create_preview_configuration()
        self.picam2.configure(config)

        # Use the preview backend your system actually supports
        self.preview = DrmPreview()

    def run(self):
        self.picam2.start(show_preview=self.preview)

        try:
            print("Camera running. Press Ctrl+C to quit.")
            while True:
                pass
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        self.picam2.stop()
        sys.exit()


if __name__ == "__main__":
    CameraDisplayGL().run()