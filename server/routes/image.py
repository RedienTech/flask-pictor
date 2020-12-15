from flask import Blueprint, request, redirect, url_for, current_app, flash, session, send_file
from datetime import date, datetime
import models.image as img
import os
from flask import render_template
import config.utils as utils
from werkzeug.utils import secure_filename



image = Blueprint('image', __name__, template_folder='templates')

@image.route('/download')
def ImagenDescargar():
    return render_template("imagen_descargar.html")

@image.route('/downloadImage', methods = ["GET", "POST"])
def downloadImage():
    return send_file("static/img/tour-eiffel-5210486_1920.jpg",as_attachment=True)

@image.route('/create', methods = ["GET", "POST"])
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


@image.route('/modify/<int:id>')
def ImagenModificar(id):
    image = img.sql_select_image(id)
    print(image)
    return render_template("imagen_modificar.html", image = image)


@image.route('/search', methods = ["POST"])
def BuscarImagen():
    key = request.form["tag"]
    return redirect(url_for('image.BuscarPorTag', busqueda = key))

@image.route('/search/<busqueda>', methods=["GET"])
def BuscarPorTag(busqueda):
    return render_template('search.html', key = busqueda)


