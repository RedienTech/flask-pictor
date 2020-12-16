from config.db import getDb
from sqlite3 import Error

def sql_insert_imagenes(titulo, descripcion, ruta, filename, tags, id_usuario):
    query="INSERT INTO imagenes (titulo, descripcion, ruta, filename, tags, id_usuario) VALUES ('"+titulo+"','"+descripcion+"','"+ruta+"','"+filename+"','"+tags+"',"+str(id_usuario)+");"       
    try:
        con = getDb()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

def sql_select_image(id):
    try:
        con = getDb()
        cur = con.cursor()
        cur.execute("SELECT id, titulo, descripcion, tags, filename, id_usuario FROM imagenes WHERE id = %s" % id)
        image = cur.fetchone()
        return image
    except Error:
        print(Error)

def sql_select_imagenes(id_usuario):
    query="SELECT * FROM imagenes WHERE id_usuario = "+str(id_usuario) +";"
    print(query)
    try:
        con = getDb()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        imagenes=cursorObj.fetchall()
        con.close()
        return imagenes
    except Error:
        print(Error)

def sql_edit_imagen(id, titulo, descripcion, tags):
    query ="UPDATE imagenes SET titulo = '"+titulo+"', descripcion='"+ descripcion+ "', tags='"+ tags +"' WHERE id ="+str(id)+";"
    try:
        con = getDb()
        cursorObj=con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

def sql_delete_imagen(id):
    query = "DELETE FROM imagenes WHERE id="+str(id)+";"
    try:
        con = getDb()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)