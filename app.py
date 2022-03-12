import os

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# create table to house users with unique userid
# CREATE TABLE users(userid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);
# CREATE TABLE data(userid INTEGER NOT NULL, rank TEXT NOT NULL, name TEXT NOT NULL, threeLast REAL NOT NULL, cie TEXT NOT NULL, bat TEXT NOT NULL, sixN TEXT NOT NULL, sevenN TEXT NOT NULL, eightN TEXT NOT NULL,ninY TEXT NOT NULL, url TEXT NOT NULL);
# CREATE UNIQUE INDEX useridx ON users (userid);

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    rows2 = db.execute("SELECT * FROM data WHERE userid = ?", session["user_id"])
    if (len(rows2) != 0):
        return redirect("/send")

    return render_template("index.html")


@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    if request.method == "POST":
        userID = session["user_id"]
        hash_row = db.execute("SELECT hash FROM users WHERE userid = ?", userID)

        # Ensure passwords were submitted
        if not request.form.get("cpw") or not request.form.get("npw") or not request.form.get("conf"):
            return apology("Must provide passwords in every field and the two last must match", 403)

        # Ensure 2 new password match
        if request.form.get("npw") != request.form.get("conf"):
            return apology("New passwords must match", 403)

        # Ensure current password matches DB password
        if not check_password_hash(hash_row[0]["hash"], request.form.get("cpw")):
            return apology("Wrong current password", 403)

        # Insert NPW into DB replacing old hash
        db.execute("UPDATE users SET hash = ? WHERE userid = ?", generate_password_hash(request.form.get("npw")), userID)

        return render_template("user.html")  # some kind of alert to confirm changeing password
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("user.html")


@app.route("/send",methods=["GET","POST"])
@login_required
def send():
    
    userID = session["user_id"]  
    table_val=[]
    rows1 = db.execute("SELECT * FROM data WHERE userid = ?", userID)

    if (len(rows1) == 0):
        return render_template("make.html")     
    
    rank = rows1[0]["rank"]
    name = rows1[0]["name"]
    threeLast = rows1[0]["threeLast"]
    cie = rows1[0]["cie"]
    bat = rows1[0]["bat"]
    sixN = rows1[0]["sixN"]
    sevenN = rows1[0]["sevenN"]
    eightN = rows1[0]["eightN"]
    nineY = rows1[0]["nineY"]
    url = rows1[0]["url"]
    table_val=[rank,name,threeLast,cie,bat,sixN,sevenN,eightN,nineY,url]

        # Redirect user to make page
    return render_template("send.html",table_val=table_val)


@app.route("/make" ,methods=["GET","POST"])
@login_required
def make():
    if request.method == "POST":
        rank = request.form.get("rank")
        name = request.form.get("name")
        threeLast = request.form.get("threeLast")
        cie = request.form.get("cie")
        bat = request.form.get("bat")
        sixN = request.form.get("sixN")
        sevenN = request.form.get("sevenN")
        eightN = request.form.get("eightN")
        nineY = request.form.get("nineY")
        userID = session["user_id"]
        table_val=[]
        payload = "entry.1315296153="+threeLast+"&entry.1429378478="+rank+"&entry.1527757341="+name+"&entry.2077813938=&entry.1170687127="+cie+"&entry.1910594951="+bat+"&entry.1958299218="+sixN+"&entry.507671141="+sevenN+"&entry.1364729209="+eightN+"&entry.1837577196="+nineY
        url ="https://docs.google.com/forms/u/0/d/e/1FAIpQLSeeA0rt7uimVYglH7WEjl4fiPV6WSUT4mRqVftB2NZMXly72Q/formResponse?"+payload
        table_val=[rank,name,threeLast,cie,bat,sixN,sevenN,eightN,nineY,url]
        checkRows = db.execute("SELECT * FROM data WHERE userid = ?", session["user_id"])
        if len(checkRows) == 0:
            db.execute("INSERT INTO data (userid, rank, name, threeLast, cie, bat, sixN, sevenN, eightN, nineY, url) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",userID, rank, name, threeLast, cie, bat, sixN, sevenN, eightN, nineY, url)
        
        db.execute("UPDATE data SET userid=?, rank=?, name=? , threeLast=?, cie=?, bat=?, sixN=?, sevenN=?, eightN=?, nineY=?, url=?",userID, rank, name, threeLast, cie, bat, sixN, sevenN, eightN, nineY, url)

        return render_template("send.html", table_val=table_val)
    else:
        return render_template("make.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["userid"]
        

        table_val=[]

        rows1 = db.execute("SELECT * FROM data WHERE userid = ?", session["user_id"])

        if (len(rows1) == 0):
            return render_template("make.html")     
        

        rank = rows1[0]["rank"]
        name = rows1[0]["name"]
        threeLast = rows1[0]["threeLast"]
        cie = rows1[0]["cie"]
        bat = rows1[0]["bat"]
        sixN = rows1[0]["sixN"]
        sevenN = rows1[0]["sevenN"]
        eightN = rows1[0]["eightN"]
        nineY = rows1[0]["nineY"]
        url = rows1[0]["url"]
        table_val=[rank,name,threeLast,cie,bat,sixN,sevenN,eightN,nineY,url]

        # Redirect user to make page
        return render_template("send.html",table_val=table_val)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password must match", 400)

        # check if username is unique
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) >= 1:
            return apology("Username already in use", 400)

        # add username to db
        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", request.form.get("username"), generate_password_hash(request.form.get("password")))

        # Remember which user has logged in
        rows2 = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        session["user_id"] = rows2[0]["userid"]

        # Redirect user to home page
        return render_template("make.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")