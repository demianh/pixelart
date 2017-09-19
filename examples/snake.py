### Config

# screen width and height
WIDTH = 10
HEIGHT = 5

# Important: Run with sudo on mac: "sudo python3 snake.py"


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

direction = []
snake = []
apple = []
hasLost = True
speed = 0.5

def reset_game():
    global direction, snake, apple, hasLost
    direction = [1, 0] # x, y
    snake = [[4,1], [3,1], [2,1], [1,1]]
    apple = [2, 3]
    hasLost = False

reset_game()

from pynput.keyboard import Key, Listener

def on_press(key):
    import math
    global direction

    #print('{0} pressed'.format(key))

    # change cursor position
    # relative change
    if (hasattr(key, 'char') and key.char == '6'):
        x = int(direction[0] * math.cos(math.radians(90)) - direction[1] * math.sin(math.radians(90)))
        y = int(direction[1] * math.cos(math.radians(90)) + direction[0] * math.sin(math.radians(90)))
        direction = [x, y]
    if (hasattr(key, 'char') and key.char == '5'):
        x = int(direction[0] * math.cos(math.radians(-90)) - direction[1] * math.sin(math.radians(-90)))
        y = int(direction[1] * math.cos(math.radians(-90)) + direction[0] * math.sin(math.radians(-90)))
        direction = [x, y]

    # absolute change
    if (key == Key.right or (hasattr(key, 'char') and key.char == 'd')):
        direction = [1, 0]
    if (key == Key.left  or (hasattr(key, 'char') and key.char == 'a')):
        direction = [-1, 0]
    if (key == Key.up    or (hasattr(key, 'char') and key.char == 'w')):
        direction = [0, -1]
    if (key == Key.down  or (hasattr(key, 'char') and key.char == 's')):
        direction = [0, 1]
    if (key == Key.enter):
        reset_game()

# Collect events until released
with Listener(on_press=on_press) as listener:
    print('Listener started. Press LEFT/RIGHT keys to change direction and ENTER to restart.')

    try:
        led.all_off()
        led.update()

        # update screen (should be done on one thread only)
        while(True):
            led.all_off()

            if (hasLost == False):
                # calculate new position
                newposition = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

                # eat apple
                appleEaten = False
                if (newposition == apple):
                    appleEaten = True

                    # position new apple
                    while True:
                        newApple = [random.randint(0, WIDTH-1),random.randint(0, HEIGHT-1)]
                        if (newApple not in snake and newApple != newposition):
                            apple = newApple
                            break
                
                # check if new position is valid
                if (newposition[0] >= WIDTH 
                    or newposition[0] < 0 
                    or newposition[1] >= HEIGHT 
                    or newposition[1] < 0
                    or newposition in snake
                    ):
                    hasLost = True
                    print('\n\nGAME OVER! You made {0} points. Press ENTER to restart.\n'.format(len(snake) - 4))
                else:
                    # move snake
                    snake.insert(0, newposition)
                    if (appleEaten == False):
                        del snake[-1]

            # draw snake
            for pos in snake:
                if (hasLost):
                    # red snake
                    led.set(pos[0],pos[1],(255,0,0))
                else:
                    # green snake
                    led.set(pos[0],pos[1],(0,255,0))

            # draw apple
            led.set(apple[0],apple[1],(255,255,255))

            led.update()
            sleep(speed)

    except KeyboardInterrupt:
        #Ctrl+C will exit the animation and turn the LEDs offs
        led.all_off()
        led.update()

    listener.join()
