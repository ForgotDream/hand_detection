from src.create_window import CameraWindow
from src.camera_worker import CameraWorker
from src.video_stream import VideoStream
from src.image_processor import ImageProcessor
from PyQt5.QtWidgets import QApplication

app = QApplication([])
camera_worker = CameraWorker(VideoStream(), ImageProcessor())
camera = CameraWindow(camera_worker)
camera.resize(800, 600)

camera.show()
app.exec()