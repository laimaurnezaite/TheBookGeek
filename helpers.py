

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
    for row in rows:
        dict_of_books["review_count"] = row["books"][0]["work_ratings_count"]
        dict_of_books["average_score"] = row["books"][0]["average_rating"]

    return dict_of_books