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
    for x in range(0, 255):
        print("We're on time %d" % (x))
        led.set(6,2,(x,(x + 50) % 255,(x + 150) % 255))
        led.set(6,3,((x + 120) % 255,(x + 180) % 255,x))
        led.set(6,4,((x + 200) % 255,x,(x + 100) % 255))
        led.update()
        sleep(0.01)
except KeyboardInterrupt:
    #Ctrl+C will exit the animation and turn the LEDs offs
    led.all_off()
    led.update()
