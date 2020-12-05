from flask import Flask, render_template, redirect, url_for, request
from routes.users import users
from routes.image import image

app = Flask(__name__)


@app.route('/')
def Index():
    return render_template("index.html")

@app.route('/perfil')
def Perfil():
    return render_template("perfil.html")

@app.route('/search')
def Search():
    return render_template("search.html")

app.register_blueprint(image,url_prefix='/image')
app.register_blueprint(users, url_prefix='/users')

if __name__ == "__main__":
    app.run(port = 3000, debug = True)
