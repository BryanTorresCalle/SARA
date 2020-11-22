from time import sleep
import sys
from SimpleMFRC522_Drv  import SimpleMFRC522
import RPi.GPIO as GPIO
reader = SimpleMFRC522()
def readCard():
    try:
        print("leyendo...")
        id= reader.read_id()
        sleep(1)        
        return id
    except KeyboardInterrupt:
        GPIO.cleanup()
        return
