from application import app, mydb
from flask import render_template, request, session
import json, random, math

mycursor = mydb.cursor(buffered=True)
mc = mydb.cursor()

@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def index():
    '''
    mycursor.execute("SELECT * FROM kanji_dict")
    mycursor.fetchall()
    kanjinumber = mycursor.rowcount
    mycursor.execute("SELECT DISTINCT grade FROM kanji_dict")
    myresult = mycursor.fetchall()
    if request.method == "POST":
        session['grades'] = request.form.getlist('grades')
    '''
    x = "SELECT DISTINCT grade, COUNT(*) AS total FROM kanji_app_db.kanji_dict GROUP BY grade"
    mycursor.execute(x)
    myresult = mycursor.fetchall()
    kanjinumber = sum(i[1] for i in myresult)
    return render_template("index.html", nav_index="active", myresult=myresult, kanjinumber=kanjinumber)

@app.route("/practice")
def practice():
    grades = session.pop('grades', [1])
    x = "SELECT * FROM kanji_dict WHERE grade = (%s)" % grades
    print (x)
    mycursor.execute("SELECT * FROM kanji_dict")
    mykanji = mycursor.fetchall()
    jkanji = json.dumps(mykanji)
    introkanji = mykanji[0]
    return render_template("practice.html", nav_practice="active", mykanji=jkanji, introkanji=introkanji)

@app.route("/quiz")
def quiz():
    grades = session.pop('grades', [1])
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
    return render_template("quiz.html", nav_quiz="active", quiz_kanji=quiz_kanji)

@app.route("/about")
def about():
    return render_template("about.html", nav_about="active")

@app.route("/test")
def test():
    x = "SELECT DISTINCT grade, COUNT(*) AS total FROM kanji_app_db.kanji_dict GROUP BY grade"
    mycursor.execute(x)
    test_data = mycursor.fetchall()
    t = sum(i[1] for i in test_data)
    print(t)
    return render_template("test.html", test_data=test_data, t=t)