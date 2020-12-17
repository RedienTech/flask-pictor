from config.db import getDb
from sqlite3 import Error

def buscarImagen(key):
    try:
        key = '%'+key+'%'
        con = getDb()
        cur = con.cursor()
        cur.execute("SELECT * FROM imagenes WHERE titulo LIKE ? AND privada = 0 or tags LIKE ? AND privada = 0 or descripcion LIKE ? AND privada = 0", (key, key, key))
        result = cur.fetchall()
        return result
    except Error:
        print(Error)


def sql_insert_imagenes(titulo, descripcion, ruta, filename, tags, id_usuario, privada):     
    try:
        con = getDb()
        cursorObj = con.cursor()
        cursorObj.execute("INSERT INTO imagenes (titulo, descripcion, ruta, filename, tags, id_usuario, privada) VALUES (?,?,?,?,?,?,?);",(titulo,descripcion,ruta, filename, tags,str(id_usuario), privada))
        con.commit()
        con.close()     
    except Error:
        print(Error)

def sql_select_image(id):
    try:
        con = getDb()
        cur = con.cursor()
        cur.execute("SELECT id, titulo, descripcion, tags, filename, id_usuario, privada FROM imagenes WHERE id = ?", (id, ))
        image = cur.fetchone()
        return image
    except Error:
        print(Error)

def sql_select_imagenes(id_usuario):
    try:
        con = getDb()
        cursorObj = con.cursor()
        cursorObj.execute("SELECT * FROM imagenes WHERE id_usuario = ? ORDER BY fecha_creacion DESC;",(id_usuario,))
        imagenes = cursorObj.fetchall()
        con.close()
        return imagenes
    except Error:
        print(Error)

def sql_edit_imagen(id, titulo, descripcion, tags, privada):
    try:
        con = getDb()
        cursorObj=con.cursor()
        cursorObj.execute("UPDATE imagenes SET titulo = ?, descripcion= ?, tags= ?, privada = ? WHERE id = ?;",(titulo,descripcion,tags, privada, id))
        con.commit()
        con.close()
    except Error:
        print(Error)

def sql_delete_imagen(id):
    query = "DELETE FROM imagenes WHERE id="+str(id)+";"
    try:
        con = getDb()
        cursorObj = con.cursor()
        cursorObj.execute("DELETE FROM imagenes WHERE id=?;",(id,))
        con.commit()
        con.close()
    except Error:
        print(Error)