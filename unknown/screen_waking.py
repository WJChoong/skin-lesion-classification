import pyautogui
import time
while True:
    for i in range(0,100):
        for j in range(0,100):
            pyautogui.moveTo(500+j,500)
        time.sleep(5)