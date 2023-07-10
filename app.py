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
    
@app.route("/chamber/<number>/<direction>")
def moveToChamber(number, direction):
    if direction == "left":
        newChamber = dungeon.gameState.moveLeft()
    if direction == "right":
        newChamber = dungeon.gameState.moveRight()
    if direction == "up":
        newChamber = dungeon.gameState.moveUp()
    if direction == "down":
        newChamber = dungeon.gameState.moveDown()
    return redirect(f"/game")

@app.route("/chamber/<number>")
def displayChamber(number):
    mapString = dungeon.gameState.createMapString(dungeon.gameState.currentCoords, 2)
    return render_template("chamber.html", 
                           mapString = mapString,
                           number=number)

@app.route("/game")
def game():
    if not dungeon.gameState:
        return redirect("/")
    chamber = dungeon.gameState.dungeon.chambers[dungeon.gameState.currentCoords]
    number = chamber.number
    mapString = dungeon.gameState.createMapString(dungeon.gameState.currentCoords, 2)
    return render_template("chamber.html", 
                           activeNpcs = dungeon.gameState.activeNpcs,
                           mapString = mapString,
                           chamber=chamber,
                           number=number)
