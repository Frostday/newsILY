from flask import Flask, request, render_template, redirect, url_for
import requests
import sqlite3
import os
currentlocation=os.path.dirname(os.path.abspath(__file__))

from datetime import date

app = Flask(__name__)

API_KEY = 'a42dad872d5b4758819201f7ec10292d'
logged_in = False
user_id = -1

@app.route('/', methods=['GET', 'POST'])
def index():
    url = (f'https://newsapi.org/v2/top-headlines?'
        'category=general&'
        f'apiKey={API_KEY}')
    response = requests.get(url)
    
    print(response.json())

    articles = response.json()['articles']

    return render_template('./index.html', data=articles)
@app.route('/', methods=['POST'])
def checklogin():
    UN=request.form['Username']
    PW=request.form['Password']
    sqlconnection=sqlite3.Connection(currentlocation + "/login.db")
    cursor=sqlconnection.cursor()
    query1="SELECT Username,Password From Users WHERE Username={UN} AND Password={PW})"
    rows=cursor.execute(query1)
    rows=rows.fetchall()
    if len(rows) == 1:
        return render_template("index.html")
    else :
        return redirect("/register")
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=="POST":
        dUN=request.form[' Enter Your sername']
        email=request.form['Enter Email ID']
        dPW=request.form[' Enter Password']
        sqlconnection=sqlite3.Connection(currentlocation + "/login.db")
        cursor=sqlconnection.cursor()
        query1="INSERT INTO Users VALUES('{u}','{p}','{ue}')".format(u=dUN,p=dPW,ue=email)
        cursor.execute(query1)
        sqlconnection.commit()
        return redirect("/")
    return render_template("Register.html")

app.run(debug=False, port=8080)
