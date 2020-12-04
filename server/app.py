from flask import Flask, render_template, redirect, url_for, request
from routes.users import users

app = Flask(__name__)


@app.route('/')
def Index():
    return render_template("index.html")


app.register_blueprint(users, url_prefix='/users')

if __name__ == "__main__":
    app.run(port = 3000, debug = True)
