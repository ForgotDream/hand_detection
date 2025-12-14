from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
import pyautogui

class CameraWorker(QThread):
  image_ready = pyqtSignal(QPixmap)

  def __init__(self, source, processor, mouse_queue):
    super().__init__()
    self.source = source
    self.processor = processor
    self.running = True
    self.mouse_queue = mouse_queue
    self.processed_image = None
    self.last_mouse_x = None
    self.last_mouse_y = None
    self.last_hold = False

  def run(self):
    if not self.source.start():
      print("Stream source failed to start.")
      self.running = False
      return

    while self.running:
      frame, timestamp = self.source.get_frame()
      if frame is None:
        # Sleep if frame capture failed
        self.msleep(1)
        continue

      # Process image every frame for smooth display
      processed_image = self.processor.process_image(frame, timestamp)

      # Send mouse commands only when coordinates change significantly
      coordinates = self.processor.get_latest_finger_coordinates()
      if coordinates["index_finger"]:
        x, y = coordinates["index_finger"]
        screen_width, screen_height = pyautogui.size()
        height, width = frame.shape[:2]
        screen_x = int(((width - x) / width) * screen_width)
        screen_y = int((y / height) * screen_height)
        screen_x = max(0, min(screen_width - 1, screen_x))
        screen_y = max(0, min(screen_height - 1, screen_y))
        # Calculate hold
        hold = False
        if coordinates["index_finger"] and coordinates["middle_finger"]:
          ix, iy = coordinates["index_finger"]
          mx, my = coordinates["middle_finger"]
          dis = ((ix - mx)**2 + (iy - my)**2)**0.5
          thres = 60 
          hold = dis < thres
        
        # Only send if coordinates changed significantly or hold state changed
        if (self.last_mouse_x is None or 
            abs(screen_x - self.last_mouse_x) > 10 or 
            abs(screen_y - self.last_mouse_y) > 10 or 
            hold != self.last_hold):
          self.mouse_queue.put((screen_x, screen_y, hold))
          self.last_mouse_x = screen_x
          self.last_mouse_y = screen_y
          self.last_hold = hold
        # self.mouse_queue.put((screen_x, screen_y, hold))

      # Emit image every frame for smooth display
      self.image_ready.emit(processed_image)
  
  def stop(self):
    self.running = False
    self.source.close()
    self.wait()