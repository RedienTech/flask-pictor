from flask import Blueprint, request, flash, url_for, redirect, session, g, current_app
import config.utils as utils
from functools import wraps
import models.image as img
import bcrypt
import sys
from flask import render_template
from config.forms import FormRegistro, FormInicio, FormRecuperar
from models.users import User
import config.tokens as token
from config.utils import getCurrentUser
import yagmail as yagmail
from config.db import getDb
from random import choice

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
                yag.send(to=email, subject='Activa tu cuenta', contents='Bienvenido usa el link para activar tu cuenta: https://34.229.90.166/users/activate?token='+tok)
                session["username"] = usuario
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
    if request.method == "POST":
        if g.user["activo"] == 0:
            usuario = session["username"]
            email = request.form["correo"]
            newToken = token.createToken(usuario).decode()
            yag = yagmail.SMTP('pictorredsocial@gmail.com','misiontic2020')
            yag.send(to=email, subject='Activa tu cuenta', contents='Bienvenido usa el link para activar tu cuenta: https://34.229.90.166/users/activate?token='+newToken)
        else:
            flash("El usuario ya habia sido activado previamente")
            return redirect(url_for('users.Perfil'))
    else:
        if request.args.get("token") is not None:
            tok = request.args.get("token")
            payload = token.decodeToken(tok)
            activatingUser = User()
            if activatingUser.Activate(payload):
                session.pop("username", None)
                return render_template("usuarioActivado.html")
            else:
                return redirect(url_for("users.Perfil"))
        else:
            return render_template("activarUsuario.html")
            

@users.route('/recover', methods=["GET", "POST"])
def RecuperarPassword():
    if request.method=="POST":
        RecoverUser=User()        
        form = FormRecuperar(request.form)       
        if form.validate_on_submit():
            usuarioCorreo = form.usuarioCorreo.data
            lista = RecoverUser.recoverPassword(usuarioCorreo,usuarioCorreo)
            if lista is not None:
                longitud = 18
                valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                p = ""
                p = p.join([choice(valores) for i in range(longitud)])
                yag = yagmail.SMTP('pictorredsocial@gmail.com','misiontic2020')
                yag.send(to=lista[1], subject='Recupera tu clave', contents='Utiliza la clave ='+p)
                RecoverUser.recoverPasswordUpdate(p,lista[0])           
                return redirect(url_for('users.InicioSesion'))
            else:
                flash("Parece que el usuario no existe")
                return redirect(url_for("users.RecuperarPassword"))
        else:
            return "Icorrecto"  
    else:
        return render_template('recoverPassword.html',form=FormRecuperar())



@users.route('/logout', methods = ["GET"])
def LogOut():
    session.pop("username", None)
    return redirect(url_for('users.InicioSesion'))


