from config.db import getDb
from sqlite3 import Error

def sql_insert_imagenes(titulo, descripcion, ruta, tags, id_usuario):
    query="insert into imagenes (titulo, descripcion, ruta, tags, id_usuario) values ('"+titulo+"','"+descripcion+"','"+ruta+"','"+tags+"',"+id_usuario+");"       
    try:
        con = getDb()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

def sql_select_imagenes(id_usuario):
    query="select * from imagenes where id="+id_usuario+";"
    try:
        con = getDb()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        productos=cursorObj.fetchall()
        con.close()
        return productos
    except Error:
        print(Error)

def sql_edit_imagen(id, titulo, descripcion, ruta, tags, id_usuario):
    query ="update imagenes set titulo = '"+titulo+"', descripcion='"+ descripcion+"', ruta='"+ ruta+"', tags='"+ tags+"', id_usuario="+id_usuario+" where id ="+id+";"
    try:
        con = getDb()
        cursorObj=con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)

def sql_delete_imagen(id):
    query = "delete from imagenes where id="+id+";"
    try:
        con = getDb()
        cursorObj = con.cursor()
        cursorObj.execute(query)
        con.commit()
        con.close()
    except Error:
        print(Error)