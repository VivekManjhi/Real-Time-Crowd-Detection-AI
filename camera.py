import time

class CameraSystem:
    def __init__(self):
        self.cams = [0]  # single camera (safe)
        self.index = 0
        self.last = time.time()

    def get_camera(self):
        return self.cams[0]