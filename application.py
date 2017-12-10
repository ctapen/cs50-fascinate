from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta

from helpers import apology, login_required, star_rating

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///fascinate.db")

# Show index homepage, displaying the fascinating content, with ability to rate said content


@app.route("/", methods=["GET", "POST"])
def index():
    """Shows homepage"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ratings
        # Once a rating star clicked
        if 'star_rating' in request.form:
            star_rating()  # from helpers.py

        else:
            # Redirects
            return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Enter number of entries want to display on index page
        nbr_of_entries_display = 4

        # Pull data on fascinating entries to display on page
        transactions_newest_limited = db.execute("SELECT e.*, round(ratings.avg_rating, 2) as avg_rating, tags_horizontal FROM entries e "
                                                 + "LEFT JOIN (SELECT auto_nbr_entries, avg(rating) as avg_rating FROM ratings GROUP BY auto_nbr_entries) ratings "
                                                 + "ON ratings.auto_nbr_entries = e.entry_nbr "
                                                 + "LEFT JOIN tags_horizontal on tags_horizontal.entry_nbr = e.entry_nbr "
                                                 + "ORDER by entry_nbr DESC LIMIT :nbr_of_entries_display", nbr_of_entries_display=nbr_of_entries_display)

        # Return html page with data to pass through
        return render_template("index.html", transactions=transactions_newest_limited)


# Show full fascinating information (unlike index's limited display), with ability to filter content on tags
@app.route("/fascinate", methods=["GET", "POST"])
@login_required
def fascinate():
    """Show full fascinating content"""

    # Tags
    # Pull tranactions by entry_nbr or by avg_rating
    transactions_newest = db.execute("SELECT e.*, round(ratings.avg_rating, 2) as avg_rating, tags_horizontal FROM entries e "
                                     + "LEFT JOIN (SELECT auto_nbr_entries, avg(rating) as avg_rating FROM ratings GROUP BY auto_nbr_entries) ratings "
                                     + "ON ratings.auto_nbr_entries = e.entry_nbr "
                                     + "LEFT JOIN tags_horizontal on tags_horizontal.entry_nbr = e.entry_nbr "
                                     + "ORDER by entry_nbr DESC")

    transactions_most_popular = db.execute("SELECT e.*, round(ratings.avg_rating, 2) as avg_rating, tags_horizontal FROM entries e "
                                           + "LEFT JOIN (SELECT auto_nbr_entries, avg(rating) as avg_rating FROM ratings GROUP BY auto_nbr_entries) ratings "
                                           + "ON ratings.auto_nbr_entries = e.entry_nbr "
                                           + "LEFT JOIN tags_horizontal on tags_horizontal.entry_nbr = e.entry_nbr "
                                           + "ORDER by avg_rating DESC")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ratings
        # Once a rating star clicked
        if 'star_rating' in request.form:
            star_rating()  # from helpers.py

        # Page filter
        # Enables to order the entries on the page (say by newest, or on technology tags)
        if 'page_display' in request.form:
            # If want to pull content for specific tags (e.g., "#US")
            transactions_tags = db.execute("SELECT DISTINCT e.*, round(ratings.avg_rating, 2) as avg_rating, tags_horizontal FROM entries e "
                                           + "LEFT JOIN (SELECT auto_nbr_entries, avg(rating) as avg_rating FROM ratings GROUP BY auto_nbr_entries) ratings "
                                           + "ON ratings.auto_nbr_entries = e.entry_nbr "
                                           + "LEFT JOIN tags_horizontal on tags_horizontal.entry_nbr = e.entry_nbr "
                                           + "INNER JOIN (SELECT tags.entry_nbr, tags_ref.tag FROM tags INNER JOIN tags_ref ON tags_ref.auto_nbr_tags_ref = tags.auto_nbr_tags_ref WHERE tag = :tag) tag "
                                           + "ON tag.entry_nbr = e.entry_nbr "
                                           + "ORDER by entry_nbr DESC", tag=request.form['page_display'])  # request.form['page_display'] stores the tag

            if request.form['page_display'] == "newest":
                transactions = transactions_newest
            elif request.form['page_display'] == "most_popular":
                transactions = transactions_most_popular
            # for tag-specific display (for tag buttons laid out in html)
            elif request.form['page_display']:
                transactions = transactions_tags

            # Renders the page with extended index information and ability to filter content, per the index_p2.html page (versus index.html page with limited entries displayed and no filtering)
            return render_template("index_p2.html", transactions=transactions)

        else:
            # Redirects
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # Return html page with data to pass through
        # index_p2.html page contains all entries and page filtering (versus index.html page with limited entries displayed and no filtering)
        return render_template("index_p2.html", transactions=transactions_newest)


# Recommend new fascinating content to share (for Fascinate administrators to review for posting)
@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    """ Enable others to recommend fascinating content """
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Error Handling
        if not request.form.get("title"):
            return apology("please provide a title", 403)

        elif not request.form.get("description_1"):
            return apology("please provide at least one fascinating line", 403)

        elif not request.form.get("source_1_link") or not request.form.get("source_1_link"):
            return apology("please provide at least one info source", 403)

        # Store to database recommendations table
        db.execute("INSERT INTO recommendations (title, description_1, description_2, description_3, image_link, image_source, image_alt, source_1_link, source_1_name, source_2_link, source_2_name, source_3_link, source_3_name, review_status, create_datetime, update_datetime, auto_nbr_users, anything_else, validity_check)" +
                   "VALUES (:title, :description_1, :description_2, :description_3, :image_link, :image_source, :image_alt, :source_1_link, :source_1_name, :source_2_link, :source_2_name, :source_3_link, :source_3_name, :review_status, :create_datetime, :update_datetime, :auto_nbr_users, :anything_else, :validity_check)",
                   title=request.form.get("title"),
                   description_1=request.form.get("description_1"),
                   description_2=request.form.get("description_2"),
                   description_3=request.form.get("description_3"),
                   image_link=request.form.get("image_link"),
                   image_source=request.form.get("image_source"),
                   image_alt=request.form.get("image_alt"),
                   source_1_link=request.form.get("source_1_link"),
                   source_1_name=request.form.get("source_1_name"),
                   source_2_link=request.form.get("source_2_link"),
                   source_2_name=request.form.get("source_2_name"),
                   source_3_link=request.form.get("source_3_link"),
                   source_3_name=request.form.get("source_3_name"),
                   review_status="Unreviewed",
                   create_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                   # ^ is 5 hrs fast b/c of some default timezone
                   update_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                   # ^ is 5 hrs fast b/c of some default timezone
                   auto_nbr_users=session["user_id"],
                   anything_else=request.form.get("anything_else"),
                   validity_check=request.form.get("validity_check")
                   )

        # Redirects to fascinating content entries
        return redirect("/fascinate")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # If logged in, go to recommend page, otherwise to login
        if session:
            return render_template("recommend.html")
        else:
            return render_template("login.html")

# Let user submit a comment on an entry's validity


@app.route("/validate", methods=["GET", "POST"])
def validate():
    """ Enable user to question an entry's validity for administrator to review """
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Error Handling
        if not request.form.get("reason_questionable"):
            return apology("please provide a reason for why questionable", 403)

        # # Store to database recommendations table
        db.execute("INSERT INTO validate (entry_nbr, title, reason_questionable, source_counter_1, source_counter_2, anything_else, " +
                   " create_datetime, auto_nbr_users) VALUES (:entry_nbr, :title, :reason_questionable, :source_counter_1, " +
                   ":source_counter_2, :anything_else, :create_datetime, :auto_nbr_users)",
                   entry_nbr=request.form.get("entry_nbr"),
                   title=request.form.get("title"),
                   reason_questionable=request.form.get("reason_questionable"),
                   source_counter_1=request.form.get("source_counter_1"),
                   source_counter_2=request.form.get("source_counter_2"),
                   anything_else=request.form.get("anything_else"),
                   create_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                   # ^ is 5 hrs fast b/c of some default timezone,
                   auto_nbr_users=session["user_id"]
                   )

        # Redirects to fascinating content entries
        return redirect("/fascinate")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        # If logged in, go to validate page, otherwise to login
        if session:
            return render_template("validate.html")
        else:
            return render_template("login.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if request.form['action'] == 'Login':

            # Ensure username was submitted
            if not request.form.get("email"):
                return apology("must provide email address", 403)

            # Ensure password was submitted
            elif not request.form.get("password"):
                return apology("must provide password", 403)

            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE email_address = :email_address",
                              email_address=request.form.get("email"))

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], request.form.get("password")):
                return apology("invalid username and/or password", 403)

            # Remember which user has logged in
            session["user_id"] = rows[0]["auto_nbr_users"]

            # Redirect user to home page
            return redirect("/fascinate")

        elif request.form['action'] == 'Register':
            return redirect("/register")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        if request.form['action'] == 'Register':

            # Store to variable username, password, password confirmation
            email_address = request.form.get("email")
            password = request.form.get("password")
            password_conf = request.form.get("confirmation")

            # Make sure fields are not left blank; if they are, apologize "Missing ____"
            if not email_address:
                # ref: https://stackoverflow.com/questions/9573244/most-elegant-way-to-check-if-the-string-is-empty-in-python
                return apology("Missing email address!")
            if not password:
                return apology("Missing password!")
            if not password_conf:
                return apology("Missing password confirmation!")
            # TF said to do separately for customized error handling to each problem situation

            # Make sure password and password confirmed match, else apologize
            if password != password_conf:
                return apology("Password mismatch")

            # Store user in database
            # Usernames are a unique field in the database
            result = db.execute("INSERT INTO users (email_address, password_hash) VALUES(:email_address, :password_hash)",
                                email_address=email_address, password_hash=generate_password_hash(
                                    password)
                                )

            if not result:
                return apology("Sorry, not unique entry")

            # Log user in by storing their ID number within the session user ID
            session["user_id"] = result

            # Redirect user to next page
            return redirect("/fascinate")

        elif request.form['action'] == 'Login':
            return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
