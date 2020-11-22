

#Se importan las librerias Necesarias
import firebase_connection
import UltraSonico
import RPi.GPIO as GPIO
import display
from time import sleep
import termocupla
import multiprocessing
import rfid
from datetime import datetime

#Conexión con  la base de datos
firebase_connection.connect()

#Inicializar display
display.lcd_init()
#Variables Globales
alarm = False
stateAlarm = False
BUZZER= 36

#Declaración de puertoa GPIO para buzzer y led
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.output(BUZZER, False)
led= 22
GPIO.setup(led, GPIO.OUT)
GPIO.output(led, False)

#Proceso para autenticarse por medio del lector rfid
def auth():
    led= 22
    global alarm
    global stateAlarm
    while True:
        sleep(1)
        print("Ponga su tarjeta")
        card = rfid.readCard() #lectra de la tarjeta rfid
        print("id: ",card)
        sleep(1)
        idcard = firebase_connection.readDB("idcard") #Lectura de la id de la tarjeta rfid
        
        if idcard == card: #verificacion de que la tarjeta sea del usuario correcto
            GPIO.output(led, True) #Prende un led si se autentica
            sleep(2)
            alarm = not alarm #Hace swith en la habilitación de la alarma
            firebase_connection.writeDB("Alarma", alarm) #Escritura de la activación de la alarma
            stateAlarm = False #desativa la alarma 
            firebase_connection.writeDB("Estado", stateAlarm)  #escritura en la base de datos del estado de la alarma
        sleep(9)
            
        
#Proceso para lectura de la termocupla 
def readThermocouple():
    lastTime = 0
    currentTime = (datetime.now().hour) # Lectura de la hora actual
    while True:
        sleep(2)
        temp = round(termocupla.getTemperature(),2) #Lectura de la termocupla
        print(temp)
        firebase_connection.writeDB("Temperatura", temp) #escritura en la base de datos de la variable temperatura
        currentTime = (datetime.now().hour) #lee la hora actual
        if temp > 60: #verifica si la temperatura es mayor a 60 grados, implicando alerta de incendio
            if currentTime != lastTime: #Control para que no se generen varios historicos de alertas por una misma alerta de incendio
                lastTime = currentTime
                firebase_connection.pushDB("Historial", ("Alerta de incendio - " + str(datetime.now()) )) #Escritura en el historico de alarmas
                firebase_connection.writeDB("Estado", True) # Escritura en la base de datos activando la alarma
                GPIO.output(BUZZER, True) # Genera sonido en buzzer
                sleep(15)
                GPIO.output(BUZZER, False) # Apaga el buzzer
        sleep(10)

#Proceso para la lectura del sensor ultrasonico
def readUltrasonico(dist):
    newDist = 0
    while True:
        sleep(5)
        
        alarm = firebase_connection.readDB("Alarma") #Lectura del estado de la alarma
        print(alarm)
        
        #Si la alarma esta habilitada el ultrasonico empieza e sensar si hay un movimiento al frente
        if(alarm):
            newDist = round(UltraSonico.get_distance(),2) #deteccion de la nueva distancia
            print(newDist)
            #Si es un dato difernete con un margen de dos centimetros al ultimo valor leido, la alarma se avtiva
            if (newDist > (dist + 2) or newDist < (dist - 2)): 
                stateAlarm = True
                firebase_connection.writeDB("Estado", True) #Se pone en verdadero el estado de la alarma en la base de datos
                #Activa el buzzer
                GPIO.output(BUZZER, True)
                sleep(15)
                #apaga el buzzer
                GPIO.output(BUZZER, False)
            else:
                stateAlarm = False
            sleep(1)
        dist = newDist 
        sleep(3)

#Proceso para mostrar la informacion en el display a partir de los datos en Firebase
def showInfoDisplay():
   
        
    while True:
        sleep(6)
        display.show(("Estado: " + str(firebase_connection.readDB("Estado")) ), ("T:" + str(firebase_connection.readDB("Temperatura")) + " C" ))
        sleep(10)

#Delaracacion de multiprocesos, que permiten el manejo de las funciones en hilos
pAuth = multiprocessing.Process(target=auth)
pTherm = multiprocessing.Process(target=readThermocouple)
pUltras = multiprocessing.Process(target=readUltrasonico, args=[133])
pShow =  multiprocessing.Process(target=showInfoDisplay)

#Iniciar Multiprocesos
pAuth.start()
pTherm.start()
pUltras.start()
pShow.start()
    
    
    
