import sqlite3
import os

currentlocation = os.path.dirname(os.path.abspath(__file__))
sqlconnection = sqlite3.Connection(currentlocation + "/login.db")
cursor = sqlconnection.cursor()
cursor.execute('''CREATE TABLE Users
               (username text, password text, name text)''')
sqlconnection.commit()
sqlconnection.close()

sqlconnection = sqlite3.Connection(currentlocation + "/shared.db")
cursor = sqlconnection.cursor()
cursor.execute('''CREATE TABLE Users
               (email_1 text, email_2 text, article_info text)''')
sqlconnection.commit()
sqlconnection.close()
