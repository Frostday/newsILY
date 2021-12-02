from flask import Flask, request, render_template, redirect
import requests
import sqlite3
import os
from textblob import TextBlob
from models import get_sentiment_and_entities

currentlocation = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

API_KEY = 'a42dad872d5b4758819201f7ec10292d'
logged_in = False
user_email = ''
user_name = ''
searched = False


@app.route('/', methods=['GET', 'POST'])
def index():
    global logged_in, user_email, user_name, searched
    if request.method == "POST":
        searched = True
        # print(request.form)
        keywords = request.form['article-keywords-phrase']
        language = request.form['language']
        # (YYYY-MM-DD)
        search_from = request.form['search-from']
        search_to = request.form['search-to']
        if request.form.get('dropdown-menu'):
            sorting = request.form['dropdown-menu']
        else:
            sorting = 'relevancy'

        url = 'https://newsapi.org/v2/everything?'
        if keywords != '':
            url += 'q=' + keywords + '&'
        if language != '':
            url += 'language=' + language + '&'
        else:
            url += 'language=en&'
        if search_from != '':
            url += 'from=' + search_from + '&'
        if search_to != '':
            url += 'to=' + search_to + '&'
        if sorting != '':
            url += 'sortBy=' + sorting + '&'
        url += 'apiKey=' + API_KEY

        response = requests.get(url)
        # print(response.json())
        articles = response.json()['articles']
        return render_template('./index.html', data=articles, x=logged_in, y=user_name, z=searched)
    else:
        searched = False
        url = (f'https://newsapi.org/v2/top-headlines?'
               'category=general&'
               'language=en&'
               f'apiKey={API_KEY}')
        response = requests.get(url)
        print(response.json())
        print(response.json()['articles'][0]['content'])
        articles = response.json()['articles']

        return render_template('./index.html', data=articles, x=logged_in, y=user_name, z=searched)


@app.route('/login', methods=['GET', 'POST'])
def checklogin():
    global logged_in, user_email, user_name
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        sqlconnection = sqlite3.Connection(currentlocation + "/login.db")
        cursor = sqlconnection.cursor()
        query = f'SELECT username, name FROM Users WHERE username="{email}" AND password="{password}"'
        rows = cursor.execute(query)
        rows = rows.fetchall()
        if len(rows) == 1:
            logged_in = True
            user_email = rows[0][0]
            user_name = rows[0][1]
            return redirect("/")
        else:
            return redirect("/register")
    return render_template("./login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        sqlconnection = sqlite3.Connection(currentlocation + "/login.db")
        cursor = sqlconnection.cursor()
        query = f'SELECT username, name FROM Users WHERE username="{email}" AND password="{password}"'
        rows = cursor.execute(query)
        rows = rows.fetchall()
        if len(rows) >= 1:
            print("User already exists")
        else:
            query = f"INSERT INTO Users VALUES('{email}', '{password}', '{name}')"
            cursor.execute(query)
            sqlconnection.commit()
        return redirect("/login")
    return render_template("./register.html")


@app.route('/shared', methods=['GET', 'POST'])
def shared():
    global logged_in, user_email, user_name
    return render_template("./shared.html")


@app.route('/article', methods=['GET', 'POST'])
def article_info():
    global logged_in, user_email, user_name
    info = eval(request.form['article-info'])
    b = TextBlob(info['description'])
    info['language'] = b.detect_language()
    if info['language'] == 'en':
        info['sentiment'], info['entities'], info['explained_entities'] = get_sentiment_and_entities(info['description'])
    else:
        info['sentiment'] = 'Cannot analyze in non-English language'
        info['entities'] = 'Cannot analyze in non-English language'
    return render_template("./article.html", x=logged_in, y=user_name, info=info)


app.run(debug=True, port=8080)
