import sqlite3
from sqlite3 import Error

def getDb():
    try:
        miConexion = sqlite3.connect('server/config/pictor.db')
        return miConexion
    except Error:
        return Error
