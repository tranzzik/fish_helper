import pyautogui
import time
#import cv2 no longer needed
import random
import numpy as np
import keyboard

print(r"""

           ___ _    _      _             _      _     
  ___ __ _| __(_)__| |_   | |__ _  _    (_)_  _| |___ 
 (_-</ _` | _|| (_-< ' \  | '_ \ || |   | | || | / _ \
 /__/\__, |_| |_/__/_||_| |_.__/\_, |  _/ |\_,_|_\___/
     |___/                      |__/  |__/            

""")

pause_button = 'left ctrl'

class PauseWhenCaught(Exception): pass

#kalkuluje roznice miedzy dwoma zdjeciami, im wyzsza liczba - tym wieksza roznica. wziete z neta nie wiem jak to dziala
def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err = err / float(imageA.shape[0]*imageA.shape[1])
    return err

#dziala jak time.sleep, z tym, ze pauzuje program gdy wykryje w tym czasie przycisniecie guzika pause_button
def pause_after(pause_time):
    start_time = time.time()
    while time.time() < start_time + pause_time:
        if keyboard.is_pressed(pause_button):
            while keyboard.is_pressed(pause_button):
                pass
                time.sleep(0.1)
            print("Pauzuję program!")
            time.sleep(5)
            raise PauseWhenCaught

print("Umieść kursor troszkę nad głową postaci (tam gdzie pojawia się emotka ryby) i wciśnij lewy ctrl.")
keyboard.wait('left ctrl')
x, y = pyautogui.position()
ssregion = (x-45, y-45, 90, 90)
#old region = (820,315,90,90)

while True:
    try:
        print("Ustaw postać i wciśnij spację (zarzuć wędkę), aby kontynuować.")
        keyboard.wait('space')

        time.sleep(1.5)

        ss = pyautogui.screenshot(region=ssregion)
        #zdj1 = cv2.imread('ss.png')
        zdj1 = np.asarray(ss)


        while True:
            try:
                ss2 = pyautogui.screenshot(region=ssregion)
                #zdj2 = cv2.imread('ss2.png')
                zdj2 = np.asarray(ss2)
                m = round(mse(zdj1, zdj2))
                print(f'MSE: {m}      ', end='\r')
                time.sleep(0.07)

                if keyboard.is_pressed(pause_button):
                    while keyboard.is_pressed(pause_button):
                        pass
                        time.sleep(0.1)
                    print("Pauzuję program!")
                    time.sleep(5)
                    break

                if m > 11000:
                    print("\nWykryto rybę!")
                    time_lottery = random.randrange(1,20,1)

                    if time_lottery == 7:
                        delay = random.randrange(1, 3, 1)/10 + random.randrange(0, 100, 1)/1000
                    else:
                        delay = random.randrange(60, 80, 1)/1000
                        #delay = random.randrange(10, 20, 1)/1000

                    #buffer = random.randrange(1, 4, 1)/2 + random.randrange(0, 99, 1)/1000
                    buffer = 0
                    print(f'Wyławiam z opóźnieniem: {delay}')
                    time.sleep(delay)
                    pyautogui.click(button='right', x=x, y=y)
                    #wciska spacje na 0.1s
                    keyboard.press(57)
                    time.sleep(0.1)
                    keyboard.release(57)
                    
                    pause_after(4 + buffer)

                    keyboard.press('2')
                    time.sleep(0.1)
                    keyboard.release('2')

                    pause_after(0.5 + buffer)

                    keyboard.press(57)
                    time.sleep(0.1)
                    keyboard.release(57)
                    
                    pause_after(3.5)

                    ss = pyautogui.screenshot(region=ssregion)
                    #zdj1 = cv2.imread('ss.png')
                    zdj1 = np.asarray(ss)

            except PauseWhenCaught:
                break
    
    except KeyboardInterrupt:
        print(r"""
                            ____            ______
        ___ ____  ___  ___/ / /  __ _____ / / / /
        / _ `/ _ \/ _ \/ _  / _ \/ // / -_)_/_/_/ 
        \_, /\___/\___/\_,_/_.__/\_, /\__(_|_|_)  
        /___/                    /___/             
        """)
        break
