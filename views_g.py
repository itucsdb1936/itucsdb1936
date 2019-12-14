from flask import render_template
from flask import request, redirect, url_for

from datetime import datetime

import psycopg2 as dbapi2

import os

#3DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_URL= "postgres://gvoybackrspqkf:339af7eacd4af135d7f93ef0df5dd3e25623e2a68da06335f5dc75855628fe95@ec2-54-247-171-30.eu-west-1.compute.amazonaws.com:5432/d7iva2beg4i1l0"

def query(url, table_name):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM %s" % (table_name))
        rows = cursor.fetchall()
        
        cursor.close()
        return rows

def validate_tech_form(form):
    form.data = {}
    form.errors = {}

    form_name = form.get("name", "").strip()
    if len(form_name) == 0:
        form.errors["name"] = "Name can not be blank."
    else:
        form.data["name"] = form_name

    return len(form.errors) == 0

def validate_meetings_form(form):
    form.data = {}
    form.errors = {}

    form_topic = form.get("topic", "").strip()
    if len(form_topic) == 0:
        form.errors["topic"] = "Topic can not be blank."
    else:
        form.data["topic"] = form_topic
        
    form_date = form.get("date")
    if not form_date:
        form.data["date"] = None
    else:
        date = form_date
        date = datetime.strptime(date, '%Y-%m-%d')
        if (date <  datetime.today()):
            form.errors["date"] = "Date can not be past."
        else:
            form.data["date"] = date

    return len(form.errors) == 0

### MEETINGS

def meetings_page():
    rows = query(DATABASE_URL, "MEETINGS")
    return render_template("meetings.html", rows=sorted(rows), len=len(rows))

def meetings_add_page():
    if request.method == "GET":
        values = {"id":"", "date":""}
        return render_template(
            "meeting_add.html", values=values
        )
    else:
        valid = validate_meetings_form(request.form)
        if not valid:
            return render_template("meeting_add.html", values=request.form)
        
        form_placeid = request.form["place_id"]
        form_date = request.form["date"]
        form_time = request.form["time"]
        form_topic = request.form["topic"]
        
        STATEMENTS = [ '''
                      INSERT INTO MEETINGS VALUES
                          (DEFAULT, %s, '%s', '%s', '%s'); ''' % (form_placeid, form_date, form_time, form_topic)  ]
        
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
           cursor = connection.cursor()
           for statement in STATEMENTS:
               cursor.execute(statement)
        
           cursor.close()
        
        return redirect(url_for("meetings_page"))

def meetings_remove(id):
        STATEMENTS = ['''
                              DELETE FROM MEETINGS
                                  WHERE (ID=%s); ''' % (id)]

        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)

            cursor.close()

        return redirect(url_for("meetings_page"))
    
def meetings_remove_page():
    if request.method == "GET":
        values = {"id":""}
        return render_template(
            "meeting_remove.html", values=values
        )
    else:
        valid = validate_meetings_form(request.form)
        if not valid:
            return render_template("meeting_remove.html", values=request.form)
        
        form_id = request.form["id"]
        
        STATEMENTS = [ '''
                      DELETE FROM MEETINGS
                          WHERE (ID=%s); ''' % (form_id)  ]

        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)

            cursor.close()

        return redirect(url_for("meetings_page"))

def meetings_update_find_page():
    if request.method == "GET":
        values = {"id":""}
        return render_template(
            "meeting_update_find.html", values=values
        )
    else:
        valid = validate_meetings_form(request.form)
        if not valid:
            return render_template("meetings_update_find.html", values=request.form)
        
        form_id = request.form["id"]
        
        return redirect(url_for("meetings_update_change_page", id=form_id))
    
