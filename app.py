from flask import Flask, render_template, request, make_response, redirect, url_for
from . import rooms

app = Flask(__name__)


@app.route("/")
def home():
    name = request.cookies.get("userName")
    return render_template("index.html", 
                           title="Hello", 
                           name=name)


@app.route("/room/<name>")
def displayRoom(name):
    room = rooms.home[name]
    return render_template("room.html", 
                           description=room.description,
                           paths=room.paths,
                           title=name)


@app.route('/setname', methods=['POST', 'GET'])
def setname():
    if request.method == 'POST':
        name = request.form['nm']

        resp = make_response(redirect(url_for("home")))
        resp.set_cookie('userName', name)

        return resp
