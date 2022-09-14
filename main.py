import pyautogui
import time
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

print('-' * 50)
print("PROGRAM DZIAŁA TYLKO PO URUCHOMIENIU JAKO ADMINISTRATOR")
print('-' * 50, end='\n')

PAUSE_BUTTON = 'left ctrl'

class PauseWhenCaught(Exception): pass

#kalkuluje roznice miedzy dwoma zdjeciami, im wyzsza liczba - tym wieksza roznica. wziete z neta nie wiem jak to dziala
def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err = err / float(imageA.shape[0]*imageA.shape[1])
    return err

#dziala jak time.sleep, z tym, ze pauzuje program gdy wykryje w tym czasie przycisniecie guzika PAUSE_BUTTON
def pause_after(pause_time):
    start_time = time.time()
    while time.time() < start_time + pause_time:
        if keyboard.is_pressed(PAUSE_BUTTON):
            while keyboard.is_pressed(PAUSE_BUTTON):
                pass
                time.sleep(0.1)
            print("Pauzuję program!")
            time.sleep(3)
            raise PauseWhenCaught
        time.sleep(0.08)

def choose_delay():
    print("""
        1. Sorta realistic (100-150ms + detection time)
        2. Less realistic (60-80ms + detection time)
        3. Zero added delay, fast as fuck!!!
        """)
    while True:
        picked_option = input("Pick the delay after which to pull out the fish: ")
        if picked_option == '1':
            return 100, 150
        if picked_option == '2':
            return 60, 80
        if picked_option == '3':
            return 0, 1
        
DELAY_LOWER, DELAY_HIGHER = choose_delay()

CHECK_FREQUENCY = 60

print("\nUmieść kursor troszkę nad głową postaci (tam gdzie pojawia się emotka ryby) i wciśnij lewy ctrl.")
keyboard.wait('left ctrl')
_x, _y = pyautogui.position()
ssregion = (_x-45, _y-45, 90, 90)

while True:
    try:
        print("Ustaw postać i wciśnij spację (zarzuć wędkę), aby kontynuować.")
        keyboard.wait('space')

        time.sleep(1.5)

        ss = pyautogui.screenshot(region=ssregion)
        zdj1 = np.asarray(ss)
        startTime = time.time()

        while True:
            try:
                ss2 = pyautogui.screenshot(region=ssregion)
                zdj2 = np.asarray(ss2)
                m = round(mse(zdj1, zdj2))
                print(f'MSE: {m}      ', end='\r')
                runTime = time.time() - startTime
                time.sleep(1/CHECK_FREQUENCY)

                if keyboard.is_pressed(PAUSE_BUTTON):
                    while keyboard.is_pressed(PAUSE_BUTTON):
                        pass
                        time.sleep(0.1)
                    print("Pauzuję program!")
                    time.sleep(5)
                    break

                if runTime > 60:
                    print("\nNie wykryto ryby przez ponad 60 sekund. Zarzucam ponownie. Jeśli problem się powtarza, zrestartuj grę.")
                    pyautogui.click(button='right', x=_x, y=_y)
                    
                    keyboard.press('2')
                    time.sleep(0.1)
                    keyboard.release('2')

                    pause_after(0.3)

                    keyboard.press(57)
                    time.sleep(0.1)
                    keyboard.release(57)
                    startTime = time.time()

                if m > 11000:
                    print("\nWykryto rybę!")

                    delay = random.randrange(DELAY_LOWER, DELAY_HIGHER, 1)/1000

                    #buffer to dodatkowy losowy delay przed zarzuceniem wędki
                    buffer = 0
                    print(f'Wyławiam z opóźnieniem: {delay}')
                    time.sleep(delay)
                    pyautogui.click(button='right', x=_x, y=_y)
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

                    zdj1 = np.asarray(ss)
                    startTime = time.time()

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
