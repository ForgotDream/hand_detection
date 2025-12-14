import cv2
import time
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

class DrawUtils:
  def __init__(self):
    self.prev_frame_time = 0
    self.new_frame_time = 0
    self.MARGIN = 10  # pixels
    self.FONT_SIZE = 1
    self.FONT_THICKNESS = 1
    self.HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

  def draw_roi(self, image, roi_manager):
    x = roi_manager.x_offset
    y = roi_manager.y_offset
    width = roi_manager.width
    height = roi_manager.height
    scale = roi_manager.scale

    roi_color = (0, 255, 0)  # Green
    roi_thickness = 2
    cv2.rectangle(image, (x, y), (x + width, y + height), roi_color, roi_thickness)
    cv2.putText(image, f"ROI {int(scale*100)}%", (x + 5, y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, roi_color, 1)
    return image

  def draw_fps(self, image):
    self.new_frame_time = time.time()
    # Avoid division by zero
    diff = self.new_frame_time - self.prev_frame_time
    fps = 1 / diff if diff > 0 else 0
    self.prev_frame_time = self.new_frame_time
    fps = int(fps)
    cv2.putText(image, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 2, cv2.LINE_AA)
    return image

  def draw_click_status(self, image, is_clicking):
    if is_clicking:
      height, width = image.shape[:2]
      # Draw a red filled circle in the top right corner
      color = (255, 0, 0) 
      cv2.circle(image, (width - 30, 30), 15, color, -1)
      cv2.putText(image, "Click", (width - 80, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return image

  def draw_landmarks_on_image(self, rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
      hand_landmarks = hand_landmarks_list[idx]
      handedness = handedness_list[idx]

      # Draw the hand landmarks.
      hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
      hand_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
      ])
      solutions.drawing_utils.draw_landmarks(
        annotated_image,
        hand_landmarks_proto,
        solutions.hands.HAND_CONNECTIONS,
        solutions.drawing_styles.get_default_hand_landmarks_style(),
        solutions.drawing_styles.get_default_hand_connections_style())

      # Get the top left corner of the detected hand's bounding box.
      height, width, _ = annotated_image.shape
      x_coordinates = [landmark.x for landmark in hand_landmarks]
      y_coordinates = [landmark.y for landmark in hand_landmarks]
      text_x = int(min(x_coordinates) * width)
      text_y = int(min(y_coordinates) * height) - self.MARGIN

      # Draw handedness (left or right hand) on the image.
      cv2.putText(annotated_image, f"{handedness[0].category_name}",
                  (text_x, text_y), cv2.FONT_HERSHEY_DUPLEX,
                  self.FONT_SIZE, self.HANDEDNESS_TEXT_COLOR, self.FONT_THICKNESS, cv2.LINE_AA)

    return annotated_image
