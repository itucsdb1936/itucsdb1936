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
        values = {"topic":"", "date":""}
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
        return render_template(
            "meeting_remove.html"
        )
    else:        
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
        return render_template(
            "meeting_update_find.html"
        )
    else:

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
        values = {"topic":"","date":"","id":id}
        return render_template(
            "meeting_update_change.html", row=row, values=values
        )
    else:
        valid = validate_tech_form(request.form)
        if not valid:
            STATEMENTS = [ '''
                      SELECT * FROM MEETINGS
                          WHERE (ID=%s); ''' % (id)  ]
            
            url= DATABASE_URL
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                for statement in STATEMENTS:
                    cursor.execute(statement)
                    
            row = cursor.fetchone()
            return render_template("meeting_update_change.html", row=row, values=request.form)
        
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
            STATEMENTS = [ '''
                      SELECT * FROM TECH
                          WHERE (name='%s'); ''' % (name)  ]
            
            url= DATABASE_URL
            with dbapi2.connect(url) as connection:
                cursor = connection.cursor()
                for statement in STATEMENTS:
                    cursor.execute(statement)
                
            row = cursor.fetchone()
            row
            return render_template("tech_update_change.html", row=row, values=request.form)
        
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
    
    
### DEPARTMENTS
        
def departments_page():
    rows = query(DATABASE_URL, "DEPARTMENTS")
    return render_template("departments.html", rows=sorted(rows), len=len(rows))

def departments_add_page():
    if request.method == "GET":
        return render_template(
            "departments_add.html"
        )
    else:
        form_department_name = request.form["department_name"]
        form_manager = request.form["manager"]
        form_location = request.form["location"]
        form_capacity = request.form["capacity"]
        form_website = request.form["website"]
        
        STATEMENTS = [ '''
                      INSERT INTO DEPARTMENTS VALUES
                          ('%s', '%s', '%s', %s, '%s'); ''' % (form_department_name, form_manager, form_location, form_capacity, form_website)  ]
        
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
           cursor = connection.cursor()
           for statement in STATEMENTS:
               cursor.execute(statement)
        
           cursor.close()
        
        return redirect(url_for("departments_page"))

def departments_remove(department_name):
        STATEMENTS = ['''
                              DELETE FROM DEPARTMENTS
                                  WHERE (Department_Name='%s'); ''' % (department_name)]

        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)

            cursor.close()

        return redirect(url_for("departments_page"))
   
def departments_remove_page():
    if request.method == "GET":
        return render_template(
            "departments_remove.html"
        )
    else:        
        form_department_name = request.form["department_name"]
        
        STATEMENTS = [ '''
                      DELETE FROM DEPARTMENTS
                          WHERE (Department_Name='%s'); ''' % (form_department_name)  ]

        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)

            cursor.close()

        return redirect(url_for("departments_page"))

def departments_update_find_page():
    if request.method == "GET":
        return render_template(
            "departments_update_find.html"
        )
    else:

        form_department_name = request.form["department_name"]
        
        return redirect(url_for("departments_update_change_page", department_name=form_department_name))
    
def departments_update_change_page(department_name):
    if request.method == "GET":
        STATEMENTS = [ '''
                      SELECT * FROM DEPARTMENTS
                          WHERE (Department_Name='%s'); ''' % (department_name)  ]
            
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
                
            row = cursor.fetchone()
            
        return render_template(
            "departments_update_change.html", row=row
        )
    else:       
        form_department_name = request.form["department_name"]
        form_manager = request.form["manager"]
        form_location = request.form["location"]
        form_capacity = request.form["capacity"]
        form_website = request.form["website"]
        
        STATEMENTS = [ '''
                      UPDATE DEPARTMENTS
                          SET Manager='%s', Location='%s', Capacity=%s, Website='%s'
                          WHERE Department_Name='%s'; ''' % (form_manager, form_location, form_capacity, form_website, form_department_name)  ]
        
        url= DATABASE_URL
        with dbapi2.connect(url) as connection:
            cursor = connection.cursor()
            for statement in STATEMENTS:
                cursor.execute(statement)
        
            cursor.close()
        
        return redirect(url_for("departments_page"))
