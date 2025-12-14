import pyautogui

class ROIManager:
  def __init__(self, scale=0.8):
    self.scale = scale
    self.x_offset = 0
    self.y_offset = 0
    self.width = 0
    self.height = 0
    self.screen_width, self.screen_height = pyautogui.size()

  def update_dimensions(self, frame_width, frame_height):
    if self.width == 0:
      self.width = int(frame_width * self.scale)
      self.height = int(frame_height * self.scale)
      self.x_offset = (frame_width - self.width) // 2
      self.y_offset = (frame_height - self.height) // 2

  def map_to_screen(self, x, y):
    # Check if point is inside ROI
    if not (self.x_offset <= x < self.x_offset + self.width and
            self.y_offset <= y < self.y_offset + self.height):
      return None
    
    roi_x = x - self.x_offset
    roi_y = y - self.y_offset
    
    # Map to screen coordinates (mirroring x axis for natural movement)
    screen_x = int(((self.width - roi_x) / self.width) * self.screen_width)
    screen_y = int((roi_y / self.height) * self.screen_height)
    
    # Clamp to screen bounds
    screen_x = max(0, min(self.screen_width - 1, screen_x))
    screen_y = max(0, min(self.screen_height - 1, screen_y))
    
    return screen_x, screen_y
