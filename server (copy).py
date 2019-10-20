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

#import os
#import psycopg2

#from psycopg2 import sql

#from sqlalchemy import create_engine

from datetime import datetime

#import views

app=Flask(__name__)

#db_user="postgres"
#db_password="docker"
#host="localhost"
#port="5432"
#db_name="postgres"

#engine_params = (f'postgresql+psycopg2://{db_user}:{db_password}@{host}:{port}/{db_name}')

#engine = create_engine(engine_params)
#conn = engine.raw_connection()
#cur = conn.cursor()

#DATABASE_URL = os.environ['postgres://postgres:docker@localhost:5432/postgres']
#connection = psycopg2.connect(DATABASE_URL, sslmode='require')

#DATABASE_URL="postgres://postgres:docker@localhost:5432/postgres"
#connection = psycopg2.connect(user = "postgres",
#                                  password = "docker",
#                                  host = "localhost",
#                                  port = "5432",
#                                  database = "postgres",
#                                  sslmode='require')

#cursor = connection.cursor()

#create_table_query = '''CREATE TABLE mobile
#          (ID INT PRIMARY KEY     NOT NULL,
#          MODEL           TEXT    NOT NULL,
#          PRICE         REAL); '''
#    
#cursor.execute(create_table_query)
#connection.commit()
#print("Table created successfully in PostgreSQL ")
#
#    # Print PostgreSQL Connection properties
#print ( connection.get_dsn_parameters(),"\n")
#
#    # Print PostgreSQL version
#cursor.execute("SELECT version();")
#record = cursor.fetchone()
#print("You are connected to - ", record,"\n")
#
#    #closing database connection.
#if(connection):
#    cursor.close()
#    connection.close()
#    print("PostgreSQL connection is closed")

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
