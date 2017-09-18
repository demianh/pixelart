from time import sleep

import bibliopixel
#causes frame timing information to be output
bibliopixel.log.setLogLevel(bibliopixel.log.DEBUG)

#Load driver for the AllPixel
from bibliopixel.drivers.serial import Serial, LEDTYPE
#set number of pixels & LED type here 
driver = Serial(width=10, height=5, num=50, ledtype = LEDTYPE.WS2812B)

#load the LEDMatrix class
from bibliopixel import Matrix, Rotation
#change rotation, vert_flip, and serpentine as needed by your display
led = Matrix(driver, 
                rotation = Rotation.ROTATE_0, 
                vert_flip = True,
                serpentine = True)


try:
    bibliopixel.image.showImage(led, "5x10.png", bgcolor = (64, 64, 64))
    led.update()
except KeyboardInterrupt:
    #Ctrl+C will exit the animation and turn the LEDs offs
    led.all_off()
    led.update()
