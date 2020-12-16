from flask import Blueprint, request, redirect, url_for, current_app, flash, session, send_file, g
from datetime import date, datetime
from config.forms import FormModificar
import models.image as img
import os
from flask import render_template
import config.utils as utils
from werkzeug.utils import secure_filename



image = Blueprint('image', __name__, template_folder='templates')

@image.route('/download')
def ImagenDescargar():
    return render_template("imagen_descargar.html")

@image.route('/download/<int:id>', methods = ["GET", "POST"])
def downloadImage(id):
    image = img.sql_select_image(id)
    if image is not None:
        imageName = image[4]
        return send_file(os.path.join("static\\files\images\\", imageName), as_attachment=True)
    return send_file("static/img/tour-eiffel-5210486_1920.jpg",as_attachment=True)

@image.route('/create/', methods = ["GET", "POST"])
def ImagenCrear():
    if request.method == "POST":
        usuario = session["username"]
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]
        tags = request.form["tags"]
        file = request.files["file"]
        filename = secure_filename(str(date.today()) + "-" + str(datetime.now().hour) + str(datetime.now().minute) + str(datetime.now().second) + "-" + usuario + "-" + file.filename)
        ruta = os.path.join(os.getcwd() + "\server\static\\files\images", filename)
        file.save(ruta)
        img.sql_insert_imagenes(titulo, descripcion, ruta, filename, tags, utils.getCurrentUser().get("id"))
        return redirect(url_for('users.Perfil'))
    else:
        return render_template("imagen_crear.html")


@image.route('/modify/<int:id>', methods=["GET", "POST"])
def ImagenModificar(id):
    if request.method == "POST":
        form = request.form
        titulo = form["titulo"]
        descripcion = form["descripcion"]
        tag = form["tags"]
        image = img.sql_select_image(id)
        if image[5] == g.user["id"]:
            img.sql_edit_imagen(id, titulo, descripcion, tag)
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

@image.route('/search/', methods = ["POST"])
def BuscarImagen():
    key = request.form["tag"]
    return redirect(url_for('image.BuscarPorTag', busqueda = key))

@image.route('/search/<busqueda>', methods=["GET"])
def BuscarPorTag(busqueda):
    return render_template('search.html', key = busqueda)


