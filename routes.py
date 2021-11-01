from application import app, mydb
from flask import render_template, redirect, request, session
#from flask_mysqldb import MySQL
#from mysqlconn import connectToMySQL
import json, random, math

mycursor = mydb.cursor(buffered=True)
mc = mydb.cursor()

@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    sql = "SELECT DISTINCT grade, COUNT(*) AS total FROM kanji_app_db.kanji_dict GROUP BY grade"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    kanjinumber = sum(i[1] for i in myresult)
    if request.method == 'POST':
        session['grades'] = request.form.getlist('grades')
    return render_template("index.html", nav_index="active", myresult=myresult, kanjinumber=kanjinumber)

@app.route("/practice",methods=["GET", "POST"])
@app.route("/practice/<kanji_num>")
def practice(kanji_num = 0):
    db_test = session['database']
    if 'grades' in session:
        grades = session['grades']
    else:
        grades=[1]
    if db_test == 'kanji':
        b = "SELECT * FROM kanji_app_db.kanji_dict WHERE "
    else:
        b = "SELECT idkanji_dict, kanji, strokes, meaning, pronounciation, reading, grade FROM my_kanji mk JOIN kanji_dict kd ON mk.kanji_dict_id = kd.idkanji_dict WHERE "
    for i in grades:
        b += "grade = " + str(i) + " OR "
    b = b[:-3]  #deletes extra "OR" from end of query
    mycursor.execute(b)
    mykanji = mycursor.fetchall()
    jkanji = json.dumps(mykanji)
    print("*********")
    print(kanij_num)
    introkanji = mykanji[int(kanji_num)]
    return render_template("practice.html", nav_practice="active", mykanji=jkanji, introkanji=introkanji)

@app.route("/quiz")
@app.route("/quiz/<timer>")
def quiz(timer=7):
    if 'grades' in session and session['grades']!=[]:
        grades = session['grades']
    else:
        grades=[1]
    print (grades)
    newsql = "SELECT * FROM kanji_dict WHERE "
    for i in grades:
        newsql += " grade = " + str(i)
        if i != grades[len(grades)-1]:
            newsql += " OR "
    x = newsql.replace("*", "count(*)")
    mycursor.execute(x)
    quiz_kanji = mycursor.fetchone()
    kanji_id = math.floor(random.random()*quiz_kanji[0])
    sql = "SELECT * FROM kanji_dict WHERE idkanji_dict = " + str(kanji_id)
    mycursor.execute(sql)
    quiz_kanji = mycursor.fetchone()
    return render_template("quiz.html", nav_quiz="active", quiz_kanji=quiz_kanji, timer=timer)

@app.route("/about")
def about():
    return render_template("about.html", nav_about="active")

@app.route("/remember_kanji", methods=["POST"])
def remember_kanji():
    data = {
        'kanji_num': request.form["kanji_number"]
    }
    print(data['kanji_num'])
    kdata=request.form["kanji_number"]
    mk = ("INSERT INTO my_kanji (kanji_dict_id) VALUES (%s)" %(kdata))
    mycursor.execute(mk)
    mydb.commit()
    return redirect("/practice/" + data['kanji_num'])

@app.route("/my_kanji")
def my_kanji():
    sql = "SELECT my_kanji.id, kanji_dict.meaning, kanji_dict.kanji, kanji_dict.reading, kanji_dict.grade FROM my_kanji INNER JOIN kanji_dict ON my_kanji.kanji_dict_id=kanji_dict.idKanji_dict"
    mycursor.execute(sql)
    my_kanji = mycursor.fetchall()
    return render_template("my_kanji.html", nav_my_kanji="active", my_kanji = my_kanji)

@app.route("/my_kanji_delete/<kanji_id>")
def my_kanji_delete(kanji_id):
    sql = ("DELETE FROM my_kanji WHERE id = (%s)" %(kanji_id))
    mycursor.execute(sql, int(kanji_id))
    mydb.commit()
    return redirect("/my_kanji")

@app.route("/change_db", methods=["POST"])
def change_db():
    print("POST")
    if 'database' not in session:
        session["database"] = "my kanji"
    if (request.method == "POST"):
        if session["database"] == "kanji":
            session["database"] = "my kanji"
        else:
            session["database"] = "kanji"
    return redirect('/practice')

@app.route("/linked")
def linked():
    return redirect("/test")