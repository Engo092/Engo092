from flask import Flask, redirect, render_template, request, url_for
import json

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["CACHE_TYPE"] = "null"

# Initialises global variables
start = None
actstore = None
h = None
m = None
s = None
wish = None

# Redirects to main page
@app.route("/")
def red():
    return redirect(url_for("main"))

@app.route("/main", methods=["GET", "POST"])
def main():
    global start # Starts start variable
    if request.method == "POST": # Redirects URL for POST
        return redirect(url_for("rect"))
    if not start: # Displays main page if timer hasn't started
        return render_template("main.html")
    else: # If timer has started, display timer page
        return redirect(url_for("time"))


@app.route("/time", methods=["GET", "POST"])
def time():
    # Calls all global variables
    global actstore
    global start
    global h
    global m
    global s
    global wish

    if request.method == "POST": # Redirects URL for POST
        return redirect(url_for("redi"))

    if request.method == "GET":
        if start == True: # Checks if timer has started
            if wish == True: # Checks if there is wished time
                return render_template("time.html", activity=json.dumps(actstore), h=h, m=m, s=s, wish=wish)
            else: # Otherwise displays it normally
                return render_template("time.html", activity=json.dumps(actstore))
        else: # If timer hasn't started, redirects to main page
            return redirect(url_for("main"))

@app.route("/error", methods=["GET"])
def error(): # Pure error page since i couldn't make it work with javascript
    global start # Initializes global start variable
    if start == True: # If timer has started, redirects to timer page
        return redirect(url_for("time"))
    else: # Otherwise display error page
        return render_template("error.html")


# Next two routes are for fixing browser resending information when refreshing page
@app.route("/redi", methods=["POST"])
def redi():
    # Calls all global variables
    global actstore
    global start
    global h
    global m
    global s
    global wish

    if not request.form.get("activity") or request.form.get("activity").strip() == "": # Checks for valid activity
        return redirect(url_for("error"))

    if digitCheck(request.form.get("h")) == False: # Checks if h value is a valid digit
        return redirect(url_for("main"))

    if digitCheck(request.form.get("m")) == False: # Checks if m value is a valid digit
        return redirect(url_for("main"))

    if digitCheck(request.form.get("s")) == False: # Checks is s value is a valid digit
        return redirect(url_for("main"))

    actstore = request.form.get("activity").strip() # Strips activity of blank spaces
    start = True # Timer has started
    if request.form.get("h") or request.form.get("m") or request.form.get("s"): # Checks if there is any optional value
        h = zeroStrip(request.form.get("h")) # Strips h variable of unnecessary zeroes
        m = zeroStrip(request.form.get("m")) # Strips m variable of unnecessary zeroes
        s = zeroStrip(request.form.get("s")) # Strips s variable of unnecessary zeroes
        wish = True # There is a time wish
        if not h: # If there isn't a h value, initialize it as 0
            h = "0"
        if not m: # If there isn't a m value, initialize it as 0
            m = "0"
        if not s: # If there isn't a s value, initialize it as 0
            s = "0"
        if h == "0" and m == "0" and s == "0": # If all values are 0, it means that there isn't any wish at all
            wish = None
    return redirect(url_for("time")) # Redirects to timer route

@app.route("/rect", methods=["POST"])
def rect():
    # Calls all global variables
    global actstore
    global start
    global h
    global m
    global s
    global wish
    
    # Initializes all variables to none
    start = None
    actstore = None
    h = None
    m = None
    s = None
    wish = None
    return redirect(url_for("main")) # Redirects to main page route


def digitCheck(num):
    if num.isdigit() == False and num != "": # Checks for invalid non-integer characters for non-empty values
        return False

def zeroStrip(n): # Strips all unnecessary zeroes
    new = ""
    found = False
    for character in n:
        if character == "0" and found == False:
            pass
        else:
            new+=character
            found = True
    return new

if __name__ == "__main__":
    app.run(debug=True)