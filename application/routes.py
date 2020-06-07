from application import app, mydb
from flask import render_template, request, session
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
        session['grades'] = request.form.getlist('grades')
        for i in request.form.getlist('grades'):
            print(i)
    return render_template("index.html", nav_index="active", myresult=myresult, kanjinumber=kanjinumber)

@app.route("/practice")
def practice():
    text = session.pop('grades', None)
    print(text)
    mycursor.execute("SELECT * FROM kanji_dict")
    mykanji = mycursor.fetchall()
    jkanji = json.dumps(mykanji)
    introkanji = mykanji[0]
    return render_template("practice.html", nav_practice="active", mykanji=jkanji, introkanji=introkanji)

@app.route("/quiz")
def quiz():
    kanji_id = math.floor(random.random()*240)
    grades = session.pop('grades', None)
    sql = "SELECT * FROM kanji_dict WHERE idkanji_dict = " + str(kanji_id)
    newsql = "SELECT * FROM kanji_dict WHERE "
    for i in grades:
        newsql += " grade = " + str(i)
        if i != grades[len(grades)-1]:
            newsql += " OR "
    print (newsql)
    mycursor.execute(sql)
    quiz_kanji = mycursor.fetchone()
    return render_template("quiz.html", nav_quiz="active", quiz_kanji=quiz_kanji)

@app.route("/about")
def about():
    return render_template("about.html", nav_about="active")