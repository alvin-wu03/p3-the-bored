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
db = sqlite3.connect("p3database.db")
c = db.cursor()
#c.execute("DROP TABLE IF EXISTS reviews") #for changing columns
c.execute("DROP TABLE IF EXISTS users") #for changing columns
c.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text, bibliography text, reviews text)""")
c.execute("""CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, product text, rating integer, review text, type text)""")
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
    return render_template('register.html')

#Registration for new user, stores user info into users db
@app.route("/register_auth", methods = ['GET', 'POST'])
def registerConfirming():
    db = sqlite3.connect("p3database.db")
    c1 = db.cursor()

    #gets all the data from the register.html form to check if they exist/match
    u = request.form['new_username']
    p = request.form['new_password_1']
    p1 = request.form['new_password_2']
    b = request.form['new_bibliography']

    #Gets a list of all the registered usernames to check later on
    usernames_list = []
    for x in c1.execute("SELECT username FROM users;"):
        usernames_list.append(x[0])

    if len(u.strip()) == 0:
        return render_template('register.html', error_type = "Please enter valid username, try again")
    elif len(p.strip()) == 0:
        return render_template('register.html', error_type = "Please enter valid password, try again")
    elif len(b.strip()) == 0:
        return render_template('register.html', error_type = "Please enter valid bibliography, try again")
    #Checks if the username exists
    elif u in usernames_list:
        return render_template('register.html', error_type = "Username already exists, try again")
    #Checks if the passwords match
    elif p != p1:
        return render_template('register.html', error_type = "Passwords do not match, try again")
    #If both pass, it adds the newly registered user and directs the user to the login page
    else:
        c1.execute("INSERT INTO users (username, password, bibliography) VALUES (?, ?, ?)", (u, p, b))
        db.commit()
        return render_template("login.html", error_type = "Please login with your new account")

#Checks credentials of login attempt
@app.route("/auth", methods = ['GET', 'POST']) # methods=['GET', 'POST']
def welcome():
    db = sqlite3.connect("p3database.db")
    c2 = db.cursor()
    username = request.form['username']
    password = request.form['password']

    u_list = []
    for x in c2.execute("SELECT username FROM users"):
        for y in x:
            u_list.append(y)
    p_list = []
    for a in c2.execute("SELECT password FROM users"):
        for b in a:
            p_list.append(b)

#    usersContributions = []      ; will be used for userReviews later
#    if username in u_list:
#        user_index = u_list.index(username)
#        for x in c2.execute("SELECT contributions FROM users"):
#            usersContributions.append(x[0])
#        user_conts = usersContributions[user_index].split("~")
#
#        if (len(user_conts) >= 1):
#            user_conts.pop()

    if username in u_list and password in p_list:
        session["user"] = username
        return render_template('home.html', user = username, message = "Your Login Has Been Successful! \(^-^)/")
    else:
        return render_template('login.html', error_type = "Invalid login attempt, please try again.")




@app.route("/") #testing purposes
def renderlogin():
    return render_template("edit_review.html", oldtitle = "TITLE", oldreviewtext = "TEXT")

@app.route("/search") #tested search function to see if category and query could be accessed, the answer is yes
def search():
    print("THIS IS THE CATEGORY: " + request.args['category'])
    print("THIS IS THE SEARCH QUERY: " + request.args['searchquery'])
    return True

#Displays login page and removes user from session
@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    session.pop("user", None) #removes the session
    return render_template('login.html')

if __name__ == "__main__": #false if this file imported as module
    app.debug = True
    app.run()
