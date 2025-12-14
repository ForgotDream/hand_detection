import cv2
import platform
import time

def get_capture(camera_index = 0):
  os_name = platform.system()

  if os_name == "Linux":
    cap_backend = cv2.CAP_V4L2
    print("Detected Linux/WSL, attempting V4L2 backend.")
  elif os_name == "Windows":
    cap_backend = cv2.CAP_MSMF 
    print("Detected Windows, attempting MSMF backend.")
  else:
    cap_backend = cv2.CAP_ANY 
    print("Detected other OS, using default backend.")

  cap = cv2.VideoCapture(camera_index, cap_backend)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

  print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

  return cap

class VideoStream:
  def __init__(self, camera_index = 0):
    self.camera_index = camera_index
    self.cap = None
    self.prev_timestamp = 0
    
  def start(self):
    self.cap = get_capture(self.camera_index)
    if not self.cap.isOpened:
      print("Can't open system camera!")
      return False
    return True
  
  def get_frame(self):
    if self.cap is None:
      print("Capture device not initialized.")
      return None, None

    ret, frame = self.cap.read()

    if not ret:
      print("Can't capture image from system camera!")
      return None, None

    timestamp = int(time.time() * 1000)
    
    # print(f"Captured frame at {timestamp} ms")
    # print(f"fps: {1000/(timestamp - self.prev_timestamp + 1e-5)}")
    self.prev_timestamp = timestamp

    return frame, timestamp

  def close(self):
    if self.cap:
      self.cap.release()
      self.cap = None