from application import app, mydb
from flask import render_template, request
import json, random, math

mycursor = mydb.cursor()
mc = mydb.cursor()

@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    mycursor.execute("SELECT * FROM kanji_dict")
    mycursor.fetchall()
    kanjinumber = mycursor.rowcount
    mycursor.execute("SELECT DISTINCT grade FROM kanji_dict")
    myresult = mycursor.fetchall()
    if request.method == "POST":
        print("------> posted")
    return render_template("index.html", nav_index="active", myresult=myresult, kanjinumber=kanjinumber)

@app.route("/practice")
def practice():
    mycursor.execute("SELECT * FROM kanji_dict")
    mykanji = mycursor.fetchall()
    jkanji = json.dumps(mykanji)
    introkanji = mykanji[0]
    return render_template("practice.html", nav_practice="active", mykanji=jkanji, introkanji=introkanji)

@app.route("/quiz")
def quiz():
    kanji_id = math.floor(random.random()*240)
    sql = "SELECT * FROM kanji_dict WHERE idkanji_dict = " + str(kanji_id)
    mycursor.execute(sql)
    quiz_kanji = mycursor.fetchone()
    print(quiz_kanji)
    return render_template("quiz.html", nav_quiz="active", quiz_kanji=quiz_kanji)