import RPi.GPIO as GPIO
import time

#configuracion de los pines 
GPIO.setmode(GPIO.BOARD)

#pines para la  configuracion del sensor ultrasinico
Trigger = 18
Echo = 16
GPIO.setup(Trigger, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

# SENSOR ULTRASONICO

#Metodo encargado de usar el trigger para enviar el tren de pulso
def send_trigger_pulse():
    GPIO.output(Trigger,True)
    time.sleep(0.00001)
    GPIO.output(Trigger,False)

#Metodo encargado de usar en echo para recibir el tren de pulso despues de rebotar en un objeto
def wait_for_echo(value, timeout):
    count=timeout
    while GPIO.input(Echo) != value and count>0:
        count=count-1

#Metodo encargado de medir el tiempo para para posteriormente multiplicarlo
# por la velocidad del sonido y hallar la distancio en segundos  
def get_distance():
    send_trigger_pulse()
    wait_for_echo(True,10000) 
    start=time.time()
    wait_for_echo(False,10000)
    finish=time.time()
    pulse_len= finish-start
    distance_cm=(pulse_len*34029)/2
    return distance_cm


#Loop principal
