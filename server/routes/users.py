from flask import Blueprint, request, flash, url_for, redirect, session, g, current_app
import config.utils as utils
from functools import wraps
import models.image as img
import bcrypt
import sys
from flask import render_template
from config.forms import FormRegistro, FormInicio
from models.users import User
import config.tokens as token
from config.utils import getCurrentUser
import yagmail as yagmail
from config.db import getDb

users = Blueprint('users', __name__, template_folder='templates')

def login_required(func):
    @wraps(func)
    def required(*args):
        with current_app.app_context():
            if g.user is not None:
                return func(*args)
            else:
                return redirect(url_for('users.InicioSesion'))
    return required()


@users.route('/perfil')
def Perfil():
    if g.user is None:
        return redirect(url_for('users.InicioSesion'))
    images = img.sql_select_imagenes(g.user["id"])
    return render_template("perfil.html", usuario = g.user["nombre"], images = images)

@users.route('/update', methods = ["GET", "POST"])
def UpdateUser():
    if request.method == "POST":
        id = g.user["id"]
        con = getDb()
        cur = con.cursor()
        cur.execute("SELECT usuario FROM usuarios WHERE id = ?;",(id,))
        existUser = cur.fetchall()
        if len(existUser) >= 1:
            clave = request.form["password"]
            cur.execute("SELECT clave FROM usuarios WHERE id = ?;",(id,))
            password = cur.fetchall()
            trueClave = password[0][0]
            if utils.comparePassword(clave, trueClave):
                newClave = request.form["newpassword"]
                cnewClave = request.form["cnewpassword"]
                if newClave == cnewClave and utils.isPasswordValid(newClave):
                    password = newClave.encode(encoding='UTF-8',errors='strict')
                    clave = bcrypt.hashpw(password, bcrypt.gensalt()).decode()
                    cur.execute("UPDATE usuarios SET clave = ? WHERE id = ?", (clave, id))
                    flash("Contraseña actualizada")
                    con.commit()
                    con.close()
                    return redirect(url_for("users.Perfil"))
                else:
                    flash("Las contraseñas no coinciden o son invalidas")
                    con.close()
                    return redirect(url_for('users.Perfil'))
            else:
                flash("La contraseña es incorrecta")
                con.close()
                return redirect(url_for('users.Perfil'))
        else:
            flash("Error actualizando el usuario")
            con.close()
            return redirect(url_for('users.Perfil'))       
    else:
        return render_template('actualizarDatos.html')

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
                flash("Error en la combinacion de usuario y contraseña")
                return redirect(url_for('users.InicioSesion'))
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
                yag.send(to=email, subject='Activa tu cuenta', contents='Bienvenido usa el link para activar tu cuenta: http://localhost:5000/users/activate?token='+tok)
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
