import csv
import urllib.request

from cs50 import SQL
from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime, timedelta

db = SQL("sqlite:///fascinate.db")


def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def star_rating():
    """ Use stars to rate content """

    # Pull star_rating, which is concatenation from html button tag of rating & _ & entry_nbr, e.g. 5_3 for 5 star on 3rd fascinate entry
    star_rating = request.form['star_rating']

    # Parse components (because couldn't find other ways to get request.form elements other than input name and get out value, so decided to concatenate then parse as workaround to get all info needed for ratings!!)
    # + Convert each element to int
    (rating, entry_nbr) = [int(s) for s in star_rating.split("_")]
    # ref: https://stackoverflow.com/questions/5749195/how-can-i-split-and-parse-a-string-in-python, https://stackoverflow.com/questions/1574678/efficient-way-to-convert-strings-from-split-function-to-ints-in-python

    # Insert rating into database's ratings table
    db.execute("INSERT INTO ratings (rating, auto_nbr_entries, auto_nbr_user, rated_datetime)" +
               "VALUES (:rating, :auto_nbr_entries, NULL, :rated_datetime)",
               rating=rating,
               auto_nbr_entries=entry_nbr,
               rated_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
               # ^ is 5 hrs fast b/c of some default timezone
               )

    return "Thanks"
