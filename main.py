import pyautogui
import time
import cv2
import random
import numpy as np
import keyboard
import sys

def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err = err / float(imageA.shape[0]*imageA.shape[1])
    return err

while True:
    try:
        print("Ustaw postać i wciśnij spację (zarzuć wędkę), aby kontynuować.")
        keyboard.wait('space')

        time.sleep(1.5)

        ss = pyautogui.screenshot('ss.png', region=(820,315,90,90))
        zdj1 = cv2.imread('ss.png')
        ready = False

        while True:
            ss2 = pyautogui.screenshot('ss2.png', region=(820,315,90,90))
            zdj2 = cv2.imread('ss2.png')
            m = round(mse(zdj1, zdj2))
            print(f'MSE: {m}', end='\r')
            time.sleep(0.1)

            if keyboard.is_pressed('left ctrl'):
                while keyboard.is_pressed('left ctrl'):
                    pass
                    time.sleep(0.1)
                print("Pauzuję program!")
                time.sleep(5)
                break

            if m > 9000:
                print("\nWykryto rybę!")
                delay = random.randrange(1, 4, 1)/10 + random.randrange(0, 100, 1)/1000
                buffer = random.randrange(0, 2, 1) + random.randrange(0, 99, 1)/1000
                print(f'Wyławiam z opóźnieniem: {delay}')
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
                
                time.sleep(3.5)
                ss = pyautogui.screenshot('ss.png', region=(820,315,90,90))
                zdj1 = cv2.imread('ss.png')
    except KeyboardInterrupt:
        print("Do zobaczenia!!")
        break
