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

import psycopg2

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

try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "docker",
                                  host = "localhost",
                                  port = "5432",
                                  database = "postgres")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

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
    #app = create_app()
    #port = app.config.get("PORT", 8080)
    app.run()
