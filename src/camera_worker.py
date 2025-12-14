from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
import pyautogui
from .mouse_simulator import MouseSimulator
from .roi_manager import ROIManager
import cv2

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
    self.roi_manager = ROIManager(scale=0.8)

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
      processed_image = self.processor.process_image(frame, timestamp, self.roi_manager)
      
      # Get coordinates
      coordinates = self.processor.get_latest_finger_coordinates()
      
      # Calculate hold status using MouseSimulator static method
      hold = MouseSimulator.calculate_click_state(coordinates["index_finger"], coordinates["middle_finger"])

      # Send mouse commands only when coordinates change significantly
      if coordinates["index_finger"]:
        x, y = coordinates["index_finger"]
        
        screen_pos = self.roi_manager.map_to_screen(x, y)
        
        if screen_pos is None:
          self.msleep(1)
          continue
          
        screen_x, screen_y = screen_pos
        
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