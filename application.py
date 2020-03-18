import os

from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
# import psycopg2
import requests
import json
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import get_information_about_book, check_if_available, login_required
from tempfile import mkdtemp

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()

db.execute("""CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, hash VARCHAR(255) NOT NULL)""")
db.execute("""CREATE TABLE IF NOT EXISTS reviews (user_id INTEGER, book_isbn VARCHAR(255), review VARCHAR NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id), FOREIGN KEY (book_isbn) REFERENCES books (isbn))""")
db.commit()


@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")

@app.route("/form/login", methods = ["GET"])
def render_login():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    # Query database for username
    result = db.execute(f"SELECT * FROM users WHERE username = '{username}'")
    row = result.fetchone()
    
    # Ensure username exists and password is correct
    if row is None or not check_password_hash(row[2], password):
        return render_template ("apology.html", message = "Invalid username and/or password")

    # Remember which user has logged in
    session["user_id"] = row[0]

    # Redirect user to home page
    return redirect("/")


@app.route("/form/register", methods=["GET"])
def render_register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    if check_if_available(username) == False:
        return render_template("apology.html", message = "Username is already taken")
    password = request.form.get("password")
    password_confirm = request.form.get("password_confirm")
    # check if password matches
    if password_confirm != password:
            return render_template("apology.html", message = "Passwords don't match")
    db.execute(f"INSERT INTO users (username, hash) VALUES ('{username}', '{generate_password_hash(password)}')")
    db.commit()
    return redirect("/") 


@app.route("/form/search", methods=["GET"])
@login_required
def render_search():
    return render_template("search.html")

@app.route("/search", methods=["POST"])
@login_required
def search():
    keyword = request.form.get("search").capitalize()
    result = db.execute(f"SELECT * FROM books WHERE author LIKE '%{keyword}%' OR title LIKE '%{keyword}%' OR isbn LIKE '%{keyword}%'")
    rows = db.execute(f"SELECT count(*) FROM books WHERE author LIKE '%{keyword}%' OR title LIKE '%{keyword}%' OR isbn LIKE '%{keyword}%'")
    count = rows.fetchone()
    if count[0] < 1:
        return render_template("apology.html", message="Sorry, no books found")
    return render_template("search.html", rows=result)


@app.route("/book/<string:isbn>", methods=["GET"])
@login_required
def render_book(isbn):
    dict_of_book = get_information_about_book(isbn)
    reviews = db.execute(f"SELECT username, review, rating FROM reviews INNER JOIN users ON users.id = reviews.user_id WHERE book_isbn = '{isbn}'")
    reviews_count = db.execute(f"SELECT count(*) FROM reviews INNER JOIN users ON users.id = reviews.user_id WHERE book_isbn = '{isbn}'")
    count = reviews_count.fetchone()

    return render_template("book.html", book=dict_of_book, reviews=reviews, count = count)

@app.route("/book/<string:isbn>", methods=["POST"])
@login_required
def review(isbn):
        review = request.form.get("review")
        rating = request.form.get("rating")
        user_id=session["user_id"]
        rows = db.execute(f"SELECT count(*) FROM reviews WHERE user_id = {user_id} AND book_isbn = '{isbn}'")
        results = rows.fetchone()
        if results[0] != 0:
            return render_template("apology.html", message = "Sorry, you have already submited review about this book")
        db.execute(f"INSERT INTO reviews (user_id, book_isbn, review, rating) VALUES ({user_id}, '{isbn}', '{review}', {rating})")
        db.commit()
        return redirect(f"/book/{isbn}")

@app.route("/api/<string:isbn>", methods = ["GET"])
@login_required
def api(isbn):
    dict_of_book = get_information_about_book(isbn)
    if (len(dict_of_book)) != 6:
        return jsonify({"error": "Sorry, no books found"}), 404
    return jsonify(dict_of_book)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")