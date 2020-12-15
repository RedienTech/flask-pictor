import jwt as jwt
import datetime

secret = "dlasdfuieuhaskjdhfaseusnedu"

def createToken(user):
    expire = str(datetime.datetime.utcnow() + datetime.timedelta(days=1))
    payload = {
        "user": user,
        "expire": expire
    }
    print(payload)
    return jwt.encode(payload, secret, algorithm = "HS256")

def decodeToken(token):
    return jwt.decode(token, secret, algorithms = ['HS256'])

