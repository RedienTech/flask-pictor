from flask_wtf import FlaskForm
from wtform import SubmitField, BooleanField, StringField, PasswordField
from wtform.validators import DataRequired

class FormInicio(FlaskForm):
    nombre = StringField('nombre', validators=[DataRequired()])
    usuario = StringField('usuario', validators=[DataRequired()])
    password = PasswordField('clave', validators=[DataRequired()])
    confirmPassword = PasswordField('cclave', validators=[DataRequired()])
    email = StringField('correo', validators=[DataRequired()])
    confirmEmail = StringField('ccorreo', validators=[DataRequired()])