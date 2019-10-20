#from flask import Flask
#
#
#app = Flask(__name__)
#
#
#@app.route("/")
#def home_page():
#    return "Hello, ITU!"
##This is going well
#
#if __name__ == "__main__":
#    app.run()

from flask import Flask

from flask import render_template

import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS DUMMY (NUM INTEGER)",
    "INSERT INTO DUMMY VALUES (42)",
]

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


from datetime import datetime

#import views

app=Flask(__name__)



@app.route("/")
def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)
    
#def create_app():
#    app = Flask(__name__)
#    app.config.from_object("settings")
#
#    app.add_url_rule("/", view_func=views.home_page)
#
#    return app


if __name__ == "__main__":
    #url = os.getenv("DATABASE_URL")
    DATABASE_URL="postgres://postgres:docker@localhost:5432/postgres"
#    if url is None:
#        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
#        sys.exit(1)
#    initialize(url)
    initialize(DATABASE_URL)
    #app = create_app()
    #port = app.config.get("PORT", 8080)
    app.run()
