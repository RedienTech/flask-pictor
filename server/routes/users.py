from flask import Blueprint, request, flash, url_for, redirect, session
import sys
from flask import render_template
from config.forms import FormRegistro, FormInicio
from models.users import User
import config.tokens as token
import yagmail as yagmail

users = Blueprint('users', __name__, template_folder='templates')

@users.route('/perfil')
def Perfil():
    return render_template("perfil.html", usuario = "Alex Morgan")

@users.route('/signin', methods=['GET', 'POST'])
def InicioSesion():
    if request.method == 'POST':
        form = FormInicio(request.form)
        if form.validate_on_submit():
            loginUser = User()
            usuario = form.usuario.data
            clave = form.password.data
            loginUser.IniciarSesion(usuario, clave)
            if loginUser.logged:
                session["username"] = loginUser.user
                return render_template("perfil.html", usuario = session["username"])
            else:
                flash("Error en la combinacion de usuario y contraseña")
                return render_template("login.html")
    return render_template("login.html", form = FormInicio())

@users.route('/signup', methods=["GET", "POST"])
def SignUp():
    if request.method == "POST":
        form = FormRegistro(request.form)
        if form.validate_on_submit():
            name = form.nombre.data
            usuario = form.usuario.data
            clave = form.password.data
            cclave = form.confirmPassword.data
            cemail = form.email.data
            email = form.confirmEmail.data
            newUser = User()
            newUser.Registrar(name, usuario, clave, cclave, cemail, email)
            if newUser.register:
                tok = token.createToken(usuario).decode()
                yag = yagmail.SMTP('pictorredsocial@gmail.com','misiontic2020')
                yag.send(to=email, subject='Activa tu cuenta', contents='Bienvenido usa el link para activar tu cuenta: http://localhost:3000/users/activate?token='+tok)
                return render_template('activarUsuario.html')
            else:
                for error in newUser.errors:
                    flash(error)
                return render_template('registerUser.html', form = FormRegistro())
    else:       
        return render_template("registerUser.html", form = FormRegistro())

@users.route('/activate', methods=['GET'])
def ActivarUsuario():
    tok = request.args.get("token")
    payload = token.decodeToken(tok)
    activatingUser = User()
    if activatingUser.Activate(payload):
        return render_template("usuarioActivado.html")
    else:
        return("El link ha expirado o es invalido")

@users.route('/recover', methods=["GET", "POST"])
def RecuperarPassword():
    if request.method=="POST":
        return "Recuperando"
    else:
        return render_template('recoverPassword.html')