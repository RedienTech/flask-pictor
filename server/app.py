from flask import Flask, render_template, redirect, url_for, request, session, g
from config.utils import getCurrentUser
from config.db import getDb
from routes.users import users
from routes.image import image

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config["UPLOAD_FOLDER"] = ".\\files\images"
app.app_context()


@app.route('/')
def Index():
    return render_template("index.html")

@app.before_request
def before_request():
    print("Before Request")
    if "username" in session:
        g.user = getCurrentUser()
    else:
        g.user = None

with app.app_context():
    app.register_blueprint(image,url_prefix='/image')
    app.register_blueprint(users, url_prefix='/users')

if __name__ == "__main__":
    app.run(port = 3000, debug = True)
