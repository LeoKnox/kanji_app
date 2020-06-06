from flask import Flask
import mysql.connector

app = Flask(__name__)
app.secret_key = 'random_string'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="kanji_app_db"
)

from application import routes