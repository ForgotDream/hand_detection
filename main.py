from src.create_window import CameraWindow
from src.camera_worker import CameraWorker
from src.mouse_worker import MouseWorker
from src.video_stream import VideoStream
from src.image_processor import ImageProcessor
from PyQt5.QtWidgets import QApplication
import queue

app = QApplication([])
mouse_queue = queue.Queue()
camera_worker = CameraWorker(VideoStream(), ImageProcessor(), mouse_queue)
mouse_worker = MouseWorker(mouse_queue)

camera = CameraWindow(camera_worker)
camera.resize(1280, 720)

# Start threads
camera_worker.start()
mouse_worker.start()

camera.show()
app.exec()

# Stop threads when app closes
camera_worker.stop()
mouse_worker.stop()