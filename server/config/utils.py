import re
from validate_email import validate_email
import bcrypt

pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{8,}$"
user_reguex = "^[a-zA-Z0-9_.-]+$"
image_reguex = "^(?i)\.(jpg|png|gif)$"
F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'

def comparePassword(clave, encrypted):
    clave = clave.encode(encoding='UTF-8',errors='strict')
    encrypted = encrypted.encode(encoding='UTF-8',errors='strict')
    return (bcrypt.checkpw(clave, encrypted))

def isEmailValid(email):
    is_valid = validate_email(email)

    return is_valid

def isValidImage(name):
    return re.search(image_reguex, name)

def isUsernameValid(user):
    if re.search(user_reguex, user):
        return True
    else:
        return False


def isPasswordValid(password):
    if re.search(pass_reguex, password):
        return True
    else:
        return False
