from flask import Flask, render_template, request, make_response, redirect, url_for
from . import dungeon
import pickle
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM gamestate').fetchall()
    conn.close()
    for post in posts:
        print(f"user: {post['username']}, content: {post['content']}")
    name = request.cookies.get("userName")
    dungeon.gameState = dungeon.GameState()
    return render_template("home.html",
                           title="Hello",
                           name=name)


@app.route("/reset")
def reset():
    picklestring = pickle.dumps(dungeon.GameState())
    print(f"Pickled {picklestring}!")
    write_gamestate_to_db(dungeon.GameState())
    return redirect("/")


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

    if not dungeon.gameState.myself:
        return redirect("/gameover")

    chamber = dungeon.gameState.dungeon.chambers[dungeon.gameState.currentCoords]
    number = chamber.number
    mapString = dungeon.gameState.createMapString(
        dungeon.gameState.currentCoords, 2)
    return render_template("room.html",
                           activeNpcs=dungeon.gameState.activeNpcs,
                           mapString=mapString,
                           chamber=chamber,
                           number=number,
                           myself=dungeon.gameState.myself,
                           history=dungeon.gameState.history)


@app.route("/gameover")
def gameover():
    return render_template("gameover.html")


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def write_gamestate_to_db(game_state: dungeon.GameState):
    picklestring = pickle.dumps(game_state)
    username = get_username()
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO gamestate (username, content) VALUES (?, ?)",
                (username, picklestring)
                )

    connection.commit()
    connection.close()

def get_username():
    name = request.cookies.get("userName")
    if not name:
        name = "HERO"
    return name


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
