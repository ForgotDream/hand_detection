import pyautogui

class MouseSimulator:
  def __init__(self):
    self.mouse_pressed = False

  def move_mouse(self, x: int, y: int):
    pyautogui.moveTo(x, y)

  def click_mouse(self, x: int, y: int):
    pyautogui.click(x, y)

  def hold_mouse(self, hold: bool):
    if hold and not self.mouse_pressed:
      pyautogui.mouseDown()
      print("Mouse Down")
      self.mouse_pressed = True
    elif not hold and self.mouse_pressed:
      pyautogui.mouseUp()
      self.mouse_pressed = False