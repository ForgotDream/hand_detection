from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from .mouse_simulator import MouseSimulator
import pyautogui

class CameraWorker(QThread):
  image_ready = pyqtSignal(QPixmap)

  def __init__(self, source, processor):
    super().__init__()
    self.source = source
    self.processor = processor
    self.mouse_simulator = MouseSimulator()
    self.running = True
    self.frame_count = 0

  def run(self):
    if not self.source.start():
      print("Stream source failed to start.")
      self.running = False
      return

    while self.running:
      frame, timestamp = self.source.get_frame()
      if frame is None:
        # Sleep if frame capture failed
        self.msleep(10)
        continue

      self.frame_count += 1
      self.frame_count %= 3
      # Process every 3rd frame to improve efficiency
      if self.frame_count == 0:
        processed_image = self.processor.process_image(frame, timestamp)

        coordinates = self.processor.get_latest_finger_coordinates()
        if coordinates["index_finger"]:
          x, y = coordinates["index_finger"]
          screen_width, screen_height = pyautogui.size()
          height, width = frame.shape[:2]
          screen_x = int(((width - x) / width) * screen_width)
          screen_y = int((y / height) * screen_height)
          self.mouse_simulator.move_mouse(screen_x, screen_y)

        # Check distance between index and middle finger tips
        if coordinates["index_finger"] and coordinates["middle_finger"]:
          ix, iy = coordinates["index_finger"]
          mx, my = coordinates["middle_finger"]
          dis = ((ix - mx)**2 + (iy - my)**2)**0.5
          thres = 20  # pixels
          self.mouse_simulator.hold_mouse(dis < thres)

        self.image_ready.emit(processed_image)
      self.msleep(1)
  
  def stop(self):
    self.running = False
    self.source.close()
    self.wait()