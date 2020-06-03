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
    print('-->', end=": ")
    print(kanjinumber)
    return render_template("index.html", nav_index="active", myresult=myresult, kanjinumber=kanjinumber)