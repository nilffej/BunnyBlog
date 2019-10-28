# Ahmed Sultan, Jeff Lin, Leia Park [BunnyTruffles]
# SoftDev1 pd 9
# p00
# 2019-10-28

import cgi
import sqlite3
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from os import urandom

app = Flask(__name__)

app.secret_key = urandom(32)
usr = "rando"

DB_FILE = "bunnyblog.db"

db = sqlite3.connect(DB_FILE)   # open if file exists, otherwise create
c = db.cursor()                 # facilitate db ops

get = db.execute('SELECT username, password FROM users;')
userList = get.fetchall()

foo = db.execute('SELECT title, username, date, content FROM posts;')
entryList = foo.fetchall()

@app.route("/")
def root():
    return render_template('entrydisplay.html',
    title = "Discover", heading = "Discover",
    entries = entryList, postNum = range(len(entryList)),
    users = userList, userNum = range(len(userList)))

@app.route("/userpage")
def userpage():
    for user in userList:
        if request.args["username"] == user[0]:
            userentries = []
            for entry in entryList:
                if entry[1] == request.args["username"]:
                    userentries.append(entry)
            return render_template("entrydisplay.html",
            title = "Profile - {}".format(request.args["username"]), heading = request.args["username"],
            entries = userentries, postNum = range(len(userentries)),
            users = userList, userNum = range(len(userList)))
    return redirect(url_for("root"))

@app.route("/profile")
def profile():
    return render_template('profile.html',
    title = "Discover", heading = "Discover",
    entries = entryList, postNum = range(len(entryList)),
    users = userList, userNum = range(len(userList)))

@app.route("/addentry")
def addentry():
    print(request.args)
    dict = {}
    for item in request.args:
        if not request.args[item]:
            return render_template('profile.html',
            title = "Discover", heading = "Discover",
            entries = entryList, postNum = range(len(entryList)),
            users = userList, userNum = range(len(userList)),
            msg = "All fields must be filled.")
    c.execute("INSERT INTO posts VALUES ('jeff',{},{},{})".format(
        request.args["entrydate"], request.args["entrytitle"], request.args["entrytext"]))
    db.commit()
    db.close()
    return redirect(url_for("profile"))

@app.route("/login", methods=["GET"])
def login(msg=""):
    usrCheck = False
    pswrdCheck = False
    if request.args:
        # Checks for all inputs to be filled
        if not bool(request.args["username"]) or not bool(request.args["password"]):
            msg = "Login fields missing"
        else:
            for row in userList:
                if request.args["username"] == row[0]:
                    usrCheck = True
                    if request.args["password"] == row[1]:
                        pswrdCheck = True
            if usrCheck and pswrdCheck:
                session["usr"] = request.args["username"]
                return redirect(url_for("profile"))
            else:
                msg = "Username or Password is incorrect"
    return render_template("login.html", msg=msg)

@app.route("/register", methods=["GET"])
def register(msg=""):
    usrCheck = False
    print(request.args)
    if request.args:
        # Checks for all inputs to be filled
        if not bool(request.args["username"]) or not bool(request.args["password"]):
            msg = "Fill in all the information"
        else:
            for row in userList:
                if request.args["username"] == row[0]:
                    msg = "username is already taken"
                else:
                    usrCheck = True
        if usrCheck:
            if request.args["password"] == request.args["confirmPass"]:
                insert = "INSERT INTO users VALUES ('{}', '{}', '{}');".format(
                    request.args["username"], request.args["password"], '/' + request.args["username"])
                print(insert)
                c.execute(insert)
                db.commit()
                db.close()
                return redirect(url_for("login"))
            else:
                msg = "passwords do not match"
    return render_template("register.html", msg=msg)

if __name__ == "__main__":
    app.debug = True
    app.run()
