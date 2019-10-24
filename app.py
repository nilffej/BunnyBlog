# Ahmed Sultan, Jeff Lin, Leia Park [BunnyTruffles]
# SoftDev1 PD 9
# P00
# 2019-10-28

import cgi
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

app = Flask(__name__)
@app.route("/")
def occupyflaskst():
    return render_template('discover.html')

@app.route("/login")
def login():
    print(request)
    print(request.args)
    return render_template('login.html')

# @app.route("/auth")
# def authenticate():
#     print(app)                      # Prints out Flask app name
#     print(request)                  # Prints out Flask app web address
#     print(request.args)             # Prints out dictionary with form information
#     return render_template(         # Renders new page templates
#
#     )

if __name__ == "__main__":
  app.debug = True
  app.run()
