# Team TheBored (Alvin Wu, William Yin, Jeffrey Huang)
# SoftDev
# P3 -- ArRESTed Development, JuSt in Time
# 2021-04-29

from flask import Flask,session            #facilitate flask webserving
from flask import render_template   #facilitate jinja templating
from flask import request, redirect           #facilitate form submission
from datetime import datetime
import os
import sqlite3   #enable control of an sqlite database

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/") #testing purposes
def renderlogin():
    return render_template("edit_review.html", oldtitle = "TITLE", oldreviewtext = "TEXT")

@app.route("/search") #tested search function to see if category and query could be accessed, the answer is yes
def search():
    print("THIS IS THE CATEGORY: " + request.args['category'])
    print("THIS IS THE SEARCH QUERY: " + request.args['searchquery'])
    return True

if __name__ == "__main__": #false if this file imported as module
    app.debug = True
    app.run()
