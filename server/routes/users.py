from flask import Blueprint, request
import sys
from flask import render_template
from models.users import User

users = Blueprint('users', __name__, template_folder='templates')

@users.route('/signin')
def InicioSesion():
    return render_template("login.html")

@users.route('/signup', methods=["GET", "POST"])
def SignUp():
    if request.method == "POST":
        name = request.form["name"]
        usuario = request.form["user"]
        clave = request.form["password"]
        cclave = request.form["cpassword"]
        cemail = request.form["cemail"]
        email = request.form["email"]
        newUser = User()
        newUser.Registrar(name, usuario, clave, cclave, cemail, email)
        if newUser.register:
            return 'Registrado'
        else:
            return "No Registrado"
    else:       
        return render_template("registerUser.html")