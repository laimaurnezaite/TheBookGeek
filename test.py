import os
import requests

isbn = '0060852577'
# api_key=os.getenv("DATABASE_URL")
# res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": api_key, "isbns": isbn})
# print(res.json())

# response = {'books': [{
#     'id': 6433752, 
#     'isbn': '0060852577', 
#     'isbn13': '9780060852573', 
#     'ratings_count': 50990, 
#     'reviews_count': 87859, 
#     'text_reviews_count': 6964, 
#     'work_ratings_count': 56496, 
#     'work_reviews_count': 98041, 
#     'work_text_reviews_count': 7625, 
#     'average_rating': '3.79'
#     }]
# }
# print(response["books"][0]["average_rating"])


# response = {"title": "The Bone Bed", "author": "Patricia Cornwell", "year": 2012, "isbn": "0399157565", "review_count": 20433, "average_score": "3.68"}
# print(len(response))

response = [(1, 'test1', 'pbkdf2:sha256:150000$91StbfaR$4b300d4cfde03d6145435657559d81fe0cb14ec5189d5bb3a5495ab80b98e7e1')]
print(response[0][2])