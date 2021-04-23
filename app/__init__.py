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

#Create db for user and story information
db = sqlite3.connect("p0database.db")
c = db.cursor()
#c.execute("DROP TABLE IF EXISTS stories") #for changing columns
#c.execute("DROP TABLE IF EXISTS users") #for changing columns
c.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text, biography text, reviews text)""")
c.execute("""CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, product text, rating nteger, review text, type text)""")
db.commit()

app = Flask(__name__)
app.secret_key = os.urandom(24)

#Checks if user is in session
@app.route("/", methods = ['GET', 'POST']) #methods=['GET', 'POST']
def disp_loginpage():
    if "user" in session:
        return render_template('home.html', user = session["user"])
    else:
        return render_template('login.html')

#Routes user to registration page
@app.route("/register", methods = ['GET', 'POST'])
def register():
    return render_template('signup.html')

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
