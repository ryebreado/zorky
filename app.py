from flask import Flask, render_template, request, make_response, redirect, url_for
from . import dungeon

app = Flask(__name__)


@app.route("/")
def home():
    name = request.cookies.get("userName")
    dungeon.gameState = dungeon.GameState()
    return render_template("index.html", 
                           title="Hello", 
                           name=name)


@app.route('/setname', methods=['POST', 'GET'])
def setname():
    if request.method == 'POST':
        name = request.form['nm']

        resp = make_response(redirect(url_for("home")))
        resp.set_cookie('userName', name)

        return resp

@app.route("/game", methods=['POST', 'GET'])
def game():
    if request.method == 'POST':
        command = request.form['cm']
        return runCommand(command)

    if not dungeon.gameState:
        return redirect("/")
    chamber = dungeon.gameState.dungeon.chambers[dungeon.gameState.currentCoords]
    number = chamber.number
    mapString = dungeon.gameState.createMapString(dungeon.gameState.currentCoords, 2)
    return render_template("chamber.html", 
                           activeNpcs = dungeon.gameState.activeNpcs,
                           mapString = mapString,
                           chamber=chamber,
                           number=number,
                           myself=dungeon.gameState.myself,
                           history = dungeon.gameState.history)

def runCommand(command):
    command = command.lower()
    if command == "west" or command == "w":
        dungeon.gameState.moveLeft()
    if command == "east" or command == "e":
        dungeon.gameState.moveRight()
    if command == "north" or command == "n":
        dungeon.gameState.moveUp()
    if command == "south" or command == "s":
        dungeon.gameState.moveDown()
    if command == "attack" or command == "a":
        dungeon.gameState.attack()
    return redirect(f"/game")
