from pynput.mouse import Controller, Button

class MouseSimulator:
  def __init__(self):
    self.mouse_pressed = False
    self.mouse_controller = Controller()

  def move_mouse(self, x: int, y: int):
    self.mouse_controller.position = (x, y)

  def click_mouse(self, x: int, y: int):
    self.mouse_controller.position = (x, y)
    self.mouse_controller.click(Button.left)

  def hold_mouse(self, hold: bool):
    if hold and not self.mouse_pressed:
      self.mouse_controller.press(Button.left)
      print("Mouse Down")
      self.mouse_pressed = True
    elif not hold and self.mouse_pressed:
      self.mouse_controller.release(Button.left)
      print("Mouse Up")
      self.mouse_pressed = False