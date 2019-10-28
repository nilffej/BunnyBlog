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

@app.route("/login")
def login():
  # if user already logged in, redirects back to discover
  if 'user' in session:
    return redirect(url_for('root'))

  # checking to see if things were submitted
  if (request.args):
    if (bool(request.args["username"]) and bool(request.args["password"])):
      # setting request.args to variables to make life easier
      inpUser = request.args["username"]
      inpPass = request.args["password"]

      for row in userList:
        if inpUser == row[0]:
          if inpPass == row[1]:
            print("successful")
            session['user'] = inpUser;
            return(redirect(url_for("root")))
          else:
            print("fail!")
            return(redirect(url_for("login")))

    else:
      print("Login fields missing!")
      return(redirect(url_for("login")))

  return render_template("login.html")

@app.route("/register")

def register():
  # if user already logged in, redirects back to discover
  if 'user' in session:
    return redirect(url_for('root'))

  # checking to see if things were submitted
  if (request.args):
    if (bool(request.args["username"]) and bool(request.args["password"])):
      # setting request.args to variables to make life easier
      inpUser = request.args["username"]
      inpPass = request.args["password"]
      inpConf = request.args["confirmPass"]

      if(addUser(inpUser, inpPass, inpConf)):
         return redirect(url_for("login"))
      else:
        print("Fail!")
        return(redirect(url_for("register")))
    else:
      print('[ERROR] MISSING FIELDS.')
      # flash('Please make sure to fill all fields!')
  return render_template("register.html")

def addUser(user, pswd, conf):
  for row in userList:
        if user == row[0]:
          print("username already taken")
          return False
  if (pswd == conf):
    # SQLite3 is being weird with threading, so I've created a separate object
    with sqlite3.connect(DB_FILE) as connection:
      cur = connection.cursor()
      q = "INSERT INTO users VALUES('{}', '{}');".format(user, pswd)
      cur.execute(q)
      connection.commit()
    return True
  else:
    print("passwords don't match")
    return False

if __name__ == "__main__":
  app.debug = True
  app.run()

db.close()
