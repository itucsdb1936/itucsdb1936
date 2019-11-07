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

#import os
#import sys

import psycopg2 as dbapi2

#INIT_STATEMENTS = [
#   '''create table IF NOT EXISTS MEETINGS (
#        ID int NOT NULL,
#        PlaceID int NOT NULL,
#        StatusID int NOT NULL,
#        DATE date NOT NULL,
#        TIME time NOT NULL,
#        Duration time,
#        Topic varchar(500)NOT NULL,
#        RESULT varchar(1500),
#        PRIMARY key (ID)
#        );''']



def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        
        cursor.close()
        
def query(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM MEETINGS")
        rows = cursor.fetchall()
        print("The: ", cursor.rowcount)
        for row in rows:
            print(row)
        
        cursor.close()
        return rows


from datetime import datetime

#import views

app=Flask(__name__)



@app.route("/")
def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

@app.route("/meetings")
def meetings_page():
    rows = query("postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0")
    return render_template("meetings.html", rows=sorted(rows), len=len(rows))

#def create_app():
#    app = Flask(__name__)
#    app.config.from_object("settings")
#
#    app.add_url_rule("/", view_func=views.home_page)
#
#    return app


if __name__ == "__main__":
    #url = os.getenv("DATABASE_URL")
    DATABASE_URL="postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"
#    if url is None:
#        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
#        sys.exit(1)
#    initialize(url)
    
#    initialize(DATABASE_URL)
    
    #query(DATABASE_URL)
    #app = create_app()
    #port = app.config.get("PORT", 8080)
    app.run()