def meetings_update_change_page(id):
    if request.method == "GET":
        STATEMENTS = [ '''
                      SELECT * FROM MEETINGS
                          WHERE (ID=%s); ''' % (id)  ]
            
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
                
            row = cursor.fetchone()
        values = {"id":"","date":"date"}
        return render_template(
            "meeting_update_change.html", row=row, values=values
        )
    else:
        valid = validate_tech_form(request.form)
        if not valid:
            return render_template("meeting_add.html", values=request.form)
        
        form_id = request.form["id"]
        form_placeid = request.form["place_id"]
        form_date = request.form["date"]
        form_time = request.form["time"]
        form_topic = request.form["topic"]
        
        STATEMENTS = [ '''
                      UPDATE MEETINGS
                          SET ID=%s, PlaceID=%s, DATE='%s', TIME='%s', Topic='%s'
                          WHERE ID=%s; ''' % (form_id, form_placeid, form_date, form_time, form_topic, form_id)  ]
        
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
        
            cursor.close()
        
        return redirect(url_for("meetings_page"))

### TECH

def tech_page():
    rows = query(DATABASE_URL, "TECH")
    return render_template("tech.html", rows=sorted(rows), len=len(rows))

def tech_add_page():
    if request.method == "GET":
        values = {"name":""}
        return render_template("tech_add.html", values=values)
    else:
        valid = validate_tech_form(request.form)
        if not valid:
            return render_template("tech_add.html", values=request.form)
        
        form_name = request.form["name"]
        form_projector = request.form["projector"]
        form_speaker = request.form["speaker"]
        form_computer = request.form["computer"]
        form_digital_whiteboard = request.form["digital_whiteboard"]
        
        STATEMENTS = [ '''
                      INSERT INTO tech VALUES
                          ('%s', '%s', '%s', '%s', '%s'); ''' % (form_name, form_projector, form_speaker, form_computer, form_digital_whiteboard)  ]
        
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
           cursor = connection.cursor()
           for statement in STATEMENTS:
               cursor.execute(statement)
        
           cursor.close()
        
        return redirect(url_for("tech_page"))

def tech_remove(name):
        STATEMENTS = ['''
                              DELETE FROM TECH
                                  WHERE (name='%s'); ''' % (name)]

        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)

            cursor.close()

        return redirect(url_for("tech_page"))
    
def tech_remove_page():
    if request.method == "GET":
        values = {"name":""}
        return render_template("tech_remove.html", values=values)
    else:
        valid = validate_tech_form(request.form)
        if not valid:
            return render_template("tech_remove.html", values=request.form)
        
        form_name = request.form["name"]
        
        STATEMENTS = [ '''
                      DELETE FROM TECH
                          WHERE (name='%s'); ''' % (form_name)  ]

        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)

            cursor.close()

        return redirect(url_for("tech_page"))

def tech_update_find_page():
    if request.method == "GET":
        values = {"name":""}
        return render_template("tech_update_find.html", values=values)
    else:
        valid = validate_tech_form(request.form)
        if not valid:
            return render_template("tech_update_find.html", values=request.form)
        
        form_name = request.form["name"]
        
        return redirect(url_for("tech_update_change_page", name=form_name))
    
def tech_update_change_page(name):
    if request.method == "GET":
        STATEMENTS = [ '''
                      SELECT * FROM TECH
                          WHERE (name='%s'); ''' % (name)  ]
            
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
                
            row = cursor.fetchone()
        values = {"name":""}
        return render_template("tech_update_change.html", row=row, values=values)
    else:
        valid = validate_tech_form(request.form)
        if not valid:
            return render_template("tech_add.html", values=request.form)
        
        form_name = request.form["name"]
        form_projector = request.form["projector"]
        form_speaker = request.form["speaker"]
        form_computer = request.form["computer"]
        form_digital_whiteboard = request.form["digital_whiteboard"]
        
        STATEMENTS = [ '''
                      UPDATE tech
                          SET Name='%s', Projector='%s', Speaker='%s', Computer='%s', DigitalWhiteboard='%s'
                          WHERE Name='%s'; ''' % (form_name, form_projector, form_speaker, form_computer, form_digital_whiteboard, form_name)  ]
        
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
        
            cursor.close()
        
        return redirect(url_for("tech_page"))