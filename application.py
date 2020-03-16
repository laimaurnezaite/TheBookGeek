import os

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)


conn = psycopg2.connect("host=ec2-54-195-247-108.eu-west-1.compute.amazonaws.com dbname=d42brirmi57g69 user=spkjihodrgivbo password=294af7e391fe62ee8e56cbd8d7cf3561061af319f9ee8b6a8230a203fa79426c")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS books (isbn VARCHAR(255) NOT NULL PRIMARY KEY, title VARCHAR(255) NOT NULL, author VARCHAR(255) NOT NULL, year INTEGER NOT NULL)""")
cur.execute("""CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, hash VARCHAR(255) NOT NULL)""")
cur.execute("""CREATE TABLE IF NOT EXISTS reviews (user_id INTEGER, book_isbn VARCHAR(255), review VARCHAR NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id), FOREIGN KEY (book_isbn) REFERENCES books (isbn))""")
conn.commit()

# all = cur.fetchall()
# for al in all:
#     print(al)

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# # Configure session to use filesystem
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"

# db = SQLAlchemy()
# # db.init_app(app)

# Session(app)

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

# # commit the changes
# db.session.commit()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form/search", methods=["GET"])
def render_search():
    return render_template("search.html")

@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("search").capitalize()
    cur.execute(f"SELECT * FROM books WHERE author LIKE '%{keyword}%' OR title LIKE '%{keyword}%' OR isbn LIKE '%{keyword}%'")
    rows = cur.fetchall()
    if len(rows) == 0:
        return render_template("apology.html", message="Sorry, no books found")
    return render_template("search.html", rows=rows)

@app.route("/book/<string:isbn>", methods=["GET"])
def render_book(isbn):
    if request.method == "GET":
        cur.execute(f"SELECT * FROM books WHERE isbn = '{isbn}'")
        book = cur.fetchall()
        cur.execute(f"SELECT username, review, rating FROM reviews_test2 INNER JOIN users_test ON users_test.id = reviews_test2.user_id WHERE book_isbn = '{isbn}'")
        reviews = cur.fetchall()
        return render_template("book.html", book=book, reviews=reviews)

@app.route("/book/<string:isbn>", methods=["POST"])
def review(isbn):
        review = request.form.get("review")
        rating = request.form.get("rating")
        user_id=2
        cur.execute(f"SELECT * FROM reviews_test2 WHERE user_id = {user_id} AND book_isbn = '{isbn}'")
        results = cur.fetchall()
        print(results)
        if results != []:
            return render_template("apology.html", message = "You have already submited review about this book")
        if review == []:
            cur.execute(f"INSERT INTO reviews_test2 (user_id, book_isbn, rating) VALUES ({user_id}, '{isbn}', {rating})")
        else:
            cur.execute(f"INSERT INTO reviews_test2 (user_id, book_isbn, review, rating) VALUES ({user_id}, '{isbn}', '{review}', {rating})")
        conn.commit()
        return redirect(f"/book/{isbn}")

