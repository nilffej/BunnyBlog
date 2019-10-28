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
from flask import flash
from os import urandom

app = Flask(__name__)

app.secret_key = urandom(32)

DB_FILE = "bunnyblog.db"

db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
c = db.cursor()               # facilitate db ops

retrieve = 'SELECT username, password FROM users;'
get = db.execute(retrieve)
userList = get.fetchall()

foo = db.execute('SELECT title, username, date, content FROM posts;')
entryList = foo.fetchall()

@app.route("/")
def root():
  print(userList)
  print(entryList)
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


@app.route("/register")
def register():
  # if user already logged in, redirects back to discover
  if 'user' in session:
    return redirect(url_for('root'))

  # if things have been submitted...
  if request.args:
    if not bool(request.args["username"]) or not bool(request.args["password"]):
      flash('Please make sure to fill all fields!')
    else:
      for row in userList:
        if request.args["username"] == row[0]:
          flash('Username is already taken! Try again.')
          return redirect(url_for('register'))
        else:
          if request.args["password"] == request.args["confirmPass"]:
            q = "INSERT INTO users VALUES('{}', '{}');".format(request.args["username"], request.args["password"])
            print(q)
            c.execute(q)
            return redirect(url_for("login"))
          else:
            flash('Passwords do not match! Try again.')
          
  return render_template("register.html")

if __name__ == "__main__":
  app.debug = True
  app.run()

db.commit()
db.close()
