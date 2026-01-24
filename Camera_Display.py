import sys
from picamera2 import Picamera2
from picamera2.previews import FullscreenPreview


class CameraDisplayGL:
    def __init__(self):
        # Init camera
        self.picam2 = Picamera2()

        # Choose a reasonable preview configuration
        config = self.picam2.create_preview_configuration()
        self.picam2.configure(config)

        # Create OpenGL preview (fullscreen by default on Pi)
        self.preview = OpenGLPreview()

    def run(self):
        # Start camera with OpenGL preview
        self.picam2.start(show_preview=self.preview)

        try:
            # Block forever; preview runs in its own loop
            print("Camera running with OpenGL preview. Press Ctrl+C to quit.")
            while True:
                pass
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        self.picam2.stop()
        sys.exit()


if __name__ == "__main__":
    CameraDisplayGL().run()