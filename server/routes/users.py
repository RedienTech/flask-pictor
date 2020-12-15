from flask import Blueprint, request, flash, url_for, redirect, session, g, current_app
from functools import wraps
import sys
from flask import render_template
from config.forms import FormRegistro, FormInicio
from models.users import User
import config.tokens as token
from config.utils import getCurrentUser
import yagmail as yagmail
from config.db import getDb

users = Blueprint('users', __name__, template_folder='templates')

'''def login_required(func):
    @wraps(func)
    def required(*args):
        if g.user is not None:
            return func(*args)
        else:
            return redirect(url_for('users.InicioSesion'))
    return required()'''

@users.route('/perfil')
#@login_required
def Perfil():
    if g.user is None:
        return redirect(url_for('users.InicioSesion'))
    return render_template("perfil.html", usuario = g.user["nombre"])

@users.route('/signin', methods=['GET', 'POST'])
def InicioSesion():
    if request.method == "POST":
        form = FormInicio(request.form)
        if form.validate_on_submit():
            loginUser = User()
            usuario = form.usuario.data
            clave = form.password.data
            loginUser.IniciarSesion(usuario, clave)
            if loginUser.logged:
                session["username"] = usuario
                return redirect(url_for('users.Perfil'))
            else:
                print("Aqui")
                flash("Error en la combinacion de usuario y contraseña")
                return render_template("login.html")
    else:
        if g.user is not None:
            return redirect(url_for('Index'))
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
        if g.user is not None:
            return redirect(url_for('Index'))       
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

@users.route('/logout', methods = ["GET"])
def LogOut():
    session.pop("username", None)
    return redirect(url_for('users.InicioSesion'))

@users.before_request #antes de realziar cualquier peticion
def load_logged_in_user():
    user_id=session.get('username')

    if user_id is None:
        g.user = None
    else:
        g.user = getDb().execute('SELECT * FROM Usuarios WHERE usuario = ?',(user_id,)).fetchone()