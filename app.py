from flask import Flask, render_template, request, make_response, redirect, url_for
from . import dungeon
import pickle
import sqlite3

app = Flask(__name__)


@app.route("/")
def home():
    try:
        conn = get_db_connection()
        records = conn.execute('SELECT * FROM gamestate').fetchall()
        conn.close()
        for record in records:
            print(f"user: {record['username']}, content: {record['content']}")
    except sqlite3.OperationalError as error:
        print(f"Database does not exist. {error}")
        return f"Database does not exist. Make sure to run 'python init_db.py' before starting for the first time! Error message: {error}"

    name = request.cookies.get("userName")
    # dungeon.gameState = dungeon.GameState()
    return render_template("home.html",
                           title="Hello",
                           name=name)


@app.route("/reset")
def reset():
    # picklestring = pickle.dumps(dungeon.GameState())
    # print(f"Pickled {picklestring}!")
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
    
    recovered_gamestate = read_gamestate_from_db()
    if not recovered_gamestate:
        return redirect("/reset")

    if not recovered_gamestate.myself:
        return redirect("/gameover")

    print(recovered_gamestate)

    chamber = recovered_gamestate.dungeon.chambers[recovered_gamestate.currentCoords]
    number = chamber.number
    mapString = recovered_gamestate.createMapString(
        recovered_gamestate.currentCoords, 2)
    return render_template("room.html",
                           activeNpcs=recovered_gamestate.activeNpcs,
                           mapString=mapString,
                           chamber=chamber,
                           number=number,
                           myself=recovered_gamestate.myself,
                           history=recovered_gamestate.history)


@app.route("/gameover")
def gameover():
    return render_template("gameover.html")


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def write_gamestate_to_db(game_state: dungeon.GameState):
    """If a gamestate already exists, update the gamestate to the new value. If not, insert a new gamestate into the database."""
    recovered_gamestate = read_gamestate_from_db()
    if recovered_gamestate:
        update_gamestate_in_db(game_state)
    else:
        insert_gamestate_to_db(game_state)

def insert_gamestate_to_db(game_state: dungeon.GameState):
    picklestring = pickle.dumps(game_state)
    username = get_username()
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO gamestate (username, content) VALUES (?, ?)",
                (username, picklestring)
                )

    connection.commit()
    connection.close()

def update_gamestate_in_db(game_state: dungeon.GameState):
    picklestring = pickle.dumps(game_state)
    username = get_username()
    connection = sqlite3.connect('database.db')
    cur = connection.cursor()
    cur.execute("UPDATE gamestate SET content = ? WHERE username = ?",
                (picklestring, username)
                )

    connection.commit()
    connection.close()

def read_gamestate_from_db() -> dungeon.GameState:
    try:
        conn = get_db_connection()
        records = conn.execute(
            'SELECT * FROM gamestate WHERE username=?', (get_username(),)).fetchall()
        conn.close()
        for record in records:
            print(f"user: {record['username']}, content: {record['content']}")
            recovered_gamestate = pickle.loads(record["content"])
            return recovered_gamestate
        return None
    except sqlite3.OperationalError:
        return None


def get_username():
    name = request.cookies.get("userName")
    if not name:
        name = "HERO"
    return name


def runCommand(command):
    recovered_gamestate = read_gamestate_from_db()
    command = command.lower()
    if command == "west" or command == "w":
        recovered_gamestate.moveLeft()
    if command == "east" or command == "e":
        recovered_gamestate.moveRight()
    if command == "north" or command == "n":
        recovered_gamestate.moveUp()
    if command == "south" or command == "s":
        recovered_gamestate.moveDown()
    if command == "attack" or command == "a":
        recovered_gamestate.attack()
    write_gamestate_to_db(recovered_gamestate)
    return redirect(f"/game")
