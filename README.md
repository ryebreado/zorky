# Zorky

Zorky was created during the summer of 2023 as a summer project to help us learn Python, CSS, and HTML. 

The original plan was to create a game similar to [Zork](https://en.wikipedia.org/wiki/Zork), with the ability to type in commands, and fight monsters. It eventually evolved to become something more inspired off of DND and turn based games.

## What We Learned

* **Python** - We learned basic data structures such as lists and dictionaries. We also used classes with inheritance.
* **HTML** and **CSS** - We learned the basics of HTML and CSS, as well as how to combine the two skills to create an aesthetic webpage. We used mainly flexboxes to structure our webpage. 
* **Flask** - We used the flask webserver framework, incuding Jinja templates to generate HTML. 
* **HTTP** - learned basics of HTTP. Our server uses POST and GET, as well as using cookies to store data such as username. 
* **SQL** - Used SQL to create database to store the gamestate. Learned SELECT, INSERT, and UPDATE.

## TODO

We ran out of time to work on this during the summer, so this is very much unfinished. Here is a nonexhauustive list of things we would like to improve:
* Improve game mechanics
    * Add items (such as keys and weapons), more characters (bosses, more NPCs), more abilities.
    * Make combat more complex, such as by adding random aspects to the game (stats/combat).
    * Add multiplayer gamemode.
* Clean up code
    * Change variables to snake_case from camelCase.
    * Refactor code. For example, split files into more logical files (such as moving game_state out of dungeon.py into its own file).
    * We currently use pickle for encoding the gamestate in the database, we would like to use a more sensical schema.
    * More documentation.
* Graphics/style
    * Currently the monsters graphics are placeholder public domain images. We would like to create our own art (similar to the NPCs).
    * Add favicon.
    * Make map nicer than ASCII art.
    * Add background image.
    * Make command input box fit style better.
    * Make design responsive.

## Developer Instructions

To run this application:

```
flask --debug run
```

Before you run the server for the first time, you have to create the database by running

```
python init_db.py
```