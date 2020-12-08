from flask import Blueprint, request, redirect, url_for
import sys
from flask import render_template


image = Blueprint('image', __name__, template_folder='templates')

@image.route('/download/')
def ImagenDescargar():
    return render_template("imagen_descargar.html")

@image.route('/create/')
def ImagenCrear():
    return render_template("imagen_crear.html")

@image.route('/modify/')
def ImagenModificar():
    return render_template("imagen_modificar.html")

@image.route('/search', methods = ["POST"])
def BuscarImagen():
    key = request.form["tag"]
    return redirect(url_for('image.BuscarPorTag', busqueda = key))

@image.route('/search/<busqueda>', methods=["GET"])
def BuscarPorTag(busqueda):
    return render_template('search.html', key = busqueda)
