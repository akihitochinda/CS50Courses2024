import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)

        if not password:
            return apology("must provide password", 400)

        if not confirmation:
            return apology("must confirm password", 400)

        if password != confirmation:
            return apology("passwords do not match", 400)

        hash = generate_password_hash(password)

        try:
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("username already exists", 400)
        session["user_id"] = new_user

        return redirect("/")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    stocks = db.execute("SELECT symbol, SUM(shares) as totshares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING totshares > 0",
                        user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    total_value = cash
    grand_total = cash

    for stock in stocks:
        quote = lookup(stock["symbol"])
        # stock["name"] = quote["name"]
        stock["price"] = quote["price"]
        stock["value"] = quote["price"] * stock["totshares"]
        total_value += stock["value"]
        grand_total += stock["value"]

    return render_template("index.html", stocks=stocks, cash=cash, total_value=total_value, grand_total=grand_total)


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        quote = lookup(symbol.upper())

        if not symbol:
            return apology("invalid symbol", 400)
        if quote == None:
            return apology("symbol not found")

        return render_template("quote.html", quote=quote)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        if not symbol:
            return apology("invalid symbol")
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("invalid number of shares")

        quote = lookup(symbol.upper())
        if quote == None:
            return apology("symbol not found")

        user_id = session["user_id"]
        price = quote["price"]
        total_cost = int(shares) * price
        cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        if cash < total_cost:
            return apology("not enough cash")

        db.execute("UPDATE users SET cash = cash - :total_cost WHERE id = :user_id",
                   total_cost=total_cost, user_id=user_id)

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                   user_id=user_id, symbol=symbol, shares=shares, price=price)

        flash(f"Bought {shares} shares of {symbol} for {usd(total_cost)}!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]
    stocks = db.execute("SELECT symbol, SUM(shares) as totshares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING totshares > 0",
                        user_id)

    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        if not symbol:
            return apology("invalid symbol")
        elif not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("invalid number of shares")
        else:
            shares = int(shares)

        for stock in stocks:
            if stock["symbol"] == symbol:
                if stock["totshares"] < shares:
                    return apology("not enough shares")
                else:
                    quote = lookup(symbol)
                    if quote == None:
                        return apology("symbol not found")
                price = quote["price"]
                total_sale = shares * price

                db.execute("UPDATE users SET cash = cash + :total_sale WHERE id = :user_id",
                           total_sale=total_sale, user_id=user_id)

                db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)",
                           user_id=user_id, symbol=symbol, shares=(-1)*shares, price=price)

                flash(f"Sold {shares} shares of {symbol} for {usd(total_sale)}!")
                return redirect("/")

        return apology("symbol not found")

    else:
        return render_template("sell.html", stocks=stocks)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id = ?", user_id)
    return render_template("history.html", transactions=transactions_db)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """User can add cash"""
    if request.methods == "GET":
        return render_template("add.html")
    else:
        new_cash = int(request.method.get("new_cash"))

        if not new_cash:
            return apology("invalid value")

        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        uptd_cash = user_cash + new_cash

        db.execute("UPDATE users SET cash = ? WHERE id = ?", uptd_cash, user_id)

        return redirect("/")


@app.route("/settings")
@login_required
def settings():
    """Show settings"""
    # Query database
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    return render_template("settings.html", username=username[0]['username'])


@app.route("/passwordupdate", methods=["GET", "POST"])
@login_required
def passwordupdate():
    """Show settings"""

    if request.method == "POST":

        # Validate submission
        currentpassword = request.form.get("currentpassword")
        newpassword = request.form.get("newpassword")
        confirmation = request.form.get("confirmation")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Ensure password == confirmation
        if not (newpassword == confirmation):
            return apology("the passwords do not match", 400)

        # Ensure password not blank
        if currentpassword == "" or newpassword == "" or confirmation == "":
            return apology("input is blank", 400)

       # Ensure password is correct
        if not check_password_hash(rows[0]["hash"], currentpassword):
            return apology("invalid password", 403)
        else:
            hashcode = generate_password_hash(newpassword, method='pbkdf2:sha256', salt_length=8)
            db.execute("UPDATE users SET hash = ? WHERE id = ?", hashcode, session["user_id"])

        # Redirect user to settings
        return redirect("/settings")

    else:
        return render_template("passwordupdate.html")
