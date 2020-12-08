import sqlite3

def getDb():
    try:
        miConexion = sqlite3.connect('server/config/pictor.db')
        return miConexion
    except:
        print("Error en la conexion")