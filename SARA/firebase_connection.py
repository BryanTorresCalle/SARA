import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# cred = credentials.Certificate('/home/pi/Desktop/SARA/credenciales.json')
# # Initialize the app with a service account, granting admin privileges
# firebase_admin.initialize_app(cred, {
#  'databaseURL': 'https://sara-alarma-iot.firebaseio.com/'
# })
# ref = db.reference('Estado')
# print(ref.set("Hola Mundo"))
# print ('Ok !')

def connect():
    cred = credentials.Certificate('/home/pi/Desktop/SARA/credenciales.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
     'databaseURL': 'https://sara-alarma-iot.firebaseio.com/'
    })
    
    print ('Ok !')
    
    
def writeDB(key,value):
    try:
        ref = db.reference(key)
        ref.set(value)
        print("Escritura en la base exitosa")
    except Exception:
        print("Error escribiendo en la BD")
        raise
    
def readDB(key):
    try:
        ref = db.reference(key)
        
        return ref.get()
    except Exception:
        print("Error leyendo en la BD")
        raise
    
def pushDB(key,value):
    db.reference(key).push(value)