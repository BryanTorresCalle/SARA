import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
BUZZER= 36
buzzState = False
GPIO.setup(BUZZER, GPIO.OUT)

while True:
    buzzState = not buzzState
    GPIO.output(BUZZER, buzzState)
    time.sleep(10)