import pyautogui
import time
import cv2
import random
import numpy as np
import keyboard

ss = pyautogui.screenshot('ss.png', region=(820,315,90,90))
zdj1 = cv2.imread('ss.png')
ready = False

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err = err / float(imageA.shape[0]*imageA.shape[1])
    return err

print("Ustaw postać i wciśnij spację (zarzuć wędkę), aby kontynuować.")
keyboard.wait('space')

while True:
    ss2 = pyautogui.screenshot('ss2.png', region=(820,315,90,90))
    zdj2 = cv2.imread('ss2.png')
    m = mse(zdj1, zdj2)
    print(m)
    if m > 9000:
        print("Wykrylo")
        delay = random.randrange(1, 4, 1)/10 + random.randrange(0, 100, 1)/1000
        buffer = random.randrange(0, 2, 1) + random.randrange(0, 99, 1)/1000
        print(f'Wylawiam z opoznieniem: {delay}')
        time.sleep(delay)
        #wciska spacje na 0.1s
        keyboard.press(57)
        time.sleep(0.1)
        keyboard.release(57)
        
        time.sleep(4 + buffer)

        keyboard.press('2')
        time.sleep(0.1)
        keyboard.release('2')

        time.sleep(0.3 + buffer)

        keyboard.press(57)
        time.sleep(0.1)
        keyboard.release(57)
        
        time.sleep(10)
        ss = pyautogui.screenshot('ss.png', region=(820,315,90,90))
        zdj1 = cv2.imread('ss.png')

