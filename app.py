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

get = c.execute('SELECT username, password FROM users;')
userList = get.fetchall()

@app.route("/")
def root():
    with sqlite3.connect(DB_FILE) as connection:
        cur = connection.cursor()
        foo = cur.execute('SELECT title, username, date, content FROM posts;')
        entryList = foo.fetchall()
        entryList.reverse()
    return render_template('entrydisplay.html',
    title = "Discover", heading = "Discover",
    entries = entryList, postNum = range(len(entryList)),
    users = userList, userNum = range(len(userList)), sessionstatus = "user" in session)

@app.route("/userpage")
def userpage():
    with sqlite3.connect(DB_FILE) as connection:
        cur = connection.cursor()
        foo = cur.execute('SELECT title, username, date, content FROM posts;')
        entryList = foo.fetchall()
        entryList.reverse()
    for user in userList:
        if request.args["username"] == user[0]:
            if request.args["username"] == session["user"]:
                return redirect(url_for("profile"))
            userentries = []
            for entry in entryList:
                if entry[1] == request.args["username"]:
                    userentries.append(entry)
            return render_template("entrydisplay.html",
            title = "Profile - {}".format(request.args["username"]), heading = request.args["username"],
            entries = userentries, postNum = range(len(userentries)),
            users = userList, userNum = range(len(userList)), sessionstatus = "user" in session)
    return redirect(url_for("root"))

@app.route("/profile")
def profile():
    with sqlite3.connect(DB_FILE) as connection:
        cur = connection.cursor()
        foo = cur.execute('SELECT title, username, date, content FROM posts;')
        entryList = foo.fetchall()
        entryList.reverse()
    userentries = []
    for entry in entryList:
        if entry[1] == session['user']:
            userentries.append(entry)
    return render_template("profile.html",
    title = "Profile - {}".format(session["user"]), heading = session["user"],
    entries = userentries, postNum = range(len(userentries)),
    users = userList, userNum = range(len(userList)), sessionstatus = "user" in session)

@app.route("/profile/<USERNAME>")
def profile2(USERNAME):
  if 'user' in session:
    if (USERNAME == session["user"]):
        return redirect(url_for("profile"))
  
  with sqlite3.connect(DB_FILE) as connection:
    cur = connection.cursor()
    q = "SELECT title, username, date, content FROM posts;"
    foo = cur.execute(q)
    entryList = foo.fetchall()
  userentries = []
  for entry in entryList:
    if entry[1] == USERNAME:
      userentries.append(entry)
  return render_template("entrydisplay.html",
                         title="Profile - {}".format(USERNAME), heading=USERNAME,
                         entries=userentries, postNum=range(len(userentries)),
                         users=userList, userNum=range(len(userList)), sessionstatus="user" in session)


@app.route("/addentry")
def addentry():
    print(request.args)
    dict = {}
    for item in request.args:
        if not request.args[item]:
            with sqlite3.connect(DB_FILE) as connection:
                cur = connection.cursor()
                foo = cur.execute('SELECT title, username, date, content FROM posts;')
                entryList = foo.fetchall()
                entryList.reverse()
            return render_template('profile.html',
            title = "Discover", heading = "Discover",
            entries = entryList, postNum = range(len(entryList)),
            users = userList, userNum = range(len(userList)),
            msg = "All fields must be filled.")
    with sqlite3.connect(DB_FILE) as connection:
        cur = connection.cursor()
        cur.execute("INSERT INTO posts VALUES ('{}','{}','{}','{}')".format(session["user"],
            request.args["entrydate"], request.args["entrytitle"], request.args["entrytext"]))
        connection.commit()
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

      with sqlite3.connect(DB_FILE) as connection:
        cur = connection.cursor()
        q = 'SELECT username, password FROM users;'
        foo = cur.execute(q)
        userList = foo.fetchall()
        for row in userList:
          if inpUser == row[0]:
            if inpPass == row[1]:
              session['user'] = inpUser
              return(redirect(url_for("root")))
            else:
              flash('Login credentials were incorrect. Please try again.')
              return(redirect(url_for("login")))

    else:
      flash('Please make sure to fill all fields!')
      return(redirect(url_for("login")))

  return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for("root"))

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
        flash('Success! Please login.')
        return redirect(url_for("login"))
      else:
        return(redirect(url_for("register")))
    else:
      print('[ERROR] MISSING FIELDS.')
      flash('Please make sure to fill all fields!')
  return render_template("register.html")

def addUser(user, pswd, conf):
  for row in userList:
        if user == row[0]:
          flash('Username already taken. Please try again.')
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
    flash('Passwords do not match. Please try again.')
    return False

if __name__ == "__main__":
  app.debug = True
  app.run()

db.close()
