from PyQt5.QtCore import QThread
from .mouse_simulator import MouseSimulator
import queue
from collections import deque

class MouseWorker(QThread):
  def __init__(self, mouse_queue):
    super().__init__()
    self.mouse_simulator = MouseSimulator()
    self.running = True
    self.mouse_queue = mouse_queue
    # Smoothing buffer
    self.position_buffer = deque(maxlen=5)
    self.hold_state = False

  def smooth_position(self, x, y):
    self.position_buffer.append((x, y))
    
    if len(self.position_buffer) < 2:
      return x, y
    
    total_x = 0
    total_y = 0
    total_weight = 0
    
    for i, (px, py) in enumerate(self.position_buffer):
      weight = i + 1  # 越新的点权重越高
      total_x += px * weight
      total_y += py * weight
      total_weight += weight
    
    smooth_x = int(total_x / total_weight)
    smooth_y = int(total_y / total_weight)
    
    return smooth_x, smooth_y

  def run(self):
    while self.running:
      try:
        x, y, hold = self.mouse_queue.get(timeout=0.01)
        self.hold_state = hold
        
        smooth_x, smooth_y = self.smooth_position(x, y)
        
        # Smooth moving mouse
        self.mouse_simulator.move_mouse(smooth_x, smooth_y)
        self.mouse_simulator.hold_mouse(self.hold_state)
      except queue.Empty:
        continue  # No message, continue loop

  def stop(self):
    self.running = False
    self.mouse_queue = None
    self.wait()