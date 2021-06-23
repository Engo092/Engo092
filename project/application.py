from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL
from datetime import datetime

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

start = None
actstore = None

@app.route("/")
def red():
    return redirect(url_for("main"))

@app.route("/main", methods=["GET", "POST"])
def main():
    global start
    if request.method == "POST":
        start = None
    if not start:
        return render_template("main.html")
    else:
        return redirect(url_for("time"))


@app.route("/time", methods=["GET", "POST"])
def time():
    global actstore
    global start
    if request.method == "POST":
        if start == True:
            start = None
            return redirect(url_for("main"))
        else:
            if not request.form.get("activity"):
                return redirect("/error")
            activity = request.form.get("activity")
            actstore = activity
            start = True
            if request.form.get("h"):
                h = request.form.get("h")
                m = request.form.get("m")
                s = request.form.get("s")
                return render_template("time.html", activity=activity, h=h, m=m, s=s, wish=True)
            else:
                return render_template("time.html", activity=activity)
        if request.method == "GET":
            if start == True:
                return render_template("time.html", activity=actstore)
        else:
            return redirect(url_for("main"))
    if request.method == "GET":
        if start == True:
            return render_template("time.html", activity=actstore)
        else:
            return redirect(url_for("main"))

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")