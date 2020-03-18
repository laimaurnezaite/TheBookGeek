# Project 1

Web Programming with Python and JavaScript

# How to run program?
- export API_KEY
- export FLASK_APP=application.py 
- export FLASK_DEBUG=1
- export DATABASE_URL (postgres://spkjihodrgivbo:294af7e391fe62ee8e56cbd8d7cf3561061af319f9ee8b6a8230a203fa79426c@ec2-54-195-247-108.eu-west-1.compute.amazonaws.com:5432/d42brirmi57g69)
- source /Users/laima/Library/Caches/pypoetry/virtualenvs/project1-qoHIWOFQ-py3.8/bin/activate

# Imported packages
- import os
- from flask import Flask, session, render_template, request, redirect, jsonify
- from flask_session import Session
- import requests
- import json
- from werkzeug.security import check_password_hash, generate_password_hash
- from helpers import get_information_about_book, check_if_available, login_required
- from tempfile import mkdtemp
- from sqlalchemy import create_engine
- from sqlalchemy.orm import scoped_session, sessionmaker
- from functools import wraps
- import csv

# Files in project:
- static
    - images
        -  books.jpg (picture to use as background)
    - styles.css
- templates - templates for different routes
- application.py - code that connect to database, create tables, defines routes
- books.csv - book data
- helpers.py - file that contains helper functions for code
- import.py - file that imports data from book.csv to database
- requirements.txt - file that contains list of packages that are neccesarry for this program