import cv2
import mediapipe as mp
import numpy as np
import os
import platform
import sys
from PyQt5.QtGui import QImage, QPixmap
from .draw_landmarks import draw_landmarks_on_image

def cv2_image_to_qpixmap(cv2_image_bgr: np.ndarray) -> QPixmap:
  cv2_image_rgb = cv2.cvtColor(cv2_image_bgr, cv2.COLOR_BGR2RGB)
  np_array = np.ascontiguousarray(cv2_image_rgb)

  height, width, _ = np_array.shape
  bytes_per_line = 3 * width
  
  q_image = QImage(
    np_array.data,
    width,
    height,
    bytes_per_line,
    QImage.Format_RGB888
  )

  q_pixmap = QPixmap.fromImage(q_image)

  return q_pixmap

class ImageProcessor:
  def __init__(self):
    base_options = mp.tasks.BaseOptions
    hand_landmarker = mp.tasks.vision.HandLandmarker
    hand_landmarker_options = mp.tasks.vision.HandLandmarkerOptions
    vision_running_mode = mp.tasks.vision.RunningMode

    root_dir = os.getcwd()
    model_path = root_dir + "/model/hand_landmarker.task"

    def callback():
      pass

    # Enable GPU acceleration on supported platforms (Linux and macOS)
    if sys.platform.startswith('linux') or sys.platform == 'darwin':
      try:
        options = hand_landmarker_options(
          base_options=base_options(
            model_asset_path=model_path,
            delegate=mp.tasks.BaseOptions.Delegate.GPU
          ),
          running_mode=vision_running_mode.VIDEO,
        )
        print("Using GPU acceleration for hand detection")
      except Exception as e:
        print(f"GPU not available, falling back to CPU: {e}")
        options = hand_landmarker_options(
          base_options=base_options(model_asset_path=model_path),
          running_mode=vision_running_mode.VIDEO,
        )
    else:
      # Windows or other platforms: use CPU
      print("Using CPU for hand detection (GPU not supported on this platform)")
      options = hand_landmarker_options(
        base_options=base_options(model_asset_path=model_path),
        running_mode=vision_running_mode.VIDEO,
      )

    self.landmarker = hand_landmarker.create_from_options(options)

    self.latest_index_finger = None
    self.latest_middle_finger = None

  def process_image(self, cv2_original_image: np.ndarray, timestamp) -> QPixmap:
    if platform.system() == "Darwin":
      frame_rgb = cv2.cvtColor(cv2_original_image, cv2.COLOR_BGR2RGBA)
      image = mp.Image(image_format=mp.ImageFormat.SRGBA, data=frame_rgb)
    else:
      frame_rgb = cv2.cvtColor(cv2_original_image, cv2.COLOR_BGR2RGB)
      image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
    detection_result = self.landmarker.detect_for_video(image, timestamp)

    if detection_result.hand_landmarks:
      hand_landmarks = detection_result.hand_landmarks[0]  # assume first hand
      height, width = cv2_original_image.shape[:2]
      self.latest_index_finger = (int(hand_landmarks[8].x * width), int(hand_landmarks[8].y * height))
      self.latest_middle_finger = (int(hand_landmarks[12].x * width), int(hand_landmarks[12].y * height))

    annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)

    q_pixmap = cv2_image_to_qpixmap(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))

    return q_pixmap

  def get_latest_finger_coordinates(self):
    return {
        "index_finger": self.latest_index_finger,
        "middle_finger": self.latest_middle_finger
    }