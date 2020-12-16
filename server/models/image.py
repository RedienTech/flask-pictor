from config.db import getDb
from sqlite3 import Error

def sql_insert_imagenes(titulo, descripcion, ruta, tags, id_usuario):     
    try:
        con = getDb()
        cursorObj = con.cursor()
        cursorObj.execute("INSERT INTO imagenes (titulo, descripcion, ruta, tags, id_usuario) VALUES (?,?,?,?,?);",(titulo,descripcion,ruta,tags,str(id_usuario)))
        con.commit()
        con.close()     
    except Error:
        print(Error)

def sql_select_image(id):
    try:
        con = getDb()
        cur = con.cursor()
        cur.execute("SELECT id, titulo, descripcion, tags, filename, id_usuario FROM imagenes WHERE id = ?", (id, ))
        image = cur.fetchone()
        return image
    except Error:
        print(Error)

def sql_select_imagenes(id_usuario):
    try:
        con = getDb()
        cursorObj = con.cursor()
        cursorObj.execute("SELECT * FROM imagenes WHERE id_usuario = ? ;",(id_usuario,))
        imagenes = cursorObj.fetchall()
        con.close()
        return imagenes
    except Error:
        print(Error)

def sql_edit_imagen(id, titulo, descripcion, tags):
    query ="UPDATE imagenes SET titulo = '"+titulo+"', descripcion='"+ descripcion+ "', tags='"+ tags +"' WHERE id ="+str(id)+";"
    try:
        con = getDb()
        cursorObj=con.cursor()
        cursorObj.execute("UPDATE imagenes SET titulo = ?, descripcion= ?, tags= ?, privada = ? WHERE id = ?;",(titulo,descripcion,tags, id))
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