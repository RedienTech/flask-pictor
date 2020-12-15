import sqlite3
from sqlite3 import Error

def getDb():
    try:
        miConexion = sqlite3.connect('server/config/Pictor.db')
        return miConexion
    except:
        print("Error en la conexion")