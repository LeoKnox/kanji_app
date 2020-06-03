from application import app, mydb
from flask import render_template

mycursor = mydb.cursor()

@app.route("/")
@app.route("/index")
def index():
    mycursor.execute("SELECT * FROM kanji_dict")
    myresult = mycursor.fetchall()
    return render_template("index.html", nav_index="active", myresult=myresult)