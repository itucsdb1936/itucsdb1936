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
from flask import request, redirect, url_for

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



#def initialize(url):
#    with dbapi2.connect(url) as connection:
#        cursor = connection.cursor()
#        for statement in INIT_STATEMENTS:
#            cursor.execute(statement)
#        
#        cursor.close()
        
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

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/meetings")
def meetings_page():
    rows = query("postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0")
    return render_template("meetings.html", rows=sorted(rows), len=len(rows))

@app.route("/meetings_add", methods=["GET", "POST"])
def meetings_add_page():
    if request.method == "GET":
        return render_template(
            "meeting_add.html"
        )
    else:
        form_id = request.form["id"]
        form_placeid = request.form["place_id"]
        form_statusid = request.form["status_id"]
        form_date = request.form["date"]
        form_time = request.form["time"]
        form_duration = request.form["duration"]
        form_topic = request.form["topic"]
        form_result = request.form["result"]
        
        STATEMENTS = [ '''
                      INSERT INTO MEETINGS VALUES
                          (%s, %s, %s, '%s', '%s', '%s', '%s', '%s'); ''' % (form_id, form_placeid, form_statusid, form_date, form_time, form_duration, form_topic, form_result)  ]
        
        url= "postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
        
            cursor.close()
        
        return redirect(url_for("meetings_page"))

@app.route("/meetings_remove_<int:id>", methods=["GET", "POST"])
def meetings_remove(id):
        STATEMENTS = ['''
                              DELETE FROM MEETINGS
                                  WHERE (ID=%s); ''' % (id)]

        url = "postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)

            cursor.close()

        return redirect(url_for("meetings_page"))


@app.route("/meetings_remove", methods=["GET", "POST"])
def meetings_remove_page():
    if request.method == "GET":
        return render_template(
            "meeting_remove.html"
        )
    else:
        form_id = request.form["id"]
        
        STATEMENTS = [ '''
                      DELETE FROM MEETINGS
                          WHERE (ID=%s); ''' % (form_id)  ]

        url= "postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)

            cursor.close()

        return redirect(url_for("meetings_page"))

@app.route("/meetings_update", methods=["GET", "POST"])
def meetings_update_find_page():
    if request.method == "GET":
        return render_template(
            "meeting_update_find.html"
        )
    else:
        form_id = request.form["id"]
        
#        STATEMENTS = [ '''
#                      SELECT * FROM MEETINGS
#                          WHERE (ID=%s); ''' % (form_id)  ]
#            
#        url= "postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"
#        with dbapi2.connect(url) as connection:
#            cursor = connection.cursor()
#            for statement in STATEMENTS:
#                cursor.execute(statement)
#                
#            row = cursor.fetchone()
            
#            form_id = row[0]
#            form_placeid = row[1]
#            form_statusid = row[2]
#            form_date = row[3]
#            form_time = row[4]
#            form_duration = row[5]
#            form_topic = row[6]
#            form_result = row[7]
#            
#            cursor.close()
        
        return redirect(url_for("meetings_update_change_page", id=form_id))
    
@app.route("/meetings_update_<int:id>", methods=["GET", "POST"])
def meetings_update_change_page(id):
    if request.method == "GET":
        STATEMENTS = [ '''
                      SELECT * FROM MEETINGS
                          WHERE (ID=%s); ''' % (id)  ]
            
        url= "postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
                
            row = cursor.fetchone()
        return render_template(
            "meeting_update_change.html", row=row
        )
    else:
        form_id = request.form["id"]
        form_placeid = request.form["place_id"]
        form_statusid = request.form["status_id"]
        form_date = request.form["date"]
        form_time = request.form["time"]
        form_duration = request.form["duration"]
        form_topic = request.form["topic"]
        form_result = request.form["result"]
        
        STATEMENTS = [ '''
                      UPDATE MEETINGS
                          SET ID=%s, PlaceID=%s, StatusID=%s, DATE='%s', TIME='%s', Duration='%s', Topic='%s', RESULT='%s'
                          WHERE ID=%s; ''' % (form_id, form_placeid, form_statusid, form_date, form_time, form_duration, form_topic, form_result, form_id)  ]
        
        url= "postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
        
            cursor.close()
        
        return redirect(url_for("meetings_page"))

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
