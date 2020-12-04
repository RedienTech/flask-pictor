import bcrypt
from config.db import getDb

class User:
    def __init__(self):
        self.register = False
        self.mysql = getDb()
        self.errors = []

    def Registrar(self, nombre, usuario, clave, cclave, ccorreo, correo):
        if clave != cclave or len(clave) < 6:
            self.errors.append("Claves no coinciden o es demasiado corta")
        if correo != ccorreo:
            self.errors.append("Correos electronicos no coinciden")
        cur = self.mysql.cursor()
        cur.execute("SELECT usuario FROM usuarios WHERE correo = '" + correo + "';")
        existEmail = cur.fetchall()
        print(existEmail)
        if len(existEmail) >= 1:
            self.errors.append("Ya existe un usuario registrado con este correo electronico")
        cur.execute("SELECT usuario FROM usuarios WHERE usuario = '" + usuario + "';")
        existUser = cur.fetchall()
        if len(existUser) >= 1:
            self.errors.append("El usuario ya esta en uso")
        
        if len(self.errors) < 1:
            password = clave.encode(encoding='UTF-8',errors='strict')
            clave = bcrypt.hashpw(password, b'$2b$12$CSEMJ59OZhiDLX1ke9x7C.')
            cur.execute('INSERT INTO usuarios (nombre, usuario, clave, correo) VALUES (%s, %s, %s, %s)', (nombre, usuario, clave, correo))
            self.mysql.commit()
            self.register = True
        self.mysql.close()