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

@app.route("/practice",methods=["GET"])
@app.route("/practice/<kanji_num>")
def practice(kanji_num = 0):
    db_test = False
    if 'grades' in session:
        grades = session['grades']
    else:
        grades=[1]
    if db_test:
        b = "SELECT * FROM kanji_app_db.kanji_dict WHERE "
    else:
        #b = "SELECT * FROM kanji_app_db.my_kanji WHERE "
        b = "SELECT * FROM my_kanji mk JOIN kanji_dict kd ON mk.kanji_dict_id = kd.idkanji_dict WHERE "
    for i in grades:
        b += "grade = " + str(i) + " OR "
    b = b[:-3]  #deletes extra "OR" from end of query
    mycursor.execute(b)
    mykanji = mycursor.fetchall()
    jkanji = json.dumps(mykanji)
    for jk in jkanji:
        print(jk)
        #jkanji[jk].pop(0)
    print (jkanji)
    introkanji = mykanji[int(kanji_num)]
    return render_template("practice.html", nav_practice="active", mykanji=jkanji, introkanji=introkanji)

@app.route("/practice", methods=["POST"])
def add_kanji_to_db():
    #print(session["kanji_number"])
    print(request.form["kanji_number"])
    return redirect("/practice")

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
    print(x)
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
    kdata=request.form["kanji_number"]
    mk = ("INSERT INTO my_kanji (kanji_dict_id) VALUES (%s)" %(kdata))
    mycursor.execute(mk)
    mydb.commit()
    return redirect("/practice/", kanji_number = kanji_number)

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

@app.route("/test")
def test():
    x = "SELECT DISTINCT grade, COUNT(*) AS total FROM kanji_app_db.kanji_dict GROUP BY grade"
    if 'grades' in session:
        grades = session['grades']
    else:
        grades=[1]
    b = "SELECT * FROM kanji_app_db.kanji_dict WHERE "
    for i in test_list:
        b += "grade = " + str(i) + " OR "
    b = b[:-3]
    b += "ORDER BY RAND() LIMIT 1;"
    mycursor.execute(b)
    test_data = mycursor.fetchall()
    return render_template("test.html", test_data=test_data, grades = grades)

@app.route("/linked")
def linked():
    return redirect("/test")