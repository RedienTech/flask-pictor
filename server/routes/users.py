from flask import Blueprint, request, flash, url_for, redirect, session
import sys
from flask import render_template
from models.users import User
import yagmail as yagmail

users = Blueprint('users', __name__, template_folder='templates')

@users.route('/perfil')
def Perfil():
    return render_template("perfil.html")

@users.route('/signin', methods=['GET', 'POST'])
def InicioSesion():
    if request.method == 'POST':
        loginUser = User()
        usuario = request.form['usuario']
        clave = request.form['clave']
        loginUser.IniciarSesion(usuario, clave)
        if loginUser.logged:
            session["username"] = loginUser.user
            return render_template("perfil.html")
        else:
            flash("Error en la combinacion de usuario y contraseña")
            return redirect(url_for('users.Perfil'))
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
            yag = yagmail.SMTP('pictorredsocial@gmail.com','misiontic2020')
            yag.send(to=email, subject='Activa tu cuenta', contents='Bienvenido usa el link para activar tu cuenta')
            return render_template('activarUsuario.html')
        else:
            for error in newUser.errors:
                flash(error)
            return render_template('registerUser.html')
    else:       
        return render_template("registerUser.html")

@users.route('/recover', methods=["GET", "POST"])
def RecuperarPassword():
    if request.method=="POST":
        return "Recuperando"
    else:
        return render_template('recoverPassword.html')