from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired

class FormRegistro(FlaskForm):
    nombre = StringField('nombre', validators=[DataRequired()])
    usuario = StringField('usuario', validators=[DataRequired()])
    password = PasswordField('clave', validators=[DataRequired()])
    confirmPassword = PasswordField('cclave', validators=[DataRequired()])
    email = StringField('correo', validators=[DataRequired()])
    confirmEmail = StringField('ccorreo', validators=[DataRequired()])

class FormInicio(FlaskForm):
    usuario = StringField('usuario', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])