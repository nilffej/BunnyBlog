# Ahmed Sultan, Jeff Lin, Leia Park [BunnyTruffles]
# SoftDev1 PD 9
# P00
# 2019-10-28


import sqlite3   #enable control of an sqlite database
from flask import Flask, session, redirect, url_for, render_template, request
from os import urandom

app = Flask(__name__)

app.secret_key = urandom(32)
usr = "rando"

###### users database setup
DB_FILE="people.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops

retrieve = """
     SELECT username, password
     FROM users
"""
get = db.execute(retrieve)
userList = get.fetchall()

###### internal flask organs
@app.route("/")
def root():
  if "usr" in session:
    return redirect(url_for("myBlog"))
  return redirect(url_for("login"))

@app.route("/login", methods = ["GET"])
def login(msg = ""):
  usrCheck = False
  pswrdCheck = False
  if request.args:
    if not bool(request.args["usrname"]) or not bool(request.args["password"]): # Checks for all inputs to be filled
      msg = "Fill in all the information"
    else:
      for row in userList:
          if request.args["username"] == row[0]:
               usrCheck = True
               if request.args["password"] == row[1]:
                    pswrdCheck = True
    if usrCheck and pswrdCheck:
      session["usr"] = request.args["username"]
      return redirect(url_for("myBlog"))
    else:
      msg = "Username or Password is incorrect"
  return render_template("login.html", msg = msg)

@app.route("/register", methods = ["GET"])
def register(msg = ""):
  usrCheck = False
  if request.args:
     if not bool(request.args["usrname"]) or not bool(request.args["password"]): # Checks for all inputs to be filled
       msg = "Fill in all the information"
     else:
       for row in userList:
            if request.args["username"] == row[0]:
                 msg = "username is already taken"
            else:
                 usrCheck = True
     if usrCheck:
       if request.args["password"] == request.args["confirmPass"]:
            insert = "INSERT INTO users VALUES ('{}', {});".format(request.args["username"], request.args["password"])
            c.execute(insert)
            return redirect(url_for("login"))
       else:
            msg = "passwords do not match"
  return render_template("register.html", msg = msg)


if __name__ == "__main__":
  app.debug = True
  app.run()
