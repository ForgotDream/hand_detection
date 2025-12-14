import numpy as np
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class CameraWindow(QWidget):
  def __init__(self, worker):
    super().__init__()
    self.setWindowTitle("Test Window")

    self.image_label = QLabel(self)
    self.image_label.setAlignment(Qt.AlignCenter)
    layout = QVBoxLayout()
    layout.addWidget(self.image_label)
    self.setLayout(layout)

    self.worker = worker
    self.worker.image_ready.connect(self.update_frame)
    self.worker.start()

  def update_frame(self, q_pixmap: QPixmap):
    scaled_pixmap = q_pixmap.scaled(
      self.image_label.size(),
      Qt.KeepAspectRatio,
      Qt.SmoothTransformation
    )
    self.image_label.setPixmap(scaled_pixmap)
    pass

  def closeEvent(self, event):
    self.worker.stop()
    super().closeEvent(event)