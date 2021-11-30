from flask import Flask, request, render_template, redirect, url_for
import requests
from datetime import date

app = Flask(__name__)

API_KEY = 'a42dad872d5b4758819201f7ec10292d'
logged_in = False
user_id = -1

@app.route('/', methods=['GET', 'POST'])
def index():
    today = date.today()
    url = (f'https://newsapi.org/v2/top-headlines?'
        'category=general&'
        f'apiKey={API_KEY}')
    response = requests.get(url)
    
    print(response.json())

    articles = response.json()['articles']

    return render_template('./index.html', data=articles)

app.run(debug=False, port=8080)
