import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    csv_file = open("books.csv")
    rows = csv.DictReader(csv_file)
    print(rows)
    for row in rows:
        book = Book(isbn=row["isbn"], title=row["title"], author=row["author"], year=row["year"])
        db.session.add(book)
        print(f'Added book: isbn: {row["isbn"]}, {row["title"]} by {row["author"]}, written in {row["year"]}')
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
