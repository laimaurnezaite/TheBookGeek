import os
import requests
from flask import redirect, session, render_template
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/form/login")
        return f(*args, **kwargs)
    return decorated_function
    
def get_information_about_book(isbn):
    dict_of_books = {}
    books = db.execute(f"SELECT * FROM books WHERE isbn = '{isbn}'")
    for book in books:
        dict_of_books["title"] = book[1]
        dict_of_books["author"] = book[2]
        dict_of_books["year"] = book[3]
        dict_of_books["isbn"] = book[0]

    api_key=os.getenv("API_KEY")
    rows = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": api_key, "isbns": isbn}).json()
    dict_of_books["review_count"] = rows["books"][0]["work_ratings_count"]
    dict_of_books["average_score"] = rows["books"][0]["average_rating"]
    
    return dict_of_books

def check_if_available(username):
    unavailable = db.execute(f"SELECT COUNT (username) FROM users WHERE username = '{username}'")
    result = unavailable.fetchone()
    if result[0] != 0:
        return False