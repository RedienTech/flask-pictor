import mysql.connector

def getDb():
    miConexion = mysql.connector.connect( host='localhost', user= 'root', passwd='', db='pictor')
    return miConexion