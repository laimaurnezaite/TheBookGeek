import csv
import os

from flask import Flask, render_template, request
from flask_session import Session
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

def main():
    csv_file = open("books.csv")
    rows = csv.DictReader(csv_file)
    for row in rows:
        # print(row)
        db.execute("""CREATE TABLE IF NOT EXISTS books (isbn VARCHAR(255) NOT NULL PRIMARY KEY, title VARCHAR(255) NOT NULL, author VARCHAR(255) NOT NULL, year INTEGER NOT NULL)""")
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {"isbn":row['isbn'], "title":row["title"], "author":row["author"], "year":row["year"]})
        print(f'Added book: isbn: {row["isbn"]}, {row["title"]} by {row["author"]}, written in {row["year"]}')
    db.commit()
    print("added all books from csv file")

if __name__ == "__main__":
    with app.app_context():
        main()
