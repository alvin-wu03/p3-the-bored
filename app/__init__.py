# Team TheBored -- Alvin Wu, William Yin, Jeffrey Huang
# SoftDev
# P3 -- ArRESTed Development, JuSt in Time
# 2021-04-29


from flask import Flask, render_template, request, session, url_for, redirect, abort
from flask_bcrypt import Bcrypt
import bcrypt
import os
import time
import sqlite3
import uuid
from utils import utils
from api_keys import api_keys


APP_NAME = "The Board"
app = Flask(APP_NAME, template_folder="app/templates", static_folder="app/static")
bcrypt = Bcrypt(app)
app.secret_key = os.urandom(32)
DB_FILE = "app/the_board.db"
PRODUCTS = ["movie", "book", "recipe"]


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    if not request.form.get("username") or not request.form.get("password") or not request.form.get("confirm password"):
        return render_template("register.html", warning="Please fill out all fields.")
    elif len(request.form.get("password")) < 4:
        return render_template("register.html", warning="Password must be at least 4 characters long.")
    elif request.form.get("password") != request.form.get("confirm password"):
        return render_template("register.html", warning="Passwords do not match.")

    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cursor.execute("select * from users where username = ?", (request.form.get("username"),))
    user = cursor.fetchone()
    if user:
        db.close()
        return render_template("register.html", warning="Username is already taken.")

    password_hash = bcrypt.generate_password_hash(request.form.get("password"))
    user_id = str(uuid.uuid4())
    if request.form.get("description"):
        cursor.execute("insert into users (user_id, username, password, description) values (?, ?, ?, ?)", (user_id, request.form.get("username"), password_hash, request.form.get("description")))
    else:
        cursor.execute("insert into users (user_id, username, password) values (?, ?, ?)", (user_id, request.form.get("username"), password_hash))
    cursor.execute("select * from users where user_id = ?", (user_id,))
    user = cursor.fetchone()
    db.commit()
    db.close()

    session["user_id"] = user[1]
    session["username"] = user[2]
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        if session.get("user_id"):
            return redirect(url_for("index"))
        return render_template("login.html")

    if not request.form.get("username") or not request.form.get("password"):
        return render_template("login.html", warning="Please fill out all fields.")

    db = sqlite3.connect(DB_FILE)
    cursor = db.cursor()
    cursor.execute("select * from users where username = ?", (request.form.get("username"),))
    user = cursor.fetchone()
    db.close()
    if not user or not bcrypt.check_password_hash(user[3], request.form.get("password")):
        return render_template("login.html", warning="Incorrect username or password.")

    session["user_id"] = user[1]
    session["username"] = user[2]
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    if not session.get("user_id") or not session.get("username"):
        return redirect(url_for("login"))

    session.pop("user_id")
    session.pop("username")
    return redirect(url_for("index"))


@app.route("/")
@app.route("/index")
def index():
    api_data = {}
    if request.args.get("search_query") and request.args.get("category") in PRODUCTS:
        if request.args.get("category") == "movie":
            arg_mapping = {"t": request.args.get("search_query"), "apikey": api_keys.OMDB_KEY}
            api_data["movie"] = utils.call_api(arg_mapping, "http://www.omdbapi.com/")
        elif request.args.get("category") == "book":
            arg_mapping = {"title": request.args.get("search_query"), "api-key": api_keys.NYT_BOOKS_KEY}
            api_data["book"] = utils.call_api(arg_mapping, "https://api.nytimes.com/svc/books/v3/lists/best-sellers/history.json")
        elif request.args.get("category") == "recipe":
            arg_mapping = {"q": request.args.get("search_query"), "app_id": api_keys.EDAMAM_APP_ID, "app_key": api_keys.EDAMAM_APP_KEY}
            api_data["recipe"] = utils.call_api(arg_mapping, "https://api.edamam.com/search")


    logged_in = session.get("user_id") and session.get("username")
    if not request.args.get("category") in PRODUCTS:
        return render_template("index.html", category="", logged_in=logged_in)
    else:
        return render_template("index.html", category=request.args.get("category"), data=api_data[request.args.get("category")], logged_in=logged_in)


if __name__ == "__main__":
    app.debug = True
    app.run()
