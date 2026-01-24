import pygame
import cv2
import sys
from picamera2 import Picamera2


class CameraDisplay:
    def __init__(self):
        # Initialize Picamera2
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration()
        self.picam2.configure(config)
        self.picam2.start()

        # Extract resolution
        self.width, self.height = config["main"]["size"]

        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption("Live Camera Feed")
        self.clock = pygame.time.Clock()

        # FPS target (Picamera2 usually runs 30fps by default)
        self.fps = 30

    def run(self):
        while True:
            # Capture frame from Pi Camera
            frame = self.picam2.capture_array()

            # Convert BGR → RGB for pygame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert to pygame surface
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

            # Draw to screen
            self.screen.blit(frame_surface, (0, 0))
            pygame.display.update()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutdown()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.shutdown()

            self.clock.tick(self.fps)

    def shutdown(self):
        self.picam2.stop()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    CameraDisplay().run()