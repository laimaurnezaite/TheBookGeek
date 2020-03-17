import os

from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import requests
import json


from helpers import get_information_about_book, check_if_available
from werkzeug import generate_password_hash

app = Flask(__name__)


conn = psycopg2.connect("host=ec2-54-195-247-108.eu-west-1.compute.amazonaws.com dbname=d42brirmi57g69 user=spkjihodrgivbo password=294af7e391fe62ee8e56cbd8d7cf3561061af319f9ee8b6a8230a203fa79426c")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS books (isbn VARCHAR(255) NOT NULL PRIMARY KEY, title VARCHAR(255) NOT NULL, author VARCHAR(255) NOT NULL, year INTEGER NOT NULL)""")
cur.execute("""CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, hash VARCHAR(255) NOT NULL)""")
cur.execute("""CREATE TABLE IF NOT EXISTS reviews (user_id INTEGER, book_isbn VARCHAR(255), review VARCHAR NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id), FOREIGN KEY (book_isbn) REFERENCES books (isbn))""")
conn.commit()

@app.route("/")
def index():
    return render_template("index.html")

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
    cur.execute(f"INSERT INTO users (username, hash) VALUES ('{username}', '{generate_password_hash(password)}')")
    conn.commit()
    return redirect("/") 

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
    dict_of_book = get_information_about_book(isbn)
    cur.execute(f"SELECT username, review, rating FROM reviews INNER JOIN users ON users_test.id = reviews.user_id WHERE book_isbn = '{isbn}'")
    reviews = cur.fetchall()

    return render_template("book.html", book=dict_of_book, reviews=reviews)

@app.route("/book/<string:isbn>", methods=["POST"])
def review(isbn):
        review = request.form.get("review")
        rating = request.form.get("rating")
        user_id=2
        cur.execute(f"SELECT * FROM reviews WHERE user_id = {user_id} AND book_isbn = '{isbn}'")
        results = cur.fetchall()
        print(results)
        if results != []:
            return render_template("apology.html", message = "Sorry, you have already submited review about this book")
        if review == []:
            cur.execute(f"INSERT INTO reviews (user_id, book_isbn, rating) VALUES ({user_id}, '{isbn}', {rating})")
        else:
            cur.execute(f"INSERT INTO reviews (user_id, book_isbn, review, rating) VALUES ({user_id}, '{isbn}', '{review}', {rating})")
        conn.commit()
        return redirect(f"/book/{isbn}")

@app.route("/api/<string:isbn>", methods = ["GET"])
def api(isbn):
    dict_of_book = get_information_about_book(isbn)
    print(type(dict_of_book))
    if (len(dict_of_book)) != 6:
        return jsonify({"error": "Sorry, no books found"}), 404
    return jsonify(dict_of_book)
