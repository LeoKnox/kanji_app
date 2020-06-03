from application import app, mydb
from flask import render_template

mycursor = mydb.cursor()
mc = mydb.cursor()

@app.route("/")
@app.route("/index")
def index():
    mycursor.execute("SELECT * FROM kanji_dict")
    mycursor.fetchall()
    kanjinumber = mycursor.rowcount
    mycursor.execute("SELECT DISTINCT grade FROM kanji_dict")
    myresult = mycursor.fetchall()
    return render_template("index.html", nav_index="active", myresult=myresult, kanjinumber=kanjinumber)

@app.route("/practice")
def practice():
    mycursor.execute("SELECT * FROM kanji_dict")
    mykanji = mycursor.fetchall()
    return render_template("practice.html", nav_practice="active", mykanji=mykanji)