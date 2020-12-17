from flask import Blueprint, request, redirect, url_for, current_app, flash, session, send_file, g
from datetime import date, datetime
from config.forms import FormModificar
import models.image as img
import os
from flask import render_template
import config.utils as utils
from werkzeug.utils import secure_filename

image = Blueprint('image', __name__, template_folder='templates')

@image.route('/info')
def ImagenDescargar():
    id = request.args["img"]
    image = img.sql_select_image(id)
    usuario = utils.getUser(image[5])
    tags = image[3].split(',')
    image = {
        "id": image[0],
        "titulo": image[1],
        "tags": tags,
        "file": image[4],
        "descripcion": image[2],
        "user": usuario
    } 
    return render_template("imagen_descargar.html", image = image)

@image.route('/download/<int:id>', methods = ["GET", "POST"])
def downloadImage(id):
    image = img.sql_select_image(id)
    if image is not None:
        if g.user is not None and image[5] == g.user["id"]:
            imageName = image[4]
            return send_file(os.path.join("static\\files\images\\", imageName), as_attachment=True)
        elif image[6] == 0:
            imageName = image[4]
            return send_file(os.path.join("static\\files\images\\", imageName), as_attachment=True)
        else:
            flash("No tiene permiso para descargar esta imagen")
            return redirect(url_for('Index'))
    else: 
        flash('La imagen que esta intentando descargar no existe o ha sido eliminada')
        return redirect(url_for('Index'))

@image.route('/create/', methods = ["GET", "POST"])
def ImagenCrear():
    if request.method == "POST":
        chekPrivada = 'privada' in request.form
        privada = 1 if chekPrivada else 0
        usuario = session["username"]
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]
        tags = request.form["tags"]
        file = request.files["file"]
        filename = secure_filename(str(date.today()) + "-" + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + "-" + usuario + "-" + file.filename)
        ruta = os.path.join(os.getcwd() + "\server\static\\files\images", filename)
        file.save(ruta)
        img.sql_insert_imagenes(titulo, descripcion, ruta, filename, tags, utils.getCurrentUser().get("id"), privada)
        flash("Imagen guardada con exito!!")
        return redirect(url_for('users.Perfil'))
    else:
        return render_template("imagen_crear.html")


@image.route('/modify/<int:id>', methods=["GET", "POST"])
def ImagenModificar(id):
    if g.user is None:
        return redirect(url_for('users.InicioSesion'))
    if request.method == "POST":
        form = request.form
        chekPrivada = 'privada' in form
        privada = 1 if chekPrivada else 0
        titulo = form["titulo"]
        descripcion = form["descripcion"]
        tag = form["tags"]
        image = img.sql_select_image(id)
        if image[5] == g.user["id"]:
            img.sql_edit_imagen(id, titulo, descripcion, tag, privada)
            flash("Imagen Actualizada!!!")
            return redirect(url_for('users.Perfil'))
        else:
            flash("No tiene permiso para esta accion")
            return redirect(url_for('users.Perfil'))
    else:
        image = img.sql_select_image(id)
        return render_template("imagen_modificar.html", image = image) 

@image.route('/delete/<int:id>', methods=["GET"])   
def EliminarImagen(id):
    image = img.sql_select_image(id)
    if image is not None:
        if image[5] == g.user["id"]:
            img.sql_delete_imagen(id)
            flash("Imagen Eliminada!!")
            return redirect(url_for("users.Perfil"))
        else:
            flash("No tiene permiso sobre esta imagen")
            return redirect(url_for('users.Perfil'))
    else:
        flash("La imagen no existe o ha sido eliminada")
        return redirect(url_for('users.Perfil'))


@image.route('/search/', methods=["GET"])
def BuscarPorTag():
    busqueda = request.args["tag"]
    imagenes = img.buscarImagen(busqueda)
    print(imagenes)
    return render_template('search.html', key = busqueda, images = imagenes)


