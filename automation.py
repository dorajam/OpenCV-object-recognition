import pyautogui

# pyautogui.PAUSE = 1
# pyautogui.FAILSAFE = True
width, height = pyautogui.size()

def mousemove(center):
    pyautogui.moveTo(center[1],center[0], duration=0.25)
    # pyautogui.moveTo(500, 100, duration=0.25)
    # pyautogui.moveTo(500, 500, duration=0.25)
    # pyautogui.moveTo(100, 200, duration=0.25)

