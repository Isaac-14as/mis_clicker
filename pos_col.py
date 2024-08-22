import pyautogui
import time


while True:
    x, y = pyautogui.position()
    specific_pixel_color = pyautogui.pixel(x, y)
    time.sleep(1)
    print(f'Координаты: {x, y}, цвет RGB: {specific_pixel_color}')


