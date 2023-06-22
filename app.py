from flask import Flask, render_template
from . import rooms

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route("/room/<name>")
def displayRoom(name):
    room = rooms.home[name]
    return room.description