from PyQt5.QtCore import QThread
from .mouse_simulator import MouseSimulator
import queue

class MouseWorker(QThread):
  def __init__(self, mouse_queue):
    super().__init__()
    self.mouse_simulator = MouseSimulator()
    self.running = True
    self.mouse_queue = mouse_queue

  def run(self):
    while self.running:
      try:
        # Non-blocking get with shorter timeout
        x, y, hold = self.mouse_queue.get(timeout=0.01)
        self.mouse_simulator.move_mouse(x, y)
        self.mouse_simulator.hold_mouse(hold)
      except queue.Empty:
        continue  # No message, continue loop

  def stop(self):
    self.running = False
    self.mouse_queue = None
    self.wait()