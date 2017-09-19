### Config

# screen width and height
WIDTH = 10
HEIGHT = 5

# Important: Run with sudo on mac: "sudo python3 test_keyboard.py"


from time import sleep
import random

import bibliopixel
#causes frame timing information to be output
bibliopixel.log.setLogLevel(bibliopixel.log.DEBUG)

#Load driver for the AllPixel
from bibliopixel.drivers.serial import Serial, LEDTYPE
#set number of pixels & LED type here 
driver = Serial(width=WIDTH, height=HEIGHT, num=WIDTH*HEIGHT, ledtype = LEDTYPE.WS2812B)

#load the LEDMatrix class
from bibliopixel import Matrix, Rotation
#change rotation, vert_flip, and serpentine as needed by your display
led = Matrix(driver, 
                rotation = Rotation.ROTATE_180, 
                vert_flip = True,
                serpentine = True)

pos_x = 1
pos_y = 1

from pynput.keyboard import Key, Listener

def on_press(key):
    global pos_x
    global pos_y

    # change cursor position
    if (key == Key.right):
        pos_x = min(pos_x + 1, WIDTH - 1)
    if (key == Key.left):
        pos_x = max(pos_x - 1, 0)
    if (key == Key.up):
        pos_y = max(pos_y - 1, 0)
    if (key == Key.down):
        pos_y = min(pos_y + 1, HEIGHT - 1)
    
    #print('{0} pressed'.format(key))
    #print('cursort at position x: {0} y: {1}'.format(pos_x, pos_y))

# def on_release(key):
#     print('{0} release'.format(
#         key))
#     if key == Key.esc:
#         # Stop listener
#         return False

# Collect events until released
with Listener(on_press=on_press) as listener:
    print('Listener started. Press arrow keys to move cursor.')

    try:
        led.all_off()
        led.update()
        while(True):
            # update screen (should be done on one thread only)
            led.set(pos_x,pos_y,(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)))
            led.update()
            #sleep(0.01)
    except KeyboardInterrupt:
        #Ctrl+C will exit the animation and turn the LEDs offs
        led.all_off()
        led.update()

    listener.join()
