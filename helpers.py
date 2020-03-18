import os
import psycopg2
import requests
from flask import redirect, session
from functools import wraps


conn = psycopg2.connect("host=ec2-54-195-247-108.eu-west-1.compute.amazonaws.com dbname=d42brirmi57g69 user=spkjihodrgivbo password=294af7e391fe62ee8e56cbd8d7cf3561061af319f9ee8b6a8230a203fa79426c")
cur = conn.cursor()

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
    cur.execute(f"SELECT * FROM books WHERE isbn = '{isbn}'")
    books = cur.fetchall()
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
    cur.execute(f"SELECT username FROM users WHERE username = '{username}'")
    unavailable = cur.fetchall()
    if unavailable != []:
        return False